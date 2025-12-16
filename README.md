

# Classical Circuit Analogy of Quantum Double-Barrier Tunneling
![me](https://github.com/atsaavedra03/14-_IPL2/blob/main/Gain_Surface_C1_C2_rotation.gif)
This repository contains the complete codebase used for the final project:

**Identifying the Optimal Parameter Regimes for Gain Across Capacitively Coupled RLC Circuits as an Analogy for Quantum Tunneling Through a Double Barrier**

The project investigates a classical analog of one-dimensional quantum double-barrier tunneling using a minimal network of three capacitively coupled parallel RLC resonators. Experimental measurements are compared against a theoretical coupled-RLC model, with gain serving as the analog of the quantum transmission coefficient.

All data acquisition, processing, modeling, visualization, and figure generation used in the final poster are included here.

---

## Project Overview

### Physical Analogy

| Quantum System                         | Circuit Analog                          |
|---------------------------------------|------------------------------------------|
| Transmission coefficient \(T\)         | Gain                                    |
| Incident energy                        | Driving frequency                       |
| Barrier width                          | Inverse coupling capacitance \(1/C\)    |
| Double-barrier potential               | Two capacitive couplings between RLCs   |

The circuit consists of three identical parallel RLC resonators coupled in series by capacitors and driven sinusoidally. Measurements are performed using Analog Discovery 2 (AD2) units, with buffering and amplification used to mitigate noise.

---

## Repository Structure
```bash 
├── Amplifier/
│   ├── amplifier_behavior.ipynb
│   └── transfer_func_data_gain10_5000Hz_10n.csv

├── Capacitance Surface/
│   ├── figure_making.ipynb
│   ├── gmeasure.py
│   ├── measurement_capacitance_surface.ipynb
│   ├── the_critical_part.ipynb
│   ├── cap_sweep_data.npz
│   └── [generated figures and GIFs]

├── Frequency Sweeps/
│   ├── frequency_sweeps.ipynb
│   ├── gmeasure.py
│   ├── *.csv
│   ├── *.pdf
│   └── [generated figures]

├── Final Figures/
│   └── [compiled final figures]

└── README.md
```

---

## Folder and File Descriptions

### `Amplifier/`

This folder contains all code and data related to characterizing and correcting the operational amplifier used in the measurements.

#### Files

- **`amplifier_behavior.ipynb`**
  - Computes the op-amp transfer function.
  - Analyzes frequency-dependent gain behavior.
  - Produces a correction function used to compensate experimental data.

- **`transfer_func_data_gain10_5000Hz_10n.csv`**
  - Raw measurement data used to extract the amplifier transfer function.
  - Stores frequency sweep data at fixed gain and operating conditions.

---

### `Capacitance Surface/`

This folder contains the full workflow for measuring, storing, analyzing, and visualizing gain as a function of coupling capacitances.

#### Key Files

- **`measurement_capacitance_surface.ipynb`**
  - Performs experimental data acquisition using AD2.
  - Sweeps coupling capacitances \(C_p\) and \(C_{pp}\).
  - Stores raw measurement results.

- **`cap_sweep_data.npz`**
  - Stores all processed capacitance sweep data as NumPy matrices.
  - Used for fast reloading without repeating measurements.

- **`figure_making.ipynb`**
  - Generates:
    - 3D gain surfaces
    - Interpolated heatmaps
    - Contour plots
    - Rotating GIFs of the 3D surfaces
  - Serves as the main visualization pipeline for capacitance surface data.

- **`the_critical_part.ipynb`**
  - Computes the quantum mechanical transmission coefficient for a one-dimensional double-barrier potential.
  - Produces the final heatmap used for direct comparison with the circuit-based capacitance surface.

- **`gmeasure.py`**
  - Measurement utility library for AD2.
  - Provides reusable functions for signal generation, acquisition, and preprocessing.
  - Imported and used across multiple folders.

- **Additional files**
  - Generated figures (PNG/PDF)
  - Animated GIFs of rotating surfaces

---

### `Frequency Sweeps/`

This folder contains all measurements and analysis related to gain as a function of driving frequency.

#### Files

- **`frequency_sweeps.ipynb`**
  - Loads multiple frequency sweep CSV files into dataframes.
  - Applies amplifier correction and preprocessing.
  - Generates consolidated figures for gain vs. frequency.
  - Allows flexible selection of datasets for plotting.

- **`*.csv`**
  - Raw frequency sweep data files (e.g. `0.033uF_frequency_sweep_n5.csv`).
  - Each file corresponds to a fixed coupling capacitance.

- **`*.pdf`**
  - Exported high-quality figures generated from the frequency sweeps.

- **`gmeasure.py`**
  - Identical measurement utility module used for AD2-based acquisition.

---

### `Final Figures/`

- Contains a curated collection of all final figures used in the project poster.
- Includes:
  - Capacitance surface heatmaps
  - Frequency sweep plots
  - Quantum–classical comparison figures

---

## Requirements

- Python 3.9+
- NumPy
- SciPy
- Matplotlib
- Pandas
- Jupyter Notebook
- Analog Discovery 2 (for measurement notebooks)

---

## Notes

- All measurement notebooks assume access to AD2 hardware.
- All figure-generation notebooks can be run independently using stored `.csv` or `.npz` data.
- The repository is organized so that **no experimental data needs to be recollected** to reproduce the figures.

---

## Authors

**Andrés Tomás Saavedra Torres**
**Dongheon Kim**
**Joseph Jung**
Department of Physics and Astronomy  
Seoul National University

---

## License

This repository is intended for academic and educational use.


