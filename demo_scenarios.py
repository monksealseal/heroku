#!/usr/bin/env python
"""
Quick GCM demonstration with multiple scenarios
Uses small resolution for fast execution
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import sys
import time
import os

# Setup paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output')

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Add GCM to path
sys.path.insert(0, SCRIPT_DIR)

print("="*60)
print("GCM DEMONSTRATION - Multiple Scenarios")
print("="*60)
print("\nImporting GCM modules...")

try:
    from gcm import GCM
    print("✓ GCM imported successfully")
except Exception as e:
    print(f"✗ Error importing GCM: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def run_scenario(name, profile, co2_ppmv=400, duration_days=3):
    """Run a single scenario with small resolution for speed"""
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"  Profile: {profile}, CO2: {co2_ppmv} ppmv, Duration: {duration_days} days")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        # Small resolution for fast demo
        model = GCM(
            nlon=24,   # Reduced for speed
            nlat=12,   # Reduced for speed
            nlev=8,    # Reduced for speed
            dt=1200,   # Larger timestep
            integration_method='rk3',
            co2_ppmv=co2_ppmv
        )

        print(f"  Initializing with {profile} profile...")
        model.initialize(profile=profile)

        print(f"  Running simulation...")
        model.run(duration_days=duration_days, output_interval_hours=24)

        elapsed = time.time() - start_time
        print(f"✓ Completed in {elapsed:.1f} seconds")

        # Print summary
        T_mean = np.mean(model.state.T)
        T_surf = np.mean(model.state.tsurf)
        u_max = np.max(np.sqrt(model.state.u**2 + model.state.v**2))

        print(f"  Global mean T: {T_mean:.2f} K")
        print(f"  Surface T: {T_surf:.2f} K")
        print(f"  Max wind: {u_max:.2f} m/s")

        return model

    except Exception as e:
        print(f"✗ Error in scenario: {e}")
        import traceback
        traceback.print_exc()
        return None

# Run scenarios
print("\n" + "="*60)
print("PART 1: ATMOSPHERIC PROFILES")
print("="*60)

scenarios = {}

print("\n1/6: Tropical atmosphere...")
scenarios['Tropical'] = run_scenario('Tropical', 'tropical', co2_ppmv=400, duration_days=3)

print("\n2/6: Midlatitude atmosphere...")
scenarios['Midlatitude'] = run_scenario('Midlatitude', 'midlatitude', co2_ppmv=400, duration_days=3)

print("\n3/6: Polar atmosphere...")
scenarios['Polar'] = run_scenario('Polar', 'polar', co2_ppmv=400, duration_days=3)

print("\n" + "="*60)
print("PART 2: CLIMATE SENSITIVITY")
print("="*60)

print("\n4/6: Pre-industrial (280 ppmv CO2)...")
scenarios['CO2_280ppmv'] = run_scenario('Pre-industrial', 'midlatitude', co2_ppmv=280, duration_days=3)

print("\n5/6: Current (420 ppmv CO2)...")
scenarios['CO2_420ppmv'] = run_scenario('Current', 'midlatitude', co2_ppmv=420, duration_days=3)

print("\n6/6: High CO2 (560 ppmv - 2×)...")
scenarios['CO2_560ppmv'] = run_scenario('2x CO2', 'midlatitude', co2_ppmv=560, duration_days=3)

# Filter out failed scenarios
scenarios = {k: v for k, v in scenarios.items() if v is not None}

if not scenarios:
    print("\n✗ No scenarios completed successfully")
    sys.exit(1)

print("\n" + "="*60)
print("GENERATING PLOTS")
print("="*60)

# Create comprehensive visualization
fig = plt.figure(figsize=(20, 24))
gs = GridSpec(6, 3, figure=fig, hspace=0.4, wspace=0.3)

fig.suptitle('GCM Simulation Results - Multiple Scenarios',
            fontsize=20, fontweight='bold', y=0.995)

# Row 1: Profile Comparison - Surface Temperature
print("\nCreating surface temperature plots...")
profile_scenarios = {k: v for k, v in scenarios.items() if 'CO2' not in k}
for idx, (name, model) in enumerate(profile_scenarios.items()):
    ax = fig.add_subplot(gs[0, idx])

    lon_deg = np.rad2deg(model.grid.lon)
    lat_deg = np.rad2deg(model.grid.lat)

    im = ax.contourf(lon_deg, lat_deg, model.state.tsurf,
                    levels=15, cmap='RdBu_r', vmin=250, vmax=310)
    ax.set_title(f'{name}\nSurface Temperature', fontweight='bold')
    ax.set_xlabel('Longitude (°)')
    ax.set_ylabel('Latitude (°)')
    plt.colorbar(im, ax=ax, label='K')

# Row 2: Profile Comparison - Zonal Wind
print("Creating zonal wind plots...")
for idx, (name, model) in enumerate(profile_scenarios.items()):
    ax = fig.add_subplot(gs[1, idx])

    k_mid = model.vgrid.nlev // 2
    lon_deg = np.rad2deg(model.grid.lon)
    lat_deg = np.rad2deg(model.grid.lat)

    im = ax.contourf(lon_deg, lat_deg, model.state.u[k_mid],
                    levels=15, cmap='RdBu_r', vmin=-30, vmax=30)
    ax.set_title(f'Zonal Wind (level {k_mid})', fontweight='bold')
    ax.set_xlabel('Longitude (°)')
    ax.set_ylabel('Latitude (°)')
    plt.colorbar(im, ax=ax, label='m/s')

# Row 3: Profile Comparison - Humidity
print("Creating humidity plots...")
for idx, (name, model) in enumerate(profile_scenarios.items()):
    ax = fig.add_subplot(gs[2, idx])

    k_mid = model.vgrid.nlev // 2
    lon_deg = np.rad2deg(model.grid.lon)
    lat_deg = np.rad2deg(model.grid.lat)

    im = ax.contourf(lon_deg, lat_deg, model.state.q[k_mid]*1000,
                    levels=15, cmap='YlGnBu', vmin=0, vmax=20)
    ax.set_title(f'Specific Humidity (level {k_mid})', fontweight='bold')
    ax.set_xlabel('Longitude (°)')
    ax.set_ylabel('Latitude (°)')
    plt.colorbar(im, ax=ax, label='g/kg')

# Row 4: Temperature Evolution
print("Creating temperature time series...")
ax = fig.add_subplot(gs[3, :])
for name, model in scenarios.items():
    ax.plot(model.diagnostics['time'],
           model.diagnostics['global_mean_T'],
           marker='o', linewidth=2, markersize=6, label=name)
ax.set_xlabel('Time (days)', fontsize=12)
ax.set_ylabel('Global Mean Temperature (K)', fontsize=12)
ax.set_title('Temperature Evolution - All Scenarios', fontsize=14, fontweight='bold')
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)

# Row 5: Climate Sensitivity
print("Creating climate sensitivity plot...")
co2_scenarios = {k: v for k, v in scenarios.items() if 'CO2' in k}
if co2_scenarios:
    co2_levels = [280, 420, 560]
    temps = []
    labels = []

    for co2 in co2_levels:
        key = f'CO2_{co2}ppmv'
        if key in co2_scenarios:
            model = co2_scenarios[key]
            temp = np.mean(model.diagnostics['global_mean_T'][-2:])
            temps.append(temp)
            labels.append(f'{co2}\nppmv')

    if temps:
        ax = fig.add_subplot(gs[4, 0])
        bars = ax.bar(range(len(temps)), temps,
                     color=['blue', 'green', 'red'][:len(temps)],
                     alpha=0.7, edgecolor='black', linewidth=2)
        ax.set_xticks(range(len(temps)))
        ax.set_xticklabels(labels)
        ax.set_ylabel('Temperature (K)', fontsize=12)
        ax.set_title('Climate Sensitivity to CO₂', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

        # Add values on bars
        for i, (bar, temp) in enumerate(zip(bars, temps)):
            ax.text(bar.get_x() + bar.get_width()/2, temp + 1,
                   f'{temp:.1f}K', ha='center', fontweight='bold')

        # Temperature change
        if len(temps) > 1:
            ax2 = fig.add_subplot(gs[4, 1])
            delta_T = [t - temps[0] for t in temps]
            bars2 = ax2.bar(range(len(delta_T)), delta_T,
                          color=['blue', 'green', 'red'][:len(delta_T)],
                          alpha=0.7, edgecolor='black', linewidth=2)
            ax2.set_xticks(range(len(delta_T)))
            ax2.set_xticklabels(labels)
            ax2.set_ylabel('ΔT (K)', fontsize=12)
            ax2.set_title('Temperature Change from 280 ppmv', fontsize=14, fontweight='bold')
            ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
            ax2.grid(True, alpha=0.3, axis='y')

            for i, (bar, dt) in enumerate(zip(bars2, delta_T)):
                ax2.text(bar.get_x() + bar.get_width()/2,
                        dt + 0.1 if dt > 0 else dt - 0.3,
                        f'{dt:+.2f}K', ha='center', fontweight='bold')

# Row 6: Energy Diagnostics
print("Creating energy diagnostics...")
ax = fig.add_subplot(gs[5, :2])
for name, model in scenarios.items():
    ax.plot(model.diagnostics['time'],
           model.diagnostics['total_energy'],
           marker='o', linewidth=2, markersize=4, label=name)
ax.set_xlabel('Time (days)', fontsize=12)
ax.set_ylabel('Total Energy (J/kg)', fontsize=12)
ax.set_title('Energy Conservation Check', fontsize=14, fontweight='bold')
ax.legend(loc='best', fontsize=9)
ax.grid(True, alpha=0.3)

# Statistics summary
ax = fig.add_subplot(gs[5, 2])
ax.axis('off')
summary_text = "Simulation Summary\n" + "="*30 + "\n\n"
for name, model in scenarios.items():
    T = np.mean(model.state.T)
    wind = np.max(np.sqrt(model.state.u**2 + model.state.v**2))
    summary_text += f"{name}:\n"
    summary_text += f"  T: {T:.1f} K\n"
    summary_text += f"  Wind: {wind:.1f} m/s\n\n"

ax.text(0.1, 0.9, summary_text, transform=ax.transAxes,
       fontsize=10, verticalalignment='top', fontfamily='monospace',
       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

print("\nSaving comprehensive plot...")
output_file = os.path.join(OUTPUT_DIR, 'gcm_scenarios_comprehensive.png')
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"✓ Saved: {output_file}")

plt.close()

# Create individual detailed plots
print("\nCreating individual scenario details...")

for name, model in list(scenarios.items())[:3]:  # First 3 scenarios
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle(f'Detailed View: {name} Scenario', fontsize=16, fontweight='bold')

    lon_deg = np.rad2deg(model.grid.lon)
    lat_deg = np.rad2deg(model.grid.lat)
    k_mid = model.vgrid.nlev // 2

    # Surface temperature
    im = axes[0, 0].contourf(lon_deg, lat_deg, model.state.tsurf,
                            levels=20, cmap='RdBu_r')
    axes[0, 0].set_title('Surface Temperature', fontweight='bold')
    axes[0, 0].set_xlabel('Longitude (°)')
    axes[0, 0].set_ylabel('Latitude (°)')
    plt.colorbar(im, ax=axes[0, 0], label='K')

    # Zonal wind
    im = axes[0, 1].contourf(lon_deg, lat_deg, model.state.u[k_mid],
                            levels=20, cmap='RdBu_r')
    axes[0, 1].set_title(f'Zonal Wind (level {k_mid})', fontweight='bold')
    axes[0, 1].set_xlabel('Longitude (°)')
    axes[0, 1].set_ylabel('Latitude (°)')
    plt.colorbar(im, ax=axes[0, 1], label='m/s')

    # Zonal mean temperature
    T_zonal = np.mean(model.state.T, axis=2)
    lat_deg_1d = np.rad2deg(model.grid.lat)
    for k in range(0, model.vgrid.nlev, 2):
        axes[1, 0].plot(lat_deg_1d, T_zonal[k],
                       label=f'Level {k}', linewidth=2)
    axes[1, 0].set_xlabel('Latitude (°)', fontsize=11)
    axes[1, 0].set_ylabel('Temperature (K)', fontsize=11)
    axes[1, 0].set_title('Zonal Mean Temperature', fontweight='bold')
    axes[1, 0].legend(fontsize=8)
    axes[1, 0].grid(True, alpha=0.3)

    # Diagnostics
    axes[1, 1].plot(model.diagnostics['time'],
                   model.diagnostics['global_mean_T'],
                   'b-o', linewidth=2, label='Temperature')
    axes[1, 1].set_xlabel('Time (days)', fontsize=11)
    axes[1, 1].set_ylabel('Temperature (K)', fontsize=11, color='b')
    axes[1, 1].tick_params(axis='y', labelcolor='b')
    axes[1, 1].set_title('Time Evolution', fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)

    ax2 = axes[1, 1].twinx()
    if len(model.diagnostics['global_mean_precip']) > 0:
        ax2.plot(model.diagnostics['time'],
                model.diagnostics['global_mean_precip'],
                'g-s', linewidth=2, label='Precipitation')
        ax2.set_ylabel('Precipitation (mm/hr)', fontsize=11, color='g')
        ax2.tick_params(axis='y', labelcolor='g')

    plt.tight_layout()
    filename = f'gcm_detail_{name.lower().replace(" ", "_")}.png'
    output_file = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(output_file, dpi=120, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

print("\n" + "="*60)
print("ALL PLOTS GENERATED!")
print("="*60)
print(f"\nGenerated files in: {OUTPUT_DIR}/")
print("  1. gcm_scenarios_comprehensive.png - Complete overview")
print("  2. gcm_detail_tropical.png - Tropical details")
print("  3. gcm_detail_midlatitude.png - Midlatitude details")
print("  4. gcm_detail_polar.png - Polar details")
print("\nAll scenarios completed successfully! 🎉")
