[![DOI](https://zenodo.org/badge/700318323.svg)](https://zenodo.org/badge/latestdoi/700318323)

# Virtual Magnetic Sensor

Virtual Magnetic Sensor is a simulation software designed to model and simulate magnetic phenomena, specifically focused on magnetic sensor technology.

## Features
- Simulates magnetic fields and sensor behavior
- Supports dynamic, time-dependent simulation of moving components
- Extensible with new components, sensors, and magnets

## Associated Article
Becker, T., Glenske, C., Rauber, L., Seewig, J.: *Simulation Software for the Virtual Design and Analysis of Magnetic Sensor Systems*. Journal of open research software (2025).
DOI: https://doi.org/10.5334/jors.498

## Citation

If you use this software in academic work, please cite the article above.

## Support

- **Email Support:** t.becker@rptu.de
- **GitHub Issues:** [GitHub Issues](https://github.com/mts-public/virtual_magnetic_sensor/issues)
- **Documentation:** [Virtual Magnetic Sensor Documentation](https://virtual-magnetic-sensor.readthedocs.io/index.html)
- **NGSolve and Netgen Documentation:** [NGSolve](https://docu.ngsolve.org/latest/)

## Installation Instructions

1. Install **Python 3.10** and update **pip**:
    ```bash
    python -m pip install --upgrade pip
    ```

2. Clone this repository and navigate to the project folder containing the `pyproject.toml` file.

3. Install the package in editable mode:
    ```bash
    pip install -e .
    ```

4. Run the software:
    ```bash
    python -m main
    ```

## Adding New Elements to the Simulation

To extend the simulation with new components, sensors, or magnets, follow these steps:

### 1. Create a New Element
- **Sensor:** Use `SensorTemplate.py`. Follow the comments and implement the conversion of magnetic field components to sensor output in the `set_data()` method.
- **Component:** Use `ComponentTemplate.py`. Follow the comments and define the time-dependent behavior of moving components in the `update()` method.
- **Magnet:** Use `MagnetTemplate.py`. Follow the comments.

### 2. Update the Frames
- Edit `SensorTemplateFrame.py`, `ComponentTemplateFrame.py`, or `MagnetTemplateFrame.py` to include your new element in the GUI, following the comments inside the files.
- Add the new element to the appropriate parent frames:
  - `ComponentsFrame` for components
  - `SensorsFrame` for sensors
  - `MagnetsFrame` for magnets

   Implement an `add_template()` method and update the `init()` and `update_sub_frames()` methods accordingly. Refer to the example in the `SensorsFrame` class.

### 3. Update the CSG Files
- Modify `CSGSensorTemplate.py` to create the corresponding CSG element.
- Add the new element to `CSGComponents`, `CSGSensors` or `CSGMagnets`.
- For an example, see the comment in the `CSGSensors` class.

### 4. Update Data Handling
- In the `DataHandler` class, import the necessary template files (e.g., `ComponentTemplate.py`, `SensorTemplate.py`, or `MagnetTemplate.py`) to handle the new element.
