.. Virtual Magnetic Sensor documentation master file, created by
   sphinx-quickstart on Tue Oct 31 16:27:38 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Virtual Magnetic Sensor's documentation!
===================================================
Virtual Magnetic Sensor is a simulation software designed to model and simulate magnetic phenomena, specifically focused on magnetic sensor technology.



.. note::
   This project is under active development.



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Features
--------

- Simulates magnetic fields and sensor behavior
- Supports dynamic, time-dependent simulation of moving components
- Extensible with new components, sensors, and magnets

Support
-------

- **Email Support:** t.becker@rptu.de
- **GitHub Issues:** `GitHub Issues <https://github.com/mts-public/virtual_magnetic_sensor/issues>`_
- **Documentation:** `Virtual Magnetic Sensor Documentation <https://virtual-magnetic-sensor.readthedocs.io/index.html>`_
- **Netgen UI Documentation:** `Netgen UI Documentation <https://docu.ngsolve.org/latest/>`_

Installation Instructions
-------------------------

1. Install **Python 3.10** and update **pip**:
    ``python -m pip install --upgrade pip``

2. Clone this repository and navigate to the project folder containing the `pyproject.toml` file.

3. Install the package in editable mode:
    ``pip install -e .``

4. Run the software:
    ``python -m main``

Adding New Elements to the Simulation
-------------------------------------

To extend the simulation with new components, sensors, or magnets, follow these steps:

1. Create a New Element
~~~~~~~~~~~~~~~~~~~~~~~
- **Sensor:** Use `SensorTemplate.py`. Follow the comments and implement the conversion of magnetic field components to sensor output in the `set_data()` method.
- **Component:** Use `ComponentTemplate.py`. Follow the comments and define the time-dependent behavior of moving components in the `update()` method.
- **Magnet:** Use `MagnetTemplate.py`. Follow the comments.

2. Update the Frames
~~~~~~~~~~~~~~~~~~~~
- Edit `SensorTemplateFrame.py`, `ComponentTemplateFrame.py`, or `MagnetTemplateFrame.py` to include your new element in the GUI, following the comments inside the files.
- Add the new element to the appropriate parent frames:
  - `ComponentsFrame` for components
  - `SensorsFrame` for sensors
  - `MagnetsFrame` for magnets

   Implement an `add_template()` method and update the `init()` and `update_sub_frames()` methods accordingly. Refer to the example in the `SensorsFrame` class.

3. Update the CSG Files
~~~~~~~~~~~~~~~~~~~~~~~
- Modify `CSGSensorTemplate.py` to create the corresponding CSG element.
- Add the new element to `CSGComponents`, `CSGSensors` or `CSGMagnets`.
- For an example, see the comment in the `CSGSensors` class.

4. Update Data Handling
~~~~~~~~~~~~~~~~~~~~~~~
- In the `DataHandler` class, import the necessary template files (e.g., `ComponentTemplate.py`, `SensorTemplate.py`, or `MagnetTemplate.py`) to handle the new element.
