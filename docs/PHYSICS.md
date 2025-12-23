# Physics Parameterizations

This document describes the physics schemes implemented in the GCM.

## Radiation

### Shortwave Radiation

The shortwave radiation scheme uses a two-stream approximation with multiple spectral bands:

**Spectral Bands:**
1. UV-visible (0.2-0.7 μm): Rayleigh scattering, O₃ absorption
2. Near-IR (0.7-1.3 μm): H₂O absorption
3. IR (1.3-2.5 μm): H₂O, CO₂ absorption
4. IR (2.5-4.0 μm): H₂O, CO₂ absorption

**Processes:**
- Rayleigh scattering
- Ozone absorption (stratosphere)
- Water vapor absorption
- CO₂ absorption
- Cloud scattering and absorption

### Longwave Radiation

Uses 6 spectral bands optimized for atmospheric windows and absorption bands:

**Key Features:**
- CO₂ 15μm band (667 cm⁻¹)
- Water vapor continuum and line absorption
- Cloud emission and absorption
- Surface emission (Stefan-Boltzmann)

**Two-Stream Approximation:**
```
Upward flux: F↑ = (1-τ)*B + τ*F↑(below)
Downward flux: F↓ = (1-τ)*B + τ*F↓(above)
```

where τ is transmissivity and B is the Planck function.

## Convection

### Mass-Flux Scheme

Implements deep and shallow convection using a mass-flux parameterization.

**CAPE Calculation:**
```
CAPE = ∫ g*(T_parcel - T_env)/T_env dz
```

**Triggering:**
- Deep convection: CAPE > 500 J/kg
- Shallow convection: 100 < CAPE < 500 J/kg

**Processes:**
- Latent heat release from condensation
- Vertical moisture redistribution
- Momentum transport
- Convective precipitation

### Closure

Convective adjustment timescale τ = 3600 s

## Cloud Microphysics

### Two-Moment Scheme

Tracks both liquid (qc) and ice (qi) cloud condensate.

**Warm Processes:**
- Condensation/Evaporation (saturation adjustment)
- Autoconversion (cloud → precipitation): Kessler scheme
- Accretion (rain collecting droplets)

**Ice Processes:**
- Homogeneous freezing (T < -40°C)
- Heterogeneous freezing (-40°C < T < 0°C)
- Deposition/Sublimation
- Bergeron process (mixed-phase clouds)
- Melting (T > 0°C)

**Sedimentation:**
- Fall speed for liquid: 0.01 m/s
- Fall speed for ice: 0.5 m/s

## Boundary Layer

### TKE Scheme

Turbulent Kinetic Energy based parameterization.

**Surface Fluxes:**

Uses Monin-Obukhov similarity theory:
```
u* = friction velocity
T* = temperature scale
q* = moisture scale
```

**Stability Functions:**
- Stable (Ri > 0): ψ = -5Ri
- Unstable (Ri < 0): ψ from Businger-Dyer relations

**Eddy Diffusivity:**
```
K = c_k * l * √(TKE)
```

where l is mixing length = κz/(1 + κz/λ)

**Vertical Mixing:**

Diffusion equation:
```
∂φ/∂t = ∂/∂z(K ∂φ/∂z)
```

Applied to u, v, T, q

## Land Surface

### Multi-Layer Soil Model

**Soil Layers:**
- Layer 1: 0-5 cm
- Layer 2: 5-20 cm
- Layer 3: 20-70 cm
- Layer 4: 70-220 cm

**Processes:**

1. **Surface Energy Balance:**
   ```
   R_net = H + LE + G
   ```
   - R_net: Net radiation
   - H: Sensible heat flux
   - LE: Latent heat flux (evapotranspiration)
   - G: Ground heat flux

2. **Soil Heat Diffusion:**
   ```
   ∂T/∂t = κ ∂²T/∂z²
   ```
   where κ = thermal conductivity / heat capacity

3. **Soil Moisture:**
   ```
   ∂θ/∂t = P - E - R - D
   ```
   - θ: soil moisture
   - P: precipitation
   - E: evapotranspiration
   - R: runoff
   - D: drainage

4. **Snow:**
   - Accumulation (T < 0°C)
   - Melt (T > 0°C, proportional to excess temperature)
   - Albedo feedback (snow albedo = 0.8)

## Ocean

### Mixed Layer Model

**Slab Ocean:**
- Fixed mixed layer depth: 50 m
- Heat capacity: ρ*cp*h

**Heat Budget:**
```
ρ*cp*h*∂T/∂t = F_net + F_transport
```

**Ocean Heat Transport:**

Diffusive parameterization:
```
Q = -κ ∇²T
```

**Sea Ice Thermodynamics:**

1. **Formation:**
   - SST at freezing point + heat loss → ice formation
   - Energy: E = m*L_f

2. **Melt:**
   - Heat input + ice present → melting
   - Ice thickness and fraction evolve

3. **Properties:**
   - Freezing point: 271.4 K (-1.8°C)
   - Ice albedo: 0.7
   - Ocean albedo: 0.06

## Numerical Implementation

### Time Integration

**3rd Order Runge-Kutta (RK3):**

Default method for stability and accuracy.

```
k₁ = f(u_n)
k₂ = f(u_n + 0.5*dt*k₁)
k₃ = f(u_n + 0.75*dt*k₂)
u_{n+1} = u_n + dt*(k₁/6 + k₂/6 + 2k₃/3)
```

**Alternative Methods:**
- Forward Euler (1st order)
- Leapfrog (2nd order)
- Adams-Bashforth 2nd order

### Stability

**CFL Condition:**

For explicit schemes:
```
dt ≤ Δx / |u_max|
```

Typical time step: 600 s (10 minutes)

**Polar Filter:**

Applied at latitudes |lat| > 80° to avoid CFL issues:
- Zonal averaging with strength increasing toward poles

### Physical Constraints

Applied after each time step:
- q, qc, qi ≥ 0
- ps ≥ 1000 Pa
- 150 K ≤ T ≤ 400 K

## References

1. **Radiation**: Two-stream approximation, gas absorption
2. **Convection**: Mass-flux scheme, CAPE-based triggering
3. **Microphysics**: Two-moment scheme, Kessler autoconversion
4. **Boundary Layer**: TKE scheme, Monin-Obukhov theory
5. **Land Surface**: Force-restore method, bucket model
6. **Ocean**: Slab ocean, thermodynamic sea ice
