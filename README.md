# Grid Control
Grid Control is a free and open source alternative to the CAM application from NZXT.

<img src="https://github.com/akej74/grid-control/blob/master/screenshots/screenshot_1.png" width="600">

<img src="https://github.com/akej74/grid-control/blob/master/screenshots/screenshot_2.png" width="200">
<img src="https://github.com/akej74/grid-control/blob/master/screenshots/screenshot_3.png" width="200">
<img src="https://github.com/akej74/grid-control/blob/master/screenshots/screenshot_4.png" width="200">

### Highlights
- Simple to use and resource efficient
- Written in Python 3 using QT5 for the user interface
- Uses OpenHardwareMonitor to read sensor values
- Individual fan control (manual or automatic with control points) 

### Stand-alone installation
Grid Control is available as a stand-alone application (Python does not need to be installed):
- Download the latest release from [Releases](https://github.com/akej74/grid-control/releases)
- Unzip file
- Run "gridcontrol.exe"

### OpenHardwareMonitor
Grid Control uses [OpenHardwareMonitor](https://github.com/openhardwaremonitor/openhardwaremonitor) to get temperature information from the available sensors in the system.
- Download latest release of OpenHardwareMonitor [here](http://openhardwaremonitor.org/files/openhardwaremonitor-v0.7.1.5-alpha.zip)

### Driver for the Grid device
The Grid uses a MCP2200 USB-to-UART serial converter from [Microchip](http://www.microchip.com/wwwproducts/en/en546923).

Driver installation:
- Windows 10
 - No driver is needed, Windows 10 will detect the Grid device automatically and add a "USB Serial Device" in Device Manager
 
- Windows 7
 - A driver is needed, see "MCP2200/MCP2221 Windows Driver & Installer" on the [product page](http://www.microchip.com/wwwproducts/en/en546923)
 
### Python environment
Assuming you have Python 3 installed, the following attitional modules are required (can be installed with "pip").
- pip install pyserial
- pip install wmi
- pip install pypiwin32
- pip install pyqt5

### Grid simulator
For troubleshooting, or if you would like to run Grid Control without a Grid device, please have a look at my grid simulator available [here](https://github.com/akej74/grid-simulator).
 
 
