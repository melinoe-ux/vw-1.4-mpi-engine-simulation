# VW 1.4 MPI Engine Cycle Simulation

A comprehensive thermodynamic simulation of the Volkswagen 1.4 liter Multi-Point Injection (MPI) engine, implementing progressive modeling from basic kinematics to complete cycle analysis with realistic combustion and heat transfer.

## Overview

This project implements a crank-angle resolved engine cycle simulation through seven progressive steps, demonstrating the quantitative impact of real-world phenomena on engine performance. The simulation reveals a 22.8% reduction in power output and 13.9 percentage point decrease in thermal efficiency when comparing idealized assumptions to physically realistic conditions.

## Engine Specifications

- **Engine**: Volkswagen 1.4 MPI
- **Displacement**: 1390 cm³ (1.4 L)
- **Configuration**: Inline 4-cylinder
- **Bore**: 76.5 mm
- **Stroke**: 75.6 mm
- **Compression Ratio**: 10.5:1
- **Connecting Rod**: 144 mm

## Key Results

### Performance Comparison (@ 3000 RPM)

| Metric | Ideal | Realistic | Difference |
|--------|-------|-----------|------------|
| Peak Pressure | 166.63 bar | 82.83 bar | -50.3% |
| IMEP | 22.36 bar | 17.26 bar | -22.8% |
| Power | 77.68 kW | 59.97 kW | -22.8% |
| Efficiency | 60.95% | 47.05% | -13.9 pp |

## Implementation Steps

### Step 1: Engine Parameters
Centralized parameter database with geometric, thermodynamic, and operational specifications.

### Step 2: Geometry (V(θ))
Slider-crank kinematics and instantaneous cylinder volume calculations.
- Verified displacement: 347.48 cm³/cylinder
- Compression ratio validation: 10.500

### Step 3: Ideal Otto Cycle
Classical four-state thermodynamic analysis.
- Theoretical efficiency: 60.96%
- IMEP: 22.36 bar

### Step 4: Crank-Angle Resolved Simulation
Integration of geometry with thermodynamics for continuous P(θ) and T(θ).
- 1° crank angle resolution
- Complete 720° four-stroke cycle

### Step 5: Wiebe Combustion Model
Progressive heat release over finite crank angle duration.
- Ignition timing: 15° BTDC
- Combustion duration: 50° CA
- Wiebe parameters: a=5, m=2

### Step 6: Woschni Heat Transfer
Convective heat transfer to cylinder walls.
- Wall temperature: 400 K
- Woschni constant: 130
- Temperature-dependent heat transfer coefficient

### Step 7: Performance Metrics
Complete analysis with IMEP, indicated power, and efficiency calculations.

## Project Structure

```
engine_cycle/
├── engine_parameters.py      # Engine specifications and constants
├── geometry.py                # Slider-crank kinematics
├── thermodynamics.py          # Ideal Otto cycle analysis
├── simulation.py              # Crank-angle resolved (ideal)
├── combustion.py              # Wiebe function implementation
├── heat_transfer.py           # Woschni correlation
├── advanced_simulation.py     # Complete realistic simulation
├── plots.py                   # Visualization functions
├── README.md                  # This file
└── [output plots]             # Generated visualizations
```

## Requirements

```bash
pip install numpy matplotlib
```

## Usage

### Run Individual Modules

```bash
# Geometry verification
python3 geometry.py

# Ideal Otto cycle
python3 thermodynamics.py

# Crank-angle resolved (ideal)
python3 simulation.py

# Wiebe combustion model
python3 combustion.py

# Heat transfer model
python3 heat_transfer.py
```

### Run Complete Analysis

```bash
# Execute full simulation with all models
python3 advanced_simulation.py
```

This generates comprehensive comparison plots and performance metrics.

## Generated Outputs

The simulation produces five primary visualizations:

1. **geometry_plots.png** - Piston position and cylinder volume vs. crank angle
2. **otto_pv_diagram.png** - Classical Otto cycle P-V diagram
3. **crank_angle_simulation.png** - Ideal P(θ), T(θ), and P-V trajectories
4. **wiebe_combustion.png** - Burned mass fraction and heat release rate
5. **final_comparison.png** - Comprehensive ideal vs. realistic comparison

## Technical Highlights

### Accurate Kinematics
- Slider-crank mechanism with connecting rod effects
- Verified geometric calculations (zero error)

### Thermodynamic Rigor
- Isentropic compression/expansion relations
- First-law energy balance with heat addition and losses
- Ideal gas law for P-V-T relationships

### Realistic Combustion
- Wiebe function with tunable parameters
- Progressive heat release over 40-60° CA
- Ignition timing control

### Heat Transfer Modeling
- Woschni correlation for convective heat transfer
- Temperature-dependent coefficients
- Instantaneous area calculation

### Performance Metrics
- Indicated work via ∮ P·dV integration
- IMEP (Indicated Mean Effective Pressure)
- Power calculation for 4-stroke cycle
- Thermal efficiency tracking

## Validation

- **Geometry**: All checks passed with <10⁻⁴ error
- **Otto Cycle**: Theoretical efficiency matches analytical formula
- **Compression**: P₂/P₁ = r^γ verified
- **Power Output**: 60 kW realistic for VW 1.4 MPI
- **Efficiency**: 47% typical for modern SI engines

## Future Extensions

- Variable valve timing effects
- Turbocharging simulation
- Multi-zone combustion modeling
- Exhaust gas recirculation (EGR)
- Mechanical friction losses (FMEP)
- Knock prediction models

## License

MIT License - Feel free to use and modify for educational and research purposes.

## Author

Developed as a comprehensive engine thermodynamics simulation project.

## References

- Heywood, J.B. (1988). *Internal Combustion Engine Fundamentals*. McGraw-Hill.
- Wiebe, I.I. (1956). *Semi-empirical expression for combustion rate in engines*.
- Woschni, G. (1967). *A universally applicable equation for the instantaneous heat transfer coefficient in the internal combustion engine*.
