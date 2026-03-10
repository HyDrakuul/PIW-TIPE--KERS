# TIPE Flywheel Curve Analysis

**Project purpose:**
This personal project is centered around acquiring, processing, and comparing rotational speed curves from a flywheel setup (volant d'inertie). It combines embedded data acquisition (Arduino), serial communication (Python), and data analysis/plotting to evaluate mechanical energy and behavior. The model used for this project was entirely designed and manufactured by me (model available in 3D_model/, designed on Autodesk Fusion 360) and 3D printed with PLA filament.

---

## What’s in this repository

- **Arduino firmware**: `src/tiperoue/tiperoue.ino`
  - Measures rotations via inductive hand made sensors.
  - Sends `tours/s` and timestamp values over Serial.
  - Displays speed on an LCD.

- **Python acquisition scripts**:
  - `src/data_acquisition.py` – reads serial data, plots it, and optionally saves curves to CSV.
  - `src/TIPEcourbe.py` – lightweight acquisition + plotting helper.
  - `src/comparaisons.py` – compares stored curves and computes rotational energy.

- **Tests & hardware validation**:
  - `tests/test_graphical.py` – simple tkinter GUI that stops a long-running loop.
  - `tests/testbobine/testbobine.ino` – test sketch for validating hand-made sensor coils (bobines) via analog voltage readings.

- **Data & output folders**:
  - `raw_datas/` – stored measurement CSVs.
  - `bin_curves/` – generated plot exports (curve images).
  - `docs/` – documentation notes and supplementary materials.
  - `tipe-courbes/` – additional curve-related files.
  - `3D_model/` - 3D model in .step format (for maximum compatibility) and in .f3d (origin format, Fusion 360 compatible).

---

##  Skills developed

This project demonstrates and helps develop the following skills:

- Serial communication and realtime data acquisition (Arduino ↔ Python)
- Signal processing and data cleaning (conversion from raw serial strings)
- Data visualization (matplotlib plots of speed and energy curves)
- Reproducible data structuring with CSV exports
- Basic GUI interaction (user validation of measurement runs)
- Embedded firmware development (interrupts + timing in Arduino)
- 3D printing, 3D modelling, electromagnetic and mechanical physics.

---

##  Running the project

### 1) Upload the Arduino sketch

1. Open `src/tiperoue/tiperoue.ino` in the Arduino IDE.
2. Connect your Arduino and select the correct board/port.
3. Upload the sketch.

### 2) Acquire data with Python

1. Install Python dependencies: `pyserial`, `matplotlib`, `numpy`.
2. Run the acquisition script:

```bash
python src/data_acquisition.py
```
4. Run the experiment while running the two programs in parallel. 
3. A plot will appear at the end of the experiment. If you confirm the curve looks valid, it will be appended to a CSV.

---

##  How to reproduce / customize the data storage 

### Change where curves are stored

The storage locations are explicitly written in `src/data_acquisition.py` for the CSV file and experiment counter file. To make this reproducible:

- Modify the paths near the bottom of `src/data_acquisition.py` to target a relative folder (e.g., `./raw_datas/`) instead of an absolute desktop path.
- Example: replace `"/Users/…/TIPE/TIPE_experience2.csv"` with `"raw_datas/TIPE_experience2.csv"`.

### Load curves from files instead of hardcoded arrays

In `src/comparaisons.py`, curve data is currently embedded as multi-line strings (`rw_temps`, `rw_vitesse`, ...). To reproduce the analysis with your own curves:

1. Save data into a CSV (as above).
2. Replace the hardcoded strings with a loader such as `numpy.loadtxt` or `pandas.read_csv`.


---

##  Project structure (detailed)

This project is organized into a few main folders. The following breakdown
explains the purpose of each folder and the key files you’ll likely work with.

### Core source code (`src/`)

- `src/tiperoue/` – **Arduino firmware**
  - `tiperoue.ino` : main sketch that reads the sensor coils, computes rotational
    speed, prints it over Serial, and displays it on an LCD.

- `src/data_acquisition.py` – **serial data acquisition and CSV export**
  - Connects to the Arduino over a serial port.
  - Collects and cleans the raw velocity/timestamp stream.
  - Optionally saves each measurement run as a CSV.

- `src/TIPEcourbe.py` – **simple acquisition + plotting helper**
  - Smaller script for quickly plotting a single run without saving.

- `src/comparaisons.py` – **curve comparison + energy plotting**
  - Loads previously recorded curve data (currently embedded in the script)
  - Plots multiple flywheel curves together and computes rotational energy.

### Test & validation (`tests/`)

- `tests/test_graphical.py` – GUI loop-stop demo
  - Useful to verify that you can interrupt a long-running acquisition cleanly.

- `tests/testbobine/` – sensor coil validation
  - `testbobine.ino` : Arduino sketch that reads an analog pin (A0) and prints
    the voltage. This is intended to validate hand-made sensor coils / wiring.

### Data, exports and documentation

- `raw_datas/` – stored measurement CSV files (raw acquisitions).
- `bin_curves/` – exported plot images (curve screenshots, etc.).
- `docs/` – additional documentation notes, plan of the model, results presentations and bibliography.
- `tipe-courbes/` – additional curve assets (e.g., scripts or export formats).

### 3D model (`3D_model`)

- Includes two files who contain the 3D model of the modulable KERS system (same model just differents extensions). 

---

##  Notes

- For best reproducibility, keep all generated data inside `raw_datas/` and update the path constants in the Python scripts.
- If you want to run analyses on new data sets, update `src/comparaisons.py` to load from the relevant file(s) rather than using embedded arrays.
