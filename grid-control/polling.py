"""
    polling.py
    ----------
    Implements a QThread for polling the Grid unit for fan rpm and voltage data,
    as well as CPU and GPU temperatures from OpenHardwareMonitor.
"""

import sys
import time

import pythoncom
import wmi
from PyQt5 import QtCore

import grid
import helper
import openhwmon

# Define status icons (available in the resource file built with "pyrcc5"
ICON_RED_LED = ":/icons/led-red-on.png"
ICON_GREEN_LED = ":/icons/green-led-on.png"

class PollingThread(QtCore.QThread):
    """QThread, performs the following:
        - Get fan rpm from Grid
        - Get fan voltage from Grid
        - Get CPU and GPU temperatures from OpenHardwareMonitor"""

    # Signals handling the fan rpm
    rpm_signal_fan1 = QtCore.pyqtSignal(str)
    rpm_signal_fan2 = QtCore.pyqtSignal(str)
    rpm_signal_fan3 = QtCore.pyqtSignal(str)
    rpm_signal_fan4 = QtCore.pyqtSignal(str)
    rpm_signal_fan5 = QtCore.pyqtSignal(str)
    rpm_signal_fan6 = QtCore.pyqtSignal(str)

    # Signals handling the fan voltage
    voltage_signal_fan1 = QtCore.pyqtSignal(str)
    voltage_signal_fan2 = QtCore.pyqtSignal(str)
    voltage_signal_fan3 = QtCore.pyqtSignal(str)
    voltage_signal_fan4 = QtCore.pyqtSignal(str)
    voltage_signal_fan5 = QtCore.pyqtSignal(str)
    voltage_signal_fan6 = QtCore.pyqtSignal(str)

    # Signals handling the pixmap icon (red or green led) indicating the fan status
    pixmap_signal_fan1 = QtCore.pyqtSignal(str)
    pixmap_signal_fan2 = QtCore.pyqtSignal(str)
    pixmap_signal_fan3 = QtCore.pyqtSignal(str)
    pixmap_signal_fan4 = QtCore.pyqtSignal(str)
    pixmap_signal_fan5 = QtCore.pyqtSignal(str)
    pixmap_signal_fan6 = QtCore.pyqtSignal(str)

    # Signals handling CPU and GPU temperatures
    cpu_temp_signal = QtCore.pyqtSignal(int)
    gpu_temp_signal = QtCore.pyqtSignal(int)

    hwmon_status_signal = QtCore.pyqtSignal(str)

    # Signal to indicate fan speed should be updated
    update_signal = QtCore.pyqtSignal()

    # Signal handling exceptions that may occur in the running thread
    exception_signal = QtCore.pyqtSignal(str)

    def __init__(self, polling_interval, ser, lock, cpu_sensor_ids, gpu_sensor_ids, cpu_calc, gpu_calc):
        """ Constructor for the polling thread."""

        super().__init__()

        # "keep_running" controls the while loop in the running thread
        # Initial value is False as the thread is not started yet
        self.keep_running = False

        # Polling interval (ms)
        self.polling_interval = polling_interval

        # Serial device
        self.ser = ser

        # Lock
        self.lock = lock

        # List of CPU and GPU temperature sensors to use
        self.cpu_sensor_ids = cpu_sensor_ids
        self.gpu_sensor_ids = gpu_sensor_ids

        # Defines if CPU and GPU temperatures should be "Maximum" or "Average" from selected sensors
        self.cpu_calc = cpu_calc
        self.gpu_calc = gpu_calc

    def __del__(self):
        self.wait()

    def stop(self):
        """Stop the running thread gracefully."""

        print("Stopping thread...")
        self.keep_running = False

        # Wait for the thread to stop
        self.wait()
        print("Thread stopped")

        # Uninitialize at thread stop (used for WMI in thread)
        pythoncom.CoUninitialize()

    def set_temp_calc(self, cpu_calc, gpu_calc):
        """Setter for cpu and gpu calc parameter."""

        self.cpu_calc = cpu_calc
        self.gpu_calc = gpu_calc

    def update_polling_interval(self, new_polling_interval):
        """Setter for polling interval value."""

        self.polling_interval = new_polling_interval

    def update_sensors(self, cpu_sensor_ids, gpu_sensor_ids):
        """Setter for CPU and GPU sensor id's."""

        self.cpu_sensor_ids = cpu_sensor_ids
        self.gpu_sensor_ids = gpu_sensor_ids

    def calculate_temp(self, temperature_sensors, type):
        """Calculate CPU/GPU temperatures (maximum or average value)"""

        if type == "cpu":
            cpu_temps = []

            # Check if any sensors are configured
            if self.cpu_sensor_ids:
                for id in self.cpu_sensor_ids:
                    for sensor in temperature_sensors:
                        if id == sensor.Identifier:
                            cpu_temps.append(sensor.Value)

                # Convert to float
                cpu_temps_float = [float(i) for i in cpu_temps]

            else:
                cpu_temps_float = [0]

            # Check if temperature values are available
            if cpu_temps_float:
                # Use maximum value
                if self.cpu_calc == "Max":
                    return max(cpu_temps_float)
                # Use average value
                elif self.cpu_calc == "Avg":
                    return (sum(cpu_temps_float) / len(cpu_temps_float))

            # If no temperature values are available, return 0
            else:
                return 0

        elif type == "gpu":
            gpu_temps = []

            # Check if any sensors are configured
            if self.gpu_sensor_ids:
                for id in self.gpu_sensor_ids:
                    for sensor in temperature_sensors:
                        if id == sensor.Identifier:
                            gpu_temps.append(sensor.Value)

                # Convert to float
                gpu_temps_float = [float(i) for i in gpu_temps]

            else:
                gpu_temps_float = [0]

            # Check if temperature values are available
            if gpu_temps_float:
                # Use maximum value
                if self.gpu_calc == "Max":
                    return max(gpu_temps_float)
                # Use average value
                elif self.gpu_calc == "Avg":
                    return (sum(gpu_temps_float) / len(gpu_temps_float))

            # If no temperature values are available, return 0
            else:
                return 0

    def run(self):
        """Main thread processing loop:
            - Poll the Grid for fan rpm and voltage.
            - Poll OpenHardwareMonitor for CPU and GPU temperatures
            - Emit signals:
                - Fan rpm's
                - Fan voltages
                - CPU temperature
                - GPU temperature
                - Update fans
        """

        try:
            print("Starting thread...")

            # CoInitialise() is needed when accessing WMI in a thread
            # CoUninitialize() is called in the stop method
            pythoncom.CoInitialize()

            # A new WMI object is needed in the thread
            hwmon_thread_wmi = wmi.WMI(namespace="root\OpenHardwareMonitor")

            # "keep_running" should be True before starting the while loop
            self.keep_running = True

            # Start the main polling loop
            while self.keep_running:
                # Get current temperature sensors from OpenHardwareMonitor
                temperature_sensors = openhwmon.get_temperature_sensors(hwmon_thread_wmi)

                # Calculate CPU and GPU temperatures
                current_cpu_temp = self.calculate_temp(temperature_sensors, "cpu")
                current_gpu_temp = self.calculate_temp(temperature_sensors, "gpu")

                # Emit temperature signals
                self.cpu_temp_signal.emit(current_cpu_temp)
                self.gpu_temp_signal.emit(current_gpu_temp)

                # If both CPU and GPU temp are 0, set OpenHardwareMonitor status to "Disconnected"
                if current_cpu_temp == current_gpu_temp == 0:
                    self.hwmon_status_signal.emit('<b><font color="red">---</font></b>')
                else:
                    self.hwmon_status_signal.emit('<b><font color="green">Connected</font></b>')

                # Read rpm for all fans
                fans_rpm = grid.read_fan_rpm(self.ser, self.lock)

                # Check if there is fan rpm data available
                if fans_rpm:
                    # Emit rpm signals with current rpm values
                    self.rpm_signal_fan1.emit(str(fans_rpm[0]))
                    self.rpm_signal_fan2.emit(str(fans_rpm[1]))
                    self.rpm_signal_fan3.emit(str(fans_rpm[2]))
                    self.rpm_signal_fan4.emit(str(fans_rpm[3]))
                    self.rpm_signal_fan5.emit(str(fans_rpm[4]))
                    self.rpm_signal_fan6.emit(str(fans_rpm[5]))

                # If no rpm data is available, emit "---" as value
                else:
                    self.rpm_signal_fan1.emit('<b><font color="red">---</font></b>')
                    self.rpm_signal_fan2.emit('<b><font color="red">---</font></b>')
                    self.rpm_signal_fan3.emit('<b><font color="red">---</font></b>')
                    self.rpm_signal_fan4.emit('<b><font color="red">---</font></b>')
                    self.rpm_signal_fan5.emit('<b><font color="red">---</font></b>')
                    self.rpm_signal_fan6.emit('<b><font color="red">---</font></b>')

                # Read voltage for all fans
                fans_voltage = grid.read_fan_voltage(self.ser, self.lock)

                # Check if there is fan voltages data available
                if fans_voltage:
                    # Emit voltage signals with current voltages
                    self.voltage_signal_fan1.emit(str(fans_voltage[0]))
                    self.voltage_signal_fan2.emit(str(fans_voltage[1]))
                    self.voltage_signal_fan3.emit(str(fans_voltage[2]))
                    self.voltage_signal_fan4.emit(str(fans_voltage[3]))
                    self.voltage_signal_fan5.emit(str(fans_voltage[4]))
                    self.voltage_signal_fan6.emit(str(fans_voltage[5]))

                # If no voltage data is available, emit "---" as value
                else:
                    self.voltage_signal_fan1.emit('<b><font color="red">---</font></b>')
                    self.voltage_signal_fan2.emit('<b><font color="red">---</font></b>')
                    self.voltage_signal_fan3.emit('<b><font color="red">---</font></b>')
                    self.voltage_signal_fan4.emit('<b><font color="red">---</font></b>')
                    self.voltage_signal_fan5.emit('<b><font color="red">---</font></b>')
                    self.voltage_signal_fan6.emit('<b><font color="red">---</font></b>')

                # Update status icons
                # Check if rpm and voltage data is available
                if fans_rpm and fans_voltage:
                    # Emit pixmap icon signal (red icon if fan rpm or voltage is 0, otherwise green icon)
                    self.pixmap_signal_fan1.emit(ICON_RED_LED if fans_rpm[0] == 0 or fans_voltage[0] == 0 else ICON_GREEN_LED)
                    self.pixmap_signal_fan2.emit(ICON_RED_LED if fans_rpm[1] == 0 or fans_voltage[1] == 0 else ICON_GREEN_LED)
                    self.pixmap_signal_fan3.emit(ICON_RED_LED if fans_rpm[2] == 0 or fans_voltage[2] == 0 else ICON_GREEN_LED)
                    self.pixmap_signal_fan4.emit(ICON_RED_LED if fans_rpm[3] == 0 or fans_voltage[3] == 0 else ICON_GREEN_LED)
                    self.pixmap_signal_fan5.emit(ICON_RED_LED if fans_rpm[4] == 0 or fans_voltage[4] == 0 else ICON_GREEN_LED)
                    self.pixmap_signal_fan6.emit(ICON_RED_LED if fans_rpm[5] == 0 or fans_voltage[5] == 0 else ICON_GREEN_LED)

                # If no fan rpm or voltage data is available, show the red status icon
                else:
                    self.pixmap_signal_fan1.emit(ICON_RED_LED)
                    self.pixmap_signal_fan2.emit(ICON_RED_LED)
                    self.pixmap_signal_fan3.emit(ICON_RED_LED)
                    self.pixmap_signal_fan4.emit(ICON_RED_LED)
                    self.pixmap_signal_fan5.emit(ICON_RED_LED)
                    self.pixmap_signal_fan6.emit(ICON_RED_LED)

                # Emit update signal
                self.update_signal.emit()

                #print("End of polling loop, sleeping for " + str(self.polling_interval) + " ms")

                # Sleep for the set polling interval (ms)
                time.sleep(self.polling_interval/1000)

        # Emits a signal if an exception occurs in the running thread
        # The main application will then show an error message about the problem
        # This is needed because a new message box widget cannot be created/displayed in the thread
        except Exception as e:
            # Stop the thread
            self.stop()
            print("Thread stopped at exception")

            # Get info about the exception
            (type, value, traceback) = sys.exc_info()

            # Generate a detailed error message
            msg = helper.exception_message_qthread(type, value, traceback)

            # Emit a signal with the error message to be displayed in a message box in the main UI
            self.exception_signal.emit(msg)
