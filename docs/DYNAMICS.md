# Atmospheric Dynamics

This document describes the dynamical core of the GCM.

## Governing Equations

The model solves the primitive equations on a rotating sphere.

### Momentum Equations

**Zonal momentum:**
```
∂u/∂t = -u*∂u/∂x - v*∂u/∂y - ω*∂u/∂p + f*v - (1/ρ)*∂Φ/∂x + F_u
```

**Meridional momentum:**
```
∂v/∂t = -u*∂v/∂x - v*∂v/∂y - ω*∂v/∂p - f*u - (1/ρ)*∂Φ/∂y + F_v
```

where:
- u, v: horizontal wind components
- ω = dp/dt: vertical velocity in pressure coordinates
- f = 2Ω*sin(φ): Coriolis parameter
- Φ: geopotential
- F: friction/diffusion terms

### Thermodynamic Equation

```
∂T/∂t = -u*∂T/∂x - v*∂T/∂y - ω*∂T/∂p + (κT/p)*ω + Q/cp
```

where:
- T: temperature
- κ = R_d/c_p: Poisson constant
- Q: diabatic heating rate

### Continuity Equation

**Mass conservation:**
```
∂ps/∂t = -∇·∫(ρV)dp
```

where ps is surface pressure.

### Moisture Equation

```
∂q/∂t = -u*∂q/∂x - v*∂q/∂y - ω*∂q/∂p + S_q
```

where S_q represents moisture sources/sinks.

### Hydrostatic Balance

```
∂Φ/∂p = -RT/p
```

## Coordinate System

### Horizontal Coordinates

**Spherical geometry:**
- Longitude: λ ∈ [0, 2π]
- Latitude: φ ∈ [-π/2, π/2]

**Metric terms:**
```
∂/∂x = 1/(R*cos(φ)) * ∂/∂λ
∂/∂y = 1/R * ∂/∂φ
```

### Vertical Coordinate

**Sigma coordinate:**
```
σ = (p - p_top) / (p_s - p_top)
```

Advantages:
- Terrain-following near surface
- Simplifies boundary conditions

## Discretization

### Horizontal Grid

**Latitude-Longitude Grid:**
- Equally spaced in longitude: Δλ = 2π/nlon
- Equally spaced in latitude: Δφ = π/(nlat-1)

**Pole Treatment:**
- Polar filter for latitudes |φ| > 80°
- Zonal averaging to prevent CFL violations

### Vertical Grid

**Sigma levels:**
- Evenly distributed from σ=0 (top) to σ=1 (surface)
- Variables at layer centers
- Fluxes at layer interfaces

### Operators

**Divergence on sphere:**
```
∇·V = 1/(R*cos(φ)) * [∂(u*cos(φ))/∂λ + ∂(v*cos(φ))/∂φ]
```

**Vorticity:**
```
ζ = 1/(R*cos(φ)) * [∂v/∂λ - ∂(u*cos(φ))/∂φ]
```

**Laplacian:**
```
∇²φ = 1/(R²*cos²(φ))*∂²φ/∂λ² + 1/(R²*cos(φ))*∂/∂φ(cos(φ)*∂φ/∂φ)
```

## Physical Processes

### Advection

**Horizontal advection:**

Computed using centered finite differences for spatial derivatives.

**Vertical advection:**

Uses pressure velocity ω from continuity equation:
```
ω_k = ω_{k-1} - ∫ ∇·V dp
```

### Pressure Gradient Force

Computed from geopotential:
```
F_pgf = -∇Φ = -g*∇z
```

where z is geopotential height from hydrostatic integration.

### Coriolis Force

```
F_cor,u = f*v
F_cor,v = -f*u
```

where f = 2Ω*sin(φ)

### Adiabatic Heating

From vertical motion:
```
dT/dt = (κT/p)*ω
```

Compression heating (ω < 0) or expansion cooling (ω > 0).

## Numerical Diffusion

Added for numerical stability:

**Horizontal diffusion:**
```
F_diff = ν_h * ∇²φ
```

with ν_h = 10⁵ m²/s

**Vertical diffusion:**

Handled by boundary layer scheme.

## Energy Conservation

The model conserves total energy (within numerical precision):

**Total Energy:**
```
E = KE + PE + IE
```

where:
- KE = (u² + v²)/2: kinetic energy
- PE = g*z: potential energy
- IE = c_v*T: internal energy

**Diagnostics:**

Energy components are tracked and reported at each output interval.

## Grid Configuration

### Standard Resolutions

| Name | nlon | nlat | nlev | Description |
|------|------|------|------|-------------|
| T21  | 64   | 32   | 20   | Low resolution |
| T42  | 128  | 64   | 20   | Medium resolution |
| T85  | 256  | 128  | 32   | High resolution |

### Vertical Levels

Distributed in sigma coordinate:

```python
sigma = np.linspace(0, 1, nlev+1)  # Interfaces
```

Higher resolution near surface for boundary layer.

## Computational Considerations

### Timestep

**CFL Condition:**

Maximum timestep limited by:
```
dt_max = min(Δx / u_max, Δy / v_max)
```

Typical values:
- T21: dt = 1200 s (20 min)
- T42: dt = 600 s (10 min)
- T85: dt = 300 s (5 min)

### Parallelization

Current implementation is serial. Future versions could parallelize:
- Latitude bands (MPI)
- Physics calculations (OpenMP)
- Spectral transforms (FFT libraries)

## Validation

The dynamical core has been tested against:

1. **Held-Suarez Test:**
   - Idealized forcing
   - Develops realistic jet streams and eddies

2. **Aquaplanet:**
   - Ocean-covered planet
   - Symmetric circulation patterns

3. **Jablonowski-Williamson Baroclinic Wave:**
   - Standard test for dynamical cores
   - Tests stability and accuracy
