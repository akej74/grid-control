"""
    openhwmon.py
    ------------
    Implements communication with OpenHardwareMonitor using WMI.
    The module also provides functions for populating the QT Tree Widget with hardware nodes and temperature sensors.
"""

import sys

import wmi
from PyQt5 import QtCore, QtWidgets, QtGui

import helper


def initialize_hwmon():
    """Create a WMI object and verify that OpenHardwareMonitor is installed."""

    # Access the OpenHWMon WMI interface
    try:
        hwmon = wmi.WMI(namespace="root\OpenHardwareMonitor")
        return hwmon

    # WMI exception (e.g. no namespace "root\OpenHardwareMonitor" indicates OpenHWMon is not installed
    except:
        helper.show_error("OpenHardwareMonitor WMI data not found.\n\n"
                          "Please make sure that OpenHardwareMonitor is installed.\n\n"
                          "Latest version is available at:\n\n"
                          "http://openhardwaremonitor.org\n\n"
                          "The application will now exit.")
        sys.exit(0)


def populate_tree(hwmon, treeWidget):
    """Read sensor data from OpenHardwareMonitor using the available WMI interface,
    and populated the tree widget with the hardware nodes and sensors.

    Hardware nodes contains the following data, note that Parent = "" indicates a top node in the tree:

    Example:
    instance of Hardware
    {
        HardwareType = "Mainboard";
        Identifier = "/mainboard";
        InstanceId = "3839";
        Name = "ASUS MAXIMUS V GENE";
        Parent = "";
        ProcessId = "21816a7d-632f-4b9a-808f-0675d8eeca33";
    };

    Example:
    instance of Hardware
    {
        HardwareType = "SuperIO";
        Identifier = "/lpc/nct6779d";
        InstanceId = "3845";
        Name = "Nuvoton NCT6779D";
        Parent = "/mainboard";
        ProcessId = "21816a7d-632f-4b9a-808f-0675d8eeca33";
    };

    Sensors nodes contains the following data (including a parent hardware node), example:

    instance of Sensor
    {
        Identifier = "/lpc/nct6779d/temperature/0";
        Index = 0;
        InstanceId = "3898";
        Max = 40.5;
        Min = 20;
        Name = "CPU Core";
        Parent = "/lpc/nct6779d";
        ProcessId = "21816a7d-632f-4b9a-808f-0675d8eeca33";
        SensorType = "Temperature";
        Value = 30.5;
    };
    """

    # Get a list of hardware nodes
    hardwares = hwmon.Hardware()

    # Get a list of temperature sensor nodes (filtered to optimize WMI performance)
    sensors = hwmon.Sensor(["Name", "Parent", "Value", "Identifier"], SensorType="Temperature")

    # No sensor data (empty list) indicates OpenHWMon is not running
    if not sensors:
        helper.show_notification("No data from OpenHardwareMonitor found.\n\n"
                                 "Please make sure OpenHardwareMonitor is running.\n\n")

    # The "hardware_nodes" dictionary will hold all hardware nodes and children
    # key = top node identifier
    # value = list of all node identifiers (including the top node)
    hardware_nodes = {}

    # Add the top hardware nodes to the dictionary
    for hardware in hardwares:
        # No parent indicates it's a top node
        if hardware.Parent == "":
            hardware_nodes[hardware.Identifier] = [hardware.Identifier]

    # Add remaining hardware nodes to the dictionary, under the corresponding top node (dictionary key)
    for hardware in hardwares:
        # If the node has a parent, it's a child node
        if hardware.Parent != "":
            hardware_nodes[hardware.Parent].append(hardware.Identifier)

    # Add hardware nodes and temperature sensors to the three widget
    for key, nodelist in hardware_nodes.items():
        item_list = []
        for index, node in enumerate(nodelist):
            # First item in the list is the top node, parent should be the "treeWidget" itself
            if index == 0:
                parent = treeWidget
                item = QtWidgets.QTreeWidgetItem(parent)
                item.setText(0, get_hardware_name(nodelist[index], hardwares))  # First column, name of the node
                item.setText(1, nodelist[index])  # Second column, node id
                item.setFlags(QtCore.Qt.ItemIsEnabled)  # Make hardware nodes "not selectable" in the UI

                # Add the item to a list used when adding child nodes
                item_list.append(item)

            # Following items in the list are children, parent is the previous item in "item_list"
            else:
                parent = item_list[index-1]
                item = QtWidgets.QTreeWidgetItem(parent)
                item.setText(0, get_hardware_name(nodelist[index], hardwares))  # First column, name of the node
                item.setText(1, nodelist[index])  # Second column, node id
                item.setFlags(QtCore.Qt.ItemIsEnabled)  # Make hardware nodes "not selectable" in the UI
                item_list.append(item)

            for sensor in sensors:
                # If the sensor belongs to the current hardware node, add it as a child node
                if sensor.Parent == nodelist[index]:
                    sensor_parent = item_list[-1]  # Last item (QTreeWidgetItem) in the list is the parent
                    item = QtWidgets.QTreeWidgetItem(sensor_parent)

                    item.setText(0, sensor.Name)  # First column, name
                    item.setText(1, sensor.Identifier)  # Second column, id
                    item.setText(2, str(sensor.Value))  # Third column, temperature value

                    # Set node name and temperature value to blue
                    item.setForeground(0, QtGui.QBrush(QtCore.Qt.blue))
                    item.setForeground(2, QtGui.QBrush(QtCore.Qt.blue))

def get_temperature_sensors(hwmon):
    """Return all temperature sensors"""

    # Get a list of temperature sensor nodes (filtered to optimize WMI performance)
    sensors = hwmon.Sensor(["Name", "Parent", "Value", "Identifier"], SensorType="Temperature")
    return sensors

def get_temp(hwmon, id):
    """Return the temperature value for the sensor id."""

    # Get a list of temperature sensor nodes (filtered to optimize WMI performance)
    sensors = hwmon.Sensor(["Name", "Parent", "Value", "Identifier"], SensorType="Temperature")
    for sensor in sensors:
        if sensor.Identifier == id:
            return sensor.Value

def get_sensor_name(hwmon, id):
    """Return the name for a specific sensor id."""

    # Get a list of temperature sensor nodes (filtered to optimize WMI performance)
    sensors = hwmon.Sensor(["Name", "Parent", "Value", "Identifier"], SensorType="Temperature")
    for sensor in sensors:
        if sensor.Identifier == id:
            return sensor.Name

def get_hardware_name(id, hardwares):
    """Return the name for a specific node id in the list of hardware nodes."""

    for hardware in hardwares:
        if hardware.Identifier == id:
            return hardware.Name



