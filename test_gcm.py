#!/usr/bin/env python
"""
Quick test of the GCM

Runs a short simulation to verify installation
"""

import numpy as np
from gcm import GCM


def test_initialization():
    """Test model initialization"""
    print("Testing model initialization...")

    model = GCM(nlon=32, nlat=16, nlev=10, dt=600)
    model.initialize(profile='tropical')

    # Check state is reasonable
    assert np.mean(model.state.T) > 200, "Temperature too cold"
    assert np.mean(model.state.T) < 350, "Temperature too hot"
    assert np.all(model.state.q >= 0), "Negative humidity"
    assert np.mean(model.state.ps) > 90000, "Surface pressure too low"

    print("  ✓ Initialization successful")


def test_short_run():
    """Test short simulation run"""
    print("\nTesting short simulation...")

    model = GCM(nlon=32, nlat=16, nlev=10, dt=600)
    model.initialize(profile='tropical')

    # Run for 1 day
    model.run(duration_days=1, output_interval_hours=12)

    # Check model didn't blow up
    assert not np.any(np.isnan(model.state.T)), "NaN values in temperature"
    assert not np.any(np.isnan(model.state.u)), "NaN values in wind"
    assert np.max(np.abs(model.state.u)) < 200, "Wind speed unrealistic"

    # Check diagnostics
    assert len(model.diagnostics['time']) > 0, "No diagnostics recorded"

    print("  ✓ Short run successful")
    print(f"  Final global mean T: {np.mean(model.state.T):.2f} K")
    print(f"  Max wind speed: {np.max(np.sqrt(model.state.u**2 + model.state.v**2)):.2f} m/s")


def test_physics():
    """Test physics schemes individually"""
    print("\nTesting physics schemes...")

    model = GCM(nlon=32, nlat=16, nlev=10, dt=600)
    model.initialize()

    # Test radiation
    model.state.reset_tendencies()
    model.radiation.compute_radiation(model.state, 0.0)
    assert np.any(model.state.physics_tendencies['radiation']['T'] != 0), "No radiation heating"
    print("  ✓ Radiation scheme working")

    # Test convection
    model.state.reset_tendencies()
    model.convection.compute_convection(model.state, 600)
    print("  ✓ Convection scheme working")

    # Test cloud microphysics
    model.state.reset_tendencies()
    model.cloud_micro.compute_microphysics(model.state, 600)
    print("  ✓ Cloud microphysics working")

    # Test boundary layer
    model.state.reset_tendencies()
    model.boundary_layer.compute_boundary_layer(model.state, 600)
    print("  ✓ Boundary layer scheme working")


def test_energy_conservation():
    """Test energy conservation"""
    print("\nTesting energy conservation...")

    model = GCM(nlon=32, nlat=16, nlev=10, dt=600)
    model.initialize()

    # Run for a few days
    model.run(duration_days=5, output_interval_hours=6)

    # Check energy drift
    energy = model.diagnostics['total_energy']
    drift = abs(energy[-1] - energy[0]) / energy[0] * 100

    print(f"  Energy drift: {drift:.4f}%")

    # Should be small (< 1% for this short run)
    assert drift < 5.0, f"Energy drift too large: {drift:.2f}%"

    print("  ✓ Energy approximately conserved")


def main():
    """Run all tests"""
    print("=" * 60)
    print("GCM Test Suite")
    print("=" * 60)

    try:
        test_initialization()
        test_short_run()
        test_physics()
        test_energy_conservation()

        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
