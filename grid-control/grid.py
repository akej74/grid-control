"""
    grid.py
    -------
    Implements serial communication with the Grid+ V2 unit,
    e.g. "initalization", "set fan voltage", "read fan voltage", "read fan rpm".
"""

import sys
import time

import serial
from serial.tools import list_ports

import helper

# Time (s) to wait until reading data from Grid after a request (s)
WAIT_GRID = 0.04

def get_serial_ports():
    """Returns a list of all serial ports found, e.g. 'COM1' in Windows"""
    return sorted([port.device for port in list_ports.comports()])

def setup_serial(ser, port, lock):
    """Setup all parameters for the serial communication"""
    try:
        with lock:
            ser.baudrate = 4800
            ser.port = port
            ser.bytesize = serial.EIGHTBITS
            ser.stopbits = serial.STOPBITS_ONE
            ser.parity = serial.PARITY_NONE
            ser.timeout = 0.1  # Read timeout in seconds
            ser.write_timeout = 0.1  # Write timeout in seconds
    except Exception as e:
        helper.show_error("Problem initializing serial port " + port + ".\n\n"
                          "Exception:\n" + str(e) + "\n\n"
                          "The application will now exit.")
        sys.exit(0)

def open_serial(ser, lock):
    """Open the serial port"""
    try:
        with lock:
            ser.open()
    except Exception as e:
        helper.show_error("Could not open serial port " + ser.port + ".\n\n"
                          "Is another instance of Grid Control running?\n\n"
                          "Exception:\n" + str(e) + "\n\n"
                          "The application will now exit.")
        sys.exit(0)

def initialize_grid(ser, lock):
    """Initialize the Grid by sending "0xC0", expected response is "0x21"

    Returns:
        - True for successful initialization
        - False otherwise
    """

    try:
        with lock:
            # Flush input and output buffers
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            # Write data to serial port to initialize the Grid
            bytes_written = ser.write(serial.to_bytes([0xC0]))

            # Wait before checking response
            time.sleep(WAIT_GRID)

            # Read response, one byte = 0x21 is expected for a successful initialization
            response = ser.read(size=1)

            # Check if the Grid responded with any data
            if response:
                # Check for correct response (should be 0x21)
                if response[0] == int("0x21", 16):
                    print("Grid initialized")
                    return True

                # Incorrect response received from the grid
                else:
                    helper.show_error("Problem initializing the Grid unit.\n\n"
                                      "Response 0x21 expected, got " + hex(ord(response)) + ".\n\n"
                                      "Please check serial port " + ser.port +".\n")
                    return False

            # In case no response (0 bytes) from the Grid
            else:
                helper.show_error("Problem initializing the Grid unit.\n\n"
                                  "Response 0x21 expected, no response received.\n\n"
                                   "Please check serial port " + ser.port +".\n")
                return False

    except Exception as e:
            helper.show_error("Problem initializing the Grid unit.\n\n"
                              "Exception:\n" + str(e) + "\n\n"
                              "The application will now exit.")
            sys.exit(0)


def set_fan(ser, fan, voltage, lock):
    """Sets voltage of a specific fan.
    Note:
        The Grid only supports voltages between 4.0V and 12.0V in 0.5V steps (e.g. 4.0, 7.5. 12.0)
        Configuring "0V" stops a fan.
    """

    # Valid voltages and corresponding data (two bytes)
    speed_data = {0:    [0x00, 0x00],  # 0%     (Values below 4V is not supported by the Grid, fans will be stopped)
                  4.0:  [0x04, 0x00],  # 33.3%  (4.0V)
                  4.5:  [0x04, 0x50],  # 37.5%  (4.5V)
                  5.0:  [0x05, 0x00],  # 41.7%  (5V)
                  5.5:  [0x05, 0x50],  # 45.8%  (5.5V)
                  6.0:  [0x06, 0x00],  # 50.0%  (6V)
                  6.5:  [0x06, 0x50],  # 54.2%  (6.5V)
                  7.0:  [0x07, 0x00],  # 58.3%  (7V)
                  7.5:  [0x07, 0x50],  # 62.5%  (7.5V)
                  8.0:  [0x08, 0x00],  # 66.7%  (8V)
                  8.5:  [0x08, 0x50],  # 70.1%  (8.5V)
                  9.0:  [0x09, 0x00],  # 75.0%  (9.0V)
                  9.5:  [0x09, 0x50],  # 79.2%  (9.5V)
                  10.0: [0x0A, 0x00],  # 83.3%  (10.0V)
                  10.5: [0x0A, 0x50],  # 87.5%  (10.5V)
                  11.0: [0x0B, 0x00],  # 91.7%  (11.0V)
                  11.5: [0x0B, 0x50],  # 95.8%  (11.5V)
                  12.0: [0x0C, 0x00]}  # 100.0% (12.0V)

    fan_data = {1: 0x01,  # Fan 1
                2: 0x02,  # Fan 2
                3: 0x03,  # Fan 3
                4: 0x04,  # Fan 4
                5: 0x05,  # Fan 5
                6: 0x06}  # Fan 6

    # Define bytes to be sent to the Grid for configuring a specific fan's voltage
    # Format is seven bytes:
    # 44 <fan id> C0 00 00 <voltage integer> <voltage decimal>
    #
    # Example configuring "7.5V" for fan "1":
    # 44 01 C0 00 00 07 50
    serial_data = [0x44, fan_data[fan], 0xC0, 0x00, 0x00, speed_data[voltage][0], speed_data[voltage][1]]

    try:
        with lock:
            bytes_written = ser.write(serial.to_bytes(serial_data))
            time.sleep(WAIT_GRID)

            # TODO: Check reponse
            # Expected response is one byte
            response = ser.read(size=1)
            print("Fan " + str(fan) + " updated")
    except Exception as e:
        helper.show_error("Could not set speed for fan " + str(fan) + ".\n\n"
                          "Please check settings for serial port " + str(ser.port) + ".\n\n"
                          "Exception:\n" + str(e) + "\n\n"
                          "The application will now exit.")
        sys.exit(0)

