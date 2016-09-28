"""
    settings.py
    -----------
    Implements functions for reading and writing UI configuration using a QSettings object.
"""

from PyQt5 import QtCore, QtWidgets, QtGui

import openhwmon


def read_settings(config, ui, hwmon):
    """Read configuration from the OS repository (Registry in Windows, ini-file in Linux).

    Uses default values if no settings are found.
    "type=<type>" defines the data type.
    """

    #
    # "General" tab
    # ------------------------

    # Horizontal slider values (fan percent), default value "35"
    ui.horizontalSliderFan1.setValue(config.value("fan1_percent", 35, type=int))
    ui.horizontalSliderFan2.setValue(config.value("fan2_percent", 35, type=int))
    ui.horizontalSliderFan3.setValue(config.value("fan3_percent", 35, type=int))
    ui.horizontalSliderFan4.setValue(config.value("fan4_percent", 35, type=int))
    ui.horizontalSliderFan5.setValue(config.value("fan5_percent", 35, type=int))
    ui.horizontalSliderFan6.setValue(config.value("fan6_percent", 35, type=int))

    # Radio buttons
    ui.radioButtonManual.setChecked(config.value("manual_control", True, type=bool))
    ui.radioButtonAutomatic.setChecked(config.value("automatic_control", False, type=bool))

    # Serial port combo box value, default "<Select port>"
    # TODO: Remove unknown/not existing serial ports from stored values
    index = ui.comboBoxComPorts.findText(config.value("port", "<Select port>", type=str))
    ui.comboBoxComPorts.setCurrentIndex(index)
    if index == -1:
        ui.comboBoxComPorts.setCurrentIndex(0)

    # Polling interval combo box value, default "500" (ms)
    index = ui.comboBoxPolling.findText(config.value("polling", "500", type=str))
    ui.comboBoxPolling.setCurrentIndex(index)
    if index == -1:
        ui.comboBoxComPorts.setCurrentIndex(0)

    #
    # "Sensor Config" tab
    # ------------------------

    # Get all available temperature sensors
    sensors = openhwmon.get_temperature_sensors(hwmon)

    # Selected CPU sensors
    parent = ui.treeWidgetSelectedCPUSensors
    for id in config.value("cpu_sensor_ids", type=str):
        item = QtWidgets.QTreeWidgetItem(parent)
        for sensor in sensors:
            if sensor.Identifier == id:
                item.setText(0, sensor.Name)
        item.setText(1, id)
        item.setForeground(0, QtGui.QBrush(QtCore.Qt.blue))  # Text color blue

    # Selected GPU sensors
    parent = ui.treeWidgetSelectedGPUSensors
    for id in config.value("gpu_sensor_ids", type=str):
        item = QtWidgets.QTreeWidgetItem(parent)
        for sensor in sensors:
            if sensor.Identifier == id:
                item.setText(0, sensor.Name)
        item.setText(1, id)
        item.setForeground(0, QtGui.QBrush(QtCore.Qt.blue))  # Text color blue

    # Radio buttons
    ui.radioButtonCPUMax.setChecked(config.value("cpu_use_max", True, type=bool))
    ui.radioButtonCPUAverage.setChecked(config.value("cpu_use_avg", False, type=bool))
    ui.radioButtonGPUMax.setChecked(config.value("gpu_use_max", True, type=bool))
    ui.radioButtonGPUAverage.setChecked(config.value("gpu_use_avg", False, type=bool))

    #
    # "Fan Config" tab
    # ------------------------

    # Radio buttons
    ui.radioButtonCPUFan1.setChecked(config.value("cpu_fan_1", True, type=bool))
    ui.radioButtonCPUFan2.setChecked(config.value("cpu_fan_2", True, type=bool))
    ui.radioButtonCPUFan3.setChecked(config.value("cpu_fan_3", True, type=bool))
    ui.radioButtonCPUFan4.setChecked(config.value("cpu_fan_4", True, type=bool))
    ui.radioButtonCPUFan5.setChecked(config.value("cpu_fan_5", True, type=bool))
    ui.radioButtonCPUFan6.setChecked(config.value("cpu_fan_6", True, type=bool))

    ui.radioButtonGPUFan1.setChecked(config.value("gpu_fan_1", False, type=bool))
    ui.radioButtonGPUFan2.setChecked(config.value("gpu_fan_2", False, type=bool))
    ui.radioButtonGPUFan3.setChecked(config.value("gpu_fan_3", False, type=bool))
    ui.radioButtonGPUFan4.setChecked(config.value("gpu_fan_4", False, type=bool))
    ui.radioButtonGPUFan5.setChecked(config.value("gpu_fan_5", False, type=bool))
    ui.radioButtonGPUFan6.setChecked(config.value("gpu_fan_6", False, type=bool))

    # Fan speed and temperature data spinbox values
    ui.spinBoxMinSpeedFan1.setValue(config.value("min_speed_fan_1", 35, type=int))
    ui.spinBoxMinSpeedFan2.setValue(config.value("min_speed_fan_2", 35, type=int))
    ui.spinBoxMinSpeedFan3.setValue(config.value("min_speed_fan_3", 35, type=int))
    ui.spinBoxMinSpeedFan4.setValue(config.value("min_speed_fan_4", 35, type=int))
    ui.spinBoxMinSpeedFan5.setValue(config.value("min_speed_fan_5", 35, type=int))
    ui.spinBoxMinSpeedFan6.setValue(config.value("min_speed_fan_6", 35, type=int))

    ui.spinBoxStartIncreaseSpeedFan1.setValue(config.value("start_increase_speed_fan_1", 40, type=int))
    ui.spinBoxStartIncreaseSpeedFan2.setValue(config.value("start_increase_speed_fan_2", 40, type=int))
    ui.spinBoxStartIncreaseSpeedFan3.setValue(config.value("start_increase_speed_fan_3", 40, type=int))
    ui.spinBoxStartIncreaseSpeedFan4.setValue(config.value("start_increase_speed_fan_4", 40, type=int))
    ui.spinBoxStartIncreaseSpeedFan5.setValue(config.value("start_increase_speed_fan_5", 40, type=int))
    ui.spinBoxStartIncreaseSpeedFan6.setValue(config.value("start_increase_speed_fan_6", 40, type=int))

    ui.spinBoxIntermediateSpeedFan1.setValue(config.value("intermediate_speed_fan_1", 60, type=int))
    ui.spinBoxIntermediateSpeedFan2.setValue(config.value("intermediate_speed_fan_2", 60, type=int))
    ui.spinBoxIntermediateSpeedFan3.setValue(config.value("intermediate_speed_fan_3", 60, type=int))
    ui.spinBoxIntermediateSpeedFan4.setValue(config.value("intermediate_speed_fan_4", 60, type=int))
    ui.spinBoxIntermediateSpeedFan5.setValue(config.value("intermediate_speed_fan_5", 60, type=int))
    ui.spinBoxIntermediateSpeedFan6.setValue(config.value("intermediate_speed_fan_6", 60, type=int))

    ui.spinBoxIntermediateTempFan1.setValue(config.value("intermediate_temp_fan_1", 60, type=int))
    ui.spinBoxIntermediateTempFan2.setValue(config.value("intermediate_temp_fan_2", 60, type=int))
    ui.spinBoxIntermediateTempFan3.setValue(config.value("intermediate_temp_fan_3", 60, type=int))
    ui.spinBoxIntermediateTempFan4.setValue(config.value("intermediate_temp_fan_4", 60, type=int))
    ui.spinBoxIntermediateTempFan5.setValue(config.value("intermediate_temp_fan_5", 60, type=int))
    ui.spinBoxIntermediateTempFan6.setValue(config.value("intermediate_temp_fan_6", 60, type=int))

    ui.spinBoxMaxSpeedFan1.setValue(config.value("max_speed_fan_1", 100, type=int))
    ui.spinBoxMaxSpeedFan2.setValue(config.value("max_speed_fan_2", 100, type=int))
    ui.spinBoxMaxSpeedFan3.setValue(config.value("max_speed_fan_3", 100, type=int))
    ui.spinBoxMaxSpeedFan4.setValue(config.value("max_speed_fan_4", 100, type=int))
    ui.spinBoxMaxSpeedFan5.setValue(config.value("max_speed_fan_5", 100, type=int))
    ui.spinBoxMaxSpeedFan6.setValue(config.value("max_speed_fan_6", 100, type=int))

    ui.spinBoxMaxTempFan1.setValue(config.value("max_temp_fan_1", 75, type=int))
    ui.spinBoxMaxTempFan2.setValue(config.value("max_temp_fan_2", 75, type=int))
    ui.spinBoxMaxTempFan3.setValue(config.value("max_temp_fan_3", 75, type=int))
    ui.spinBoxMaxTempFan4.setValue(config.value("max_temp_fan_4", 75, type=int))
    ui.spinBoxMaxTempFan5.setValue(config.value("max_temp_fan_5", 75, type=int))
    ui.spinBoxMaxTempFan6.setValue(config.value("max_temp_fan_6", 75, type=int))

    #
    # "Rename Fans" tab
    # ------------------------

    # Fan labels, default "Fan 1" ... "Fan 6"
    ui.lineEditFan1.setText(config.value("fan1_name", "Fan 1", type=str))
    ui.lineEditFan2.setText(config.value("fan2_name", "Fan 2", type=str))
    ui.lineEditFan3.setText(config.value("fan3_name", "Fan 3", type=str))
    ui.lineEditFan4.setText(config.value("fan4_name", "Fan 4", type=str))
    ui.lineEditFan5.setText(config.value("fan5_name", "Fan 5", type=str))
    ui.lineEditFan6.setText(config.value("fan6_name", "Fan 6", type=str))

