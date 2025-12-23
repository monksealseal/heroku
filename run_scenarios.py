#!/usr/bin/env python
"""
Run GCM on multiple scenarios and create comprehensive plots

This script demonstrates the model's capabilities by running:
1. Different atmospheric profiles (tropical, midlatitude, polar)
2. Climate sensitivity experiments (varying CO2)
3. Comparison visualizations
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import sys
sys.path.insert(0, '.')

from gcm import GCM


def run_scenario(name, profile, co2_ppmv=400, duration_days=15):
    """
    Run a single scenario

    Parameters
    ----------
    name : str
        Scenario name
    profile : str
        Atmospheric profile type
    co2_ppmv : float
        CO2 concentration
    duration_days : float
        Simulation duration

    Returns
    -------
    model : GCM
        Model instance with results
    """
    print(f"\n{'='*60}")
    print(f"Running scenario: {name}")
    print(f"  Profile: {profile}")
    print(f"  CO2: {co2_ppmv} ppmv")
    print(f"  Duration: {duration_days} days")
    print(f"{'='*60}")

    # Create model with moderate resolution
    model = GCM(
        nlon=48,
        nlat=24,
        nlev=16,
        dt=600,
        integration_method='rk3',
        co2_ppmv=co2_ppmv
    )

    # Initialize
    model.initialize(profile=profile)

    # Run
    model.run(duration_days=duration_days, output_interval_hours=6)

    print(f"✓ Scenario complete!")
    print(f"  Final global mean T: {np.mean(model.state.T):.2f} K")
    print(f"  Max wind speed: {np.max(np.sqrt(model.state.u**2 + model.state.v**2)):.2f} m/s")

    return model


def plot_scenario_comparison(scenarios, filename='scenario_comparison.png'):
    """
    Create comprehensive comparison plots

    Parameters
    ----------
    scenarios : dict
        Dictionary of {name: model} pairs
    filename : str
        Output filename
    """
    print(f"\nCreating comparison plots...")

    fig = plt.figure(figsize=(20, 12))
    gs = GridSpec(4, len(scenarios), figure=fig, hspace=0.3, wspace=0.3)

    scenario_names = list(scenarios.keys())

    # Row 1: Surface Temperature
    for i, (name, model) in enumerate(scenarios.items()):
        ax = fig.add_subplot(gs[0, i])

        lon_deg = np.rad2deg(model.grid.lon)
        lat_deg = np.rad2deg(model.grid.lat)

        im = ax.contourf(lon_deg, lat_deg, model.state.tsurf,
                        levels=20, cmap='RdBu_r', vmin=260, vmax=310)
        ax.set_title(f'{name}\nSurface Temperature', fontsize=10, fontweight='bold')
        ax.set_ylabel('Latitude')
        if i == 0:
            ax.set_xlabel('Longitude')
        plt.colorbar(im, ax=ax, label='K')

    # Row 2: Zonal Wind (mid-level)
    for i, (name, model) in enumerate(scenarios.items()):
        ax = fig.add_subplot(gs[1, i])

        k_mid = model.vgrid.nlev // 2
        lon_deg = np.rad2deg(model.grid.lon)
        lat_deg = np.rad2deg(model.grid.lat)

        im = ax.contourf(lon_deg, lat_deg, model.state.u[k_mid],
                        levels=20, cmap='RdBu_r', vmin=-40, vmax=40)
        ax.set_title(f'Zonal Wind (level {k_mid})', fontsize=10)
        ax.set_ylabel('Latitude')
        plt.colorbar(im, ax=ax, label='m/s')

    # Row 3: Specific Humidity
    for i, (name, model) in enumerate(scenarios.items()):
        ax = fig.add_subplot(gs[2, i])

        k_mid = model.vgrid.nlev // 2
        lon_deg = np.rad2deg(model.grid.lon)
        lat_deg = np.rad2deg(model.grid.lat)

        im = ax.contourf(lon_deg, lat_deg, model.state.q[k_mid]*1000,
                        levels=20, cmap='YlGnBu', vmin=0, vmax=15)
        ax.set_title(f'Specific Humidity (level {k_mid})', fontsize=10)
        ax.set_ylabel('Latitude')
        plt.colorbar(im, ax=ax, label='g/kg')

    # Row 4: Time series comparison
    ax = fig.add_subplot(gs[3, :])

    for name, model in scenarios.items():
        time_days = model.diagnostics['time']
        temp = model.diagnostics['global_mean_T']
        ax.plot(time_days, temp, label=name, linewidth=2, marker='o', markersize=4)

    ax.set_xlabel('Time (days)', fontsize=12)
    ax.set_ylabel('Global Mean Temperature (K)', fontsize=12)
    ax.set_title('Temperature Evolution Comparison', fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"✓ Saved comparison plot to {filename}")

    plt.close()


def plot_climate_sensitivity(co2_levels, temperatures, filename='climate_sensitivity.png'):
    """
    Plot climate sensitivity curve

    Parameters
    ----------
    co2_levels : list
        CO2 concentrations (ppmv)
    temperatures : list
        Equilibrium temperatures (K)
    filename : str
        Output filename
    """
    print(f"\nCreating climate sensitivity plot...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Temperature vs CO2
    ax1.plot(co2_levels, temperatures, 'o-', linewidth=2, markersize=10, color='red')
    ax1.set_xlabel('CO₂ Concentration (ppmv)', fontsize=12)
    ax1.set_ylabel('Equilibrium Temperature (K)', fontsize=12)
    ax1.set_title('Climate Sensitivity to CO₂', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Annotate key points
    for co2, temp in zip(co2_levels, temperatures):
        ax1.annotate(f'{temp:.1f}K', (co2, temp),
                    textcoords="offset points", xytext=(0,10), ha='center')

    # Plot 2: Temperature change relative to pre-industrial
    delta_T = np.array(temperatures) - temperatures[0]

    ax2.bar(range(len(co2_levels)), delta_T, color=['blue', 'green', 'orange', 'red'])
    ax2.set_xticks(range(len(co2_levels)))
    ax2.set_xticklabels([f'{co2}\nppmv' for co2 in co2_levels])
    ax2.set_ylabel('Temperature Change (K)', fontsize=12)
    ax2.set_title('Temperature Change Relative to Pre-Industrial', fontsize=14, fontweight='bold')
    ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax2.grid(True, alpha=0.3, axis='y')

    # Annotate values
    for i, dt in enumerate(delta_T):
        ax2.text(i, dt + 0.1, f'{dt:+.2f}K', ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"✓ Saved climate sensitivity plot to {filename}")

    plt.close()


def plot_vertical_profiles(scenarios, filename='vertical_profiles.png'):
    """
    Plot vertical profiles of temperature and wind

    Parameters
    ----------
    scenarios : dict
        Dictionary of {name: model} pairs
    filename : str
        Output filename
    """
    print(f"\nCreating vertical profile plots...")

    fig, axes = plt.subplots(1, 3, figsize=(15, 6))

    for name, model in scenarios.items():
        # Compute zonal and global means
        T_zonal = np.mean(model.state.T, axis=2)  # Average over longitude
        u_zonal = np.mean(model.state.u, axis=2)

        T_global = np.mean(T_zonal, axis=1)  # Average over latitude
        u_global = np.mean(u_zonal, axis=1)

        # Pressure levels (approximate)
        p_levels = np.linspace(100000, 10000, model.vgrid.nlev)

        # Plot temperature profile
        axes[0].plot(T_global, p_levels/100, marker='o', label=name, linewidth=2)

        # Plot wind profile
        axes[1].plot(u_global, p_levels/100, marker='o', label=name, linewidth=2)

        # Plot temperature vs latitude at mid-level
        k_mid = model.vgrid.nlev // 2
        lat_deg = np.rad2deg(model.grid.lat)
        axes[2].plot(lat_deg, T_zonal[k_mid], marker='o', label=name, linewidth=2)

    # Temperature profile
    axes[0].set_xlabel('Temperature (K)', fontsize=12)
    axes[0].set_ylabel('Pressure (hPa)', fontsize=12)
    axes[0].set_title('Vertical Temperature Profile', fontsize=12, fontweight='bold')
    axes[0].invert_yaxis()
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    # Wind profile
    axes[1].set_xlabel('Zonal Wind (m/s)', fontsize=12)
    axes[1].set_ylabel('Pressure (hPa)', fontsize=12)
    axes[1].set_title('Vertical Wind Profile', fontsize=12, fontweight='bold')
    axes[1].invert_yaxis()
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    # Latitude cross-section
    axes[2].set_xlabel('Latitude (°)', fontsize=12)
    axes[2].set_ylabel('Temperature (K)', fontsize=12)
    axes[2].set_title('Mid-Level Temperature vs Latitude', fontsize=12, fontweight='bold')
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"✓ Saved vertical profiles to {filename}")

    plt.close()


def plot_energy_diagnostics(scenarios, filename='energy_diagnostics.png'):
    """
    Plot energy diagnostics for all scenarios

    Parameters
    ----------
    scenarios : dict
        Dictionary of {name: model} pairs
    filename : str
        Output filename
    """
    print(f"\nCreating energy diagnostics plots...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Total Energy
    for name, model in scenarios.items():
        axes[0, 0].plot(model.diagnostics['time'],
                       model.diagnostics['total_energy'],
                       label=name, linewidth=2, marker='o', markersize=3)

    axes[0, 0].set_xlabel('Time (days)')
    axes[0, 0].set_ylabel('Total Energy (J/kg)')
    axes[0, 0].set_title('Total Energy Evolution', fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Kinetic Energy
    for name, model in scenarios.items():
        axes[0, 1].plot(model.diagnostics['time'],
                       model.diagnostics['kinetic_energy'],
                       label=name, linewidth=2, marker='o', markersize=3)

    axes[0, 1].set_xlabel('Time (days)')
    axes[0, 1].set_ylabel('Kinetic Energy (J/kg)')
    axes[0, 1].set_title('Kinetic Energy Evolution', fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Precipitation
    for name, model in scenarios.items():
        axes[1, 0].plot(model.diagnostics['time'],
                       model.diagnostics['global_mean_precip'],
                       label=name, linewidth=2, marker='o', markersize=3)

    axes[1, 0].set_xlabel('Time (days)')
    axes[1, 0].set_ylabel('Precipitation (mm/hr)')
    axes[1, 0].set_title('Global Mean Precipitation', fontweight='bold')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Energy Conservation Check
    for name, model in scenarios.items():
        energy = np.array(model.diagnostics['total_energy'])
        drift = (energy - energy[0]) / energy[0] * 100
        axes[1, 1].plot(model.diagnostics['time'], drift,
                       label=name, linewidth=2, marker='o', markersize=3)

    axes[1, 1].set_xlabel('Time (days)')
    axes[1, 1].set_ylabel('Energy Drift (%)')
    axes[1, 1].set_title('Energy Conservation Check', fontweight='bold')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].axhline(y=0, color='k', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"✓ Saved energy diagnostics to {filename}")

    plt.close()


def main():
    """Run all scenarios and create plots"""

    print("="*60)
    print("GCM SCENARIO ANALYSIS")
    print("Running multiple scenarios and creating visualizations")
    print("="*60)

    # ===== PART 1: Different Atmospheric Profiles =====
    print("\n### PART 1: ATMOSPHERIC PROFILE SCENARIOS ###\n")

    profile_scenarios = {}

    # Tropical
    profile_scenarios['Tropical'] = run_scenario(
        'Tropical',
        profile='tropical',
        co2_ppmv=400,
        duration_days=15
    )

    # Midlatitude
    profile_scenarios['Midlatitude'] = run_scenario(
        'Midlatitude',
        profile='midlatitude',
        co2_ppmv=400,
        duration_days=15
    )

    # Polar
    profile_scenarios['Polar'] = run_scenario(
        'Polar',
        profile='polar',
        co2_ppmv=400,
        duration_days=15
    )

    # Create comparison plots
    plot_scenario_comparison(profile_scenarios, 'scenario_comparison.png')
    plot_vertical_profiles(profile_scenarios, 'vertical_profiles.png')
    plot_energy_diagnostics(profile_scenarios, 'energy_diagnostics.png')

    # ===== PART 2: Climate Sensitivity =====
    print("\n### PART 2: CLIMATE SENSITIVITY EXPERIMENTS ###\n")

    co2_levels = [280, 400, 560, 800]
    co2_scenarios = {}
    temperatures = []

    for co2 in co2_levels:
        scenario_name = f'CO2_{co2}ppmv'
        model = run_scenario(
            scenario_name,
            profile='midlatitude',
            co2_ppmv=co2,
            duration_days=20
        )

        co2_scenarios[scenario_name] = model

        # Get equilibrium temperature (average of last 5 time points)
        T_eq = np.mean(model.diagnostics['global_mean_T'][-5:])
        temperatures.append(T_eq)

    # Plot climate sensitivity
    plot_climate_sensitivity(co2_levels, temperatures, 'climate_sensitivity.png')

    # Create comparison for CO2 scenarios
    plot_scenario_comparison(co2_scenarios, 'co2_scenario_comparison.png')

    # ===== PART 3: Summary Report =====
    print("\n### GENERATING SUMMARY REPORT ###\n")

    # Create summary figure
    create_summary_report(profile_scenarios, co2_scenarios, co2_levels, temperatures)

    print("\n" + "="*60)
    print("ALL SCENARIOS COMPLETE!")
    print("="*60)
    print("\nGenerated plots:")
    print("  1. scenario_comparison.png - Profile comparison")
    print("  2. vertical_profiles.png - Vertical structure")
    print("  3. energy_diagnostics.png - Energy evolution")
    print("  4. climate_sensitivity.png - CO2 sensitivity")
    print("  5. co2_scenario_comparison.png - CO2 comparison")
    print("  6. summary_report.png - Complete summary")
    print("="*60)


def create_summary_report(profile_scenarios, co2_scenarios, co2_levels, temperatures):
    """Create comprehensive summary report"""

    print("Creating comprehensive summary report...")

    fig = plt.figure(figsize=(20, 14))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)

    # Title
    fig.suptitle('GCM Comprehensive Scenario Analysis Report',
                fontsize=18, fontweight='bold', y=0.98)

    # 1. Profile comparison - Surface temp
    ax1 = fig.add_subplot(gs[0, 0])
    for name, model in profile_scenarios.items():
        T_mean_lat = np.mean(model.state.tsurf, axis=1)
        lat_deg = np.rad2deg(model.grid.lat)
        ax1.plot(lat_deg, T_mean_lat, marker='o', label=name, linewidth=2)
    ax1.set_xlabel('Latitude (°)')
    ax1.set_ylabel('Surface Temperature (K)')
    ax1.set_title('Surface Temperature by Profile', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Time evolution comparison
    ax2 = fig.add_subplot(gs[0, 1])
    for name, model in profile_scenarios.items():
        ax2.plot(model.diagnostics['time'],
                model.diagnostics['global_mean_T'],
                marker='o', label=name, linewidth=2, markersize=4)
    ax2.set_xlabel('Time (days)')
    ax2.set_ylabel('Global Mean Temperature (K)')
    ax2.set_title('Temperature Evolution by Profile', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. Climate sensitivity
    ax3 = fig.add_subplot(gs[0, 2])
    delta_T = np.array(temperatures) - temperatures[0]
    colors = ['blue', 'green', 'orange', 'red']
    bars = ax3.bar(range(len(co2_levels)), delta_T, color=colors, alpha=0.7, edgecolor='black')
    ax3.set_xticks(range(len(co2_levels)))
    ax3.set_xticklabels([f'{co2}\nppmv' for co2 in co2_levels])
    ax3.set_ylabel('ΔT (K)')
    ax3.set_title('Climate Sensitivity (ΔT from 280ppmv)', fontweight='bold')
    ax3.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax3.grid(True, alpha=0.3, axis='y')
    for i, (dt, bar) in enumerate(zip(delta_T, bars)):
        ax3.text(i, dt + 0.1 if dt > 0 else dt - 0.3, f'{dt:+.2f}K',
                ha='center', fontweight='bold', fontsize=10)

    # 4-6. Individual scenario snapshots (Tropical)
    model = profile_scenarios['Tropical']
    lon_deg = np.rad2deg(model.grid.lon)
    lat_deg = np.rad2deg(model.grid.lat)
    k_mid = model.vgrid.nlev // 2

    ax4 = fig.add_subplot(gs[1, 0])
    im4 = ax4.contourf(lon_deg, lat_deg, model.state.tsurf, levels=20, cmap='RdBu_r')
    ax4.set_title('Tropical: Surface Temperature', fontweight='bold')
    ax4.set_ylabel('Latitude')
    plt.colorbar(im4, ax=ax4, label='K')

    ax5 = fig.add_subplot(gs[1, 1])
    im5 = ax5.contourf(lon_deg, lat_deg, model.state.u[k_mid], levels=20, cmap='RdBu_r')
    ax5.set_title('Tropical: Mid-level Zonal Wind', fontweight='bold')
    plt.colorbar(im5, ax=ax5, label='m/s')

    ax6 = fig.add_subplot(gs[1, 2])
    im6 = ax6.contourf(lon_deg, lat_deg, model.state.q[k_mid]*1000, levels=20, cmap='YlGnBu')
    ax6.set_title('Tropical: Mid-level Humidity', fontweight='bold')
    plt.colorbar(im6, ax=ax6, label='g/kg')

    # 7-9. Summary statistics
    ax7 = fig.add_subplot(gs[2, 0])
    profile_names = list(profile_scenarios.keys())
    mean_temps = [np.mean(m.state.T) for m in profile_scenarios.values()]
    ax7.bar(profile_names, mean_temps, color=['red', 'orange', 'blue'], alpha=0.7, edgecolor='black')
    ax7.set_ylabel('Temperature (K)')
    ax7.set_title('Mean Atmospheric Temperature', fontweight='bold')
    ax7.grid(True, alpha=0.3, axis='y')
    for i, temp in enumerate(mean_temps):
        ax7.text(i, temp + 2, f'{temp:.1f}K', ha='center', fontweight='bold')

    ax8 = fig.add_subplot(gs[2, 1])
    max_winds = [np.max(np.sqrt(m.state.u**2 + m.state.v**2)) for m in profile_scenarios.values()]
    ax8.bar(profile_names, max_winds, color=['red', 'orange', 'blue'], alpha=0.7, edgecolor='black')
    ax8.set_ylabel('Wind Speed (m/s)')
    ax8.set_title('Maximum Wind Speed', fontweight='bold')
    ax8.grid(True, alpha=0.3, axis='y')
    for i, wind in enumerate(max_winds):
        ax8.text(i, wind + 1, f'{wind:.1f}', ha='center', fontweight='bold')

    ax9 = fig.add_subplot(gs[2, 2])
    # Climate sensitivity summary
    sensitivity_2x = delta_T[2]  # 560 ppmv (2x 280)
    sensitivity_3x = delta_T[3]  # 800 ppmv (~3x 280)

    ax9.text(0.5, 0.8, 'Climate Sensitivity Summary',
            ha='center', fontsize=14, fontweight='bold', transform=ax9.transAxes)
    ax9.text(0.5, 0.6, f'Pre-industrial (280 ppmv): {temperatures[0]:.2f} K',
            ha='center', fontsize=11, transform=ax9.transAxes)
    ax9.text(0.5, 0.5, f'Current (400 ppmv): {temperatures[1]:.2f} K ({delta_T[1]:+.2f} K)',
            ha='center', fontsize=11, transform=ax9.transAxes)
    ax9.text(0.5, 0.4, f'2×CO₂ (560 ppmv): {temperatures[2]:.2f} K ({delta_T[2]:+.2f} K)',
            ha='center', fontsize=11, fontweight='bold', color='red', transform=ax9.transAxes)
    ax9.text(0.5, 0.3, f'High (800 ppmv): {temperatures[3]:.2f} K ({delta_T[3]:+.2f} K)',
            ha='center', fontsize=11, transform=ax9.transAxes)
    ax9.text(0.5, 0.1, f'Climate Sensitivity (2×CO₂): {sensitivity_2x:.2f} K',
            ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5),
            transform=ax9.transAxes)
    ax9.axis('off')

    plt.savefig('summary_report.png', dpi=150, bbox_inches='tight')
    print("✓ Saved summary report to summary_report.png")

    plt.close()


if __name__ == '__main__':
    main()
