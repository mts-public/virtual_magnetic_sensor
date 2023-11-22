[![DOI](https://zenodo.org/badge/700318323.svg)](https://zenodo.org/badge/latestdoi/700318323)

# virtual_magnetic_sensor
Virtual Magnetic Sensor is a simulation software for the simulation of magnetic problems in regard to magnetic sensor technology.

# Installation Instructions
1. Install Python 3.10 and update pip
2. Install packages in the requirements.txt file
3. Add the working directory "Virtual Magnetic Sensor" to PYTHONPATH
4. Run apps/main.py

# Add New Elements to the Simulation Software
1.	Use the template files ComponentTemplate.py, SensorTemplate.py or MagnetTemplate.py and edit them according to the comments.
    1. In the case of a sensor implementation: Add the conversion of the magnetic field components to sensor output signals to the set_data() method.
    2. In case of a component implementation: Add the time-dependent behaviour of moving components to the update() method.
2.	Use the SensorTemplateFrame.py template file and edit it according to the comments.
3.	Add the element to the ComponentsFrame, SensorsFrame or MagnetsFrame classes by implementing an add_template() method and extending the init() and update_sub_frames() methods. For an example, see the comment in the SensorsFrame class.
4.	Use the template file CSGSensorTemplate.py and implement and edit it according to the comment.
5.	Add the new element to the CSGComponents, CSGSensors or CSGMagnets classes. For an example, see the comment in the CSGSensors class.
6.	Add the new element to the DataHandler class by adding the import statement (Import ComponentTemplate.py, SensorTemplate.py or MagnetTemplate.py).