def save_settings(config, ui):
    """Save current UI configuration to the OS repository, called when exiting the main application"""

    #
    # "General" tab
    # ------------------------
    # Fan slider values
    config.setValue("fan1_percent", ui.horizontalSliderFan1.value())
    config.setValue("fan2_percent", ui.horizontalSliderFan2.value())
    config.setValue("fan3_percent", ui.horizontalSliderFan3.value())
    config.setValue("fan4_percent", ui.horizontalSliderFan4.value())
    config.setValue("fan5_percent", ui.horizontalSliderFan5.value())
    config.setValue("fan6_percent", ui.horizontalSliderFan6.value())

    # Serial port
    config.setValue("port", ui.comboBoxComPorts.currentText())

    # Polling interval
    config.setValue("polling", ui.comboBoxPolling.currentText())

    # Radio buttons
    config.setValue("automatic_control", ui.radioButtonAutomatic.isChecked())
    config.setValue("manual_control", ui.radioButtonManual.isChecked())

    #
    # "Sensor Config" tab
    # ------------------------

    # Selected CPU sensors
    root = ui.treeWidgetSelectedCPUSensors.invisibleRootItem()
    child_count = root.childCount()
    cpu_sensor_ids = []
    for i in range(child_count):
        item = root.child(i)
        cpu_sensor_ids.append(item.text(1))
    config.setValue("cpu_sensor_ids", cpu_sensor_ids)

    # Selected GPU sensors
    root = ui.treeWidgetSelectedGPUSensors.invisibleRootItem()
    child_count = root.childCount()
    gpu_sensor_ids = []
    for i in range(child_count):
        item = root.child(i)
        gpu_sensor_ids.append(item.text(1))
    config.setValue("gpu_sensor_ids", gpu_sensor_ids)

    # Radio buttons
    config.setValue("cpu_use_max", ui.radioButtonCPUMax.isChecked())
    config.setValue("cpu_use_avg", ui.radioButtonCPUAverage.isChecked())
    config.setValue("gpu_use_max", ui.radioButtonGPUMax.isChecked())
    config.setValue("gpu_use_avg", ui.radioButtonGPUAverage.isChecked())

    #
    # "Fan Config" tab
    # ------------------------

    # Radio buttons
    config.setValue("cpu_fan_1", ui.radioButtonCPUFan1.isChecked())
    config.setValue("cpu_fan_2", ui.radioButtonCPUFan2.isChecked())
    config.setValue("cpu_fan_3", ui.radioButtonCPUFan3.isChecked())
    config.setValue("cpu_fan_4", ui.radioButtonCPUFan4.isChecked())
    config.setValue("cpu_fan_5", ui.radioButtonCPUFan5.isChecked())
    config.setValue("cpu_fan_6", ui.radioButtonCPUFan6.isChecked())

    config.setValue("gpu_fan_1", ui.radioButtonGPUFan1.isChecked())
    config.setValue("gpu_fan_2", ui.radioButtonGPUFan2.isChecked())
    config.setValue("gpu_fan_3", ui.radioButtonGPUFan3.isChecked())
    config.setValue("gpu_fan_4", ui.radioButtonGPUFan4.isChecked())
    config.setValue("gpu_fan_5", ui.radioButtonGPUFan5.isChecked())
    config.setValue("gpu_fan_6", ui.radioButtonGPUFan6.isChecked())

    # Fan and temp data spinbox values
    config.setValue("min_speed_fan_1", ui.spinBoxMinSpeedFan1.value())
    config.setValue("min_speed_fan_2", ui.spinBoxMinSpeedFan2.value())
    config.setValue("min_speed_fan_3", ui.spinBoxMinSpeedFan3.value())
    config.setValue("min_speed_fan_4", ui.spinBoxMinSpeedFan4.value())
    config.setValue("min_speed_fan_5", ui.spinBoxMinSpeedFan5.value())
    config.setValue("min_speed_fan_6", ui.spinBoxMinSpeedFan6.value())

    config.setValue("start_increase_speed_fan_1", ui.spinBoxStartIncreaseSpeedFan1.value())
    config.setValue("start_increase_speed_fan_2", ui.spinBoxStartIncreaseSpeedFan2.value())
    config.setValue("start_increase_speed_fan_3", ui.spinBoxStartIncreaseSpeedFan3.value())
    config.setValue("start_increase_speed_fan_4", ui.spinBoxStartIncreaseSpeedFan4.value())
    config.setValue("start_increase_speed_fan_5", ui.spinBoxStartIncreaseSpeedFan5.value())
    config.setValue("start_increase_speed_fan_6", ui.spinBoxStartIncreaseSpeedFan6.value())

    config.setValue("intermediate_speed_fan_1", ui.spinBoxIntermediateSpeedFan1.value())
    config.setValue("intermediate_speed_fan_2", ui.spinBoxIntermediateSpeedFan2.value())
    config.setValue("intermediate_speed_fan_3", ui.spinBoxIntermediateSpeedFan3.value())
    config.setValue("intermediate_speed_fan_4", ui.spinBoxIntermediateSpeedFan4.value())
    config.setValue("intermediate_speed_fan_5", ui.spinBoxIntermediateSpeedFan5.value())
    config.setValue("intermediate_speed_fan_6", ui.spinBoxIntermediateSpeedFan6.value())

    config.setValue("intermediate_temp_fan_1", ui.spinBoxIntermediateTempFan1.value())
    config.setValue("intermediate_temp_fan_2", ui.spinBoxIntermediateTempFan2.value())
    config.setValue("intermediate_temp_fan_3", ui.spinBoxIntermediateTempFan3.value())
    config.setValue("intermediate_temp_fan_4", ui.spinBoxIntermediateTempFan4.value())
    config.setValue("intermediate_temp_fan_5", ui.spinBoxIntermediateTempFan5.value())
    config.setValue("intermediate_temp_fan_6", ui.spinBoxIntermediateTempFan6.value())

    config.setValue("max_speed_fan_1", ui.spinBoxMaxSpeedFan1.value())
    config.setValue("max_speed_fan_2", ui.spinBoxMaxSpeedFan2.value())
    config.setValue("max_speed_fan_3", ui.spinBoxMaxSpeedFan3.value())
    config.setValue("max_speed_fan_4", ui.spinBoxMaxSpeedFan4.value())
    config.setValue("max_speed_fan_5", ui.spinBoxMaxSpeedFan5.value())
    config.setValue("max_speed_fan_6", ui.spinBoxMaxSpeedFan6.value())

    config.setValue("max_temp_fan_1", ui.spinBoxMaxTempFan1.value())
    config.setValue("max_temp_fan_2", ui.spinBoxMaxTempFan2.value())
    config.setValue("max_temp_fan_3", ui.spinBoxMaxTempFan3.value())
    config.setValue("max_temp_fan_4", ui.spinBoxMaxTempFan4.value())
    config.setValue("max_temp_fan_5", ui.spinBoxMaxTempFan5.value())
    config.setValue("max_temp_fan_6", ui.spinBoxMaxTempFan6.value())

    #
    # "Rename Fans" tab
    # ------------------------

    # Fan labels
    config.setValue("fan1_name", ui.lineEditFan1.text())
    config.setValue("fan2_name", ui.lineEditFan2.text())
    config.setValue("fan3_name", ui.lineEditFan3.text())
    config.setValue("fan4_name", ui.lineEditFan4.text())
    config.setValue("fan5_name", ui.lineEditFan5.text())
    config.setValue("fan6_name", ui.lineEditFan6.text())