def read_fan_rpm(ser, lock):
    """Reads the current rpm of each fan.
    Returns:
        - If success: A list with rpm data for each fan
        - If failure to read data: An empty list
    """

    # List to hold fan rpm data to be returned
    fans = []

    with lock:
        for fan in [0x01, 0x02, 0x03, 0x04, 0x05, 0x06]:
            try:
                # Define bytes to be sent to the Grid for reading rpm for a specific fan
                # Format is two bytes:
                # 8A <fan id>
                serial_data = [0x8A, fan]

                ser.reset_output_buffer()
                # TODO: Check bytes written
                bytes_written = ser.write(serial.to_bytes(serial_data))

                # Wait before checking response
                time.sleep(WAIT_GRID)

                # Expected response is 5 bytes
                # Example response: C0 00 00 03 00 = 0x0300 = 768 rpm (two bytes unsigned)
                response = ser.read(size=5)

                # Check if the Grid responded with any data
                if response:
                    # Check for correct response, first three bytes should be C0 00 00
                    if response[0] == int("0xC0", 16) and response[1] == response[2] == int("0x00", 16):
                        # Convert rpm from 2-bytes unsigned value to decimal
                        rpm = response[3] * 256 + response[4]
                        fans.append(rpm)

                    # An incorrect response was received, return an empty list
                    else:
                        return []

                # In case no response (0 bytes) received, return an empty list
                else:
                    return []

            except Exception as e:
                helper.show_error("Could not read rpm for fan " + str(fan) + ".\n\n"
                                  "Please check serial port settings.\n\n"
                                  "Exception:\n" + str(e) + "\n\n"
                                  "The application will now exit.")
                print(str(e))
                sys.exit(0)

        # Fan
        return fans

def read_fan_voltage(ser, lock):
    """Reads the current voltage of each fan.

    Returns:
        - If success: a list with voltage data for each fan
        - If failure to read data: An empty list
    """

    # List to hold fan voltage data to be returned
    fans = []

    with lock:
        for fan in [0x01, 0x02, 0x03, 0x04, 0x05, 0x06]:
            try:
                # Define bytes to be sent to the Grid for reading voltage for a specific fan
                # Format is two bytes, e.g. [0x84, <fan id>]
                serial_data = [0x84, fan]

                ser.reset_output_buffer()
                bytes_written = ser.write(serial.to_bytes(serial_data))

                # Wait before checking response
                time.sleep(WAIT_GRID)

                # Expected response is 5 bytes
                # Example response: 00 00 00 0B 01 = 0x0B 0x01 = 11.01 volt
                response = ser.read(size=5)

                # Check if the Grid responded with any data
                if response:
                    # Check for correct response (first three bytes should be 0x00)
                    if response[0] == int("0xC0", 16) and response[1] == response[2] == int("0x00", 16):
                        # Convert last two bytes to a decimal float value
                        voltage = float(str(response[3]) + "." + str(response[4]))
                        # Add the voltage for the current fan to the list
                        fans.append(voltage)

                    # An incorrect response was received
                    else:
                        print("Error reading fan voltage, incorrect response")
                        return []

                # In case no response (0 bytes) is returned from the Grid
                else:
                    print("Error reading fan voltage, no data returned")
                    return []

            except Exception as e:
                helper.show_error("Could not read fan voltage.\n\n"
                                  "Please check serial port " + ser.port + ".\n\n"
                                  "Exception:\n" + str(e) + "\n\n"
                                  "The application will now exit.")
                print(str(e))
                sys.exit(0)

        return fans


def calculate_voltage(percent):
    """Convert fan speed in percent (0-100) to nearest valid voltage (4.0V to 12.0V in steps of 0.5V).
    Values below 33% will be defined as "0V" (fan will be stopped).
    """

    if percent < 33:
        return 0.0
    elif percent >= 33 and percent < 36:
        return 4.0
    elif percent >= 36 and percent < 40:
        return 4.5
    elif percent >= 40 and percent < 44:
        return 5.0
    elif percent >= 44 and percent < 48:
        return 5.5
    elif percent >= 48 and percent < 52:
        return 6.0
    elif percent >= 52 and percent < 56:
        return 6.5
    elif percent >= 56 and percent < 60:
        return 7.0
    elif percent >= 60 and percent < 64:
        return 7.5
    elif percent >= 64 and percent < 68:
        return 8.0
    elif percent >= 68 and percent < 72:
        return 8.5
    elif percent >= 72 and percent < 76:
        return 9.0
    elif percent >= 76 and percent < 80:
        return 9.5
    elif percent >= 80 and percent < 84:
        return 10.0
    elif percent >= 84 and percent < 88:
        return 10.5
    elif percent >= 88 and percent < 93:
        return 11.0
    elif percent >= 93 and percent < 98:
        return 11.5
    else:
        return 12.0

