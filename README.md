# Grid Control
Grid Control is a free and open source alternative to the CAM application from NZXT.

<img src="https://github.com/akej74/grid-control/blob/master/screenshots/screenshot_1.png" width="600">

<img src="https://github.com/akej74/grid-control/blob/master/screenshots/screenshot_2.png" width="200">
<img src="https://github.com/akej74/grid-control/blob/master/screenshots/screenshot_3.png" width="200">
<img src="https://github.com/akej74/grid-control/blob/master/screenshots/screenshot_4.png" width="200">

### Highlights
- Simple to use and resource efficient
- Uses OpenHardwareMonitor to read sensor values
- Individual fan control (manual or automatic with control points)
- Support the Grid+ V2 device
- Developed in Python 3 using QT5 for the user interface

### Disclaimer
NZXT is not involved in this project, please do not contact them regarding this application. If you have a question, please open an Issue or send me a message on Reddit. Also, while it seems very unlikely that your hardware could be damaged by this application, I do **NOT** take any responsibility for any damage done to your HW using this software (e.g. overheat due to low fan settings).

### Note about supporting other hardware devices besides the Grid V2
Grid Control only supports the Grid V2 device, no other hardware from NZXT like the different Kraken watercoolers or HUE lightning devices. There are other applications available on GitHub for these devices, please check the NZXT Reddit community for details.

### Stand-alone installation (built with PyInstaller)
Grid Control is available as a stand-alone application (Python does not need to be installed):
- Download the latest release from [Releases](https://github.com/akej74/grid-control/releases)
- Unzip file
- Run "gridcontrol.exe"
- NOTE! At first startup, you will get the message "No data from OpenHardwareMonitor found", even if OHM is running. Just configure the sensor data on the "Sensors" tab, after this the warning will not be displayed.

### Note on saving and loading settings
Grid Control automatically saves all settings when the application is closed ("x" in the top right corner). The settings are stored in the registry at HKEY_CURRENT_USER\Software\GridControl\App\ or HKEY_LOCAL_MACHINE\Software\GridControl\App\

All settings are automatically loaded when Grid Control starts (with default values if no saved settings are found).

### OpenHardwareMonitor / LibreHardwareMonitor
Grid Control uses [OpenHardwareMonitor](https://github.com/openhardwaremonitor/openhardwaremonitor) to get temperature information from the available sensors in the system. 
- Download latest release of OpenHardwareMonitor [here](http://openhardwaremonitor.org/files/openhardwaremonitor-v0.8.0.3-alpha.zip)
- *UPDATE* - There is a fork of OpenHardwareMonitor called **LibreHardwareMonitor**, available [here](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor) that is in active development
- Note that an update to Windows 10 caused problems with OHM and the WMI communication. This can be fixed by a PowerShell command, see [this forum thread](https://forum.rainmeter.net/viewtopic.php?t=19546)

### Driver for the Grid device (not needed for Windows 10)
The Grid uses a MCP2200 USB-to-UART serial converter from [Microchip](http://www.microchip.com/wwwproducts/en/en546923).

Driver installation:
- Windows 10
  - No driver is needed, Windows 10 will detect the Grid device automatically and add a "USB Serial Device" in Device Manager
 
- Windows 7
  - A driver is needed, see "MCP2200/MCP2221 Windows Driver & Installer" on the [product page](http://www.microchip.com/wwwproducts/en/en546923)
 
### Python environment and running the application
Assuming you have latest version of Python 3 installed, the following additional modules are required, install with pip:
- `pip install pyserial`
- `pip install wmi`
- `pip install pypiwin32`
- `pip install pyqt5`

Run `python gridcontrol.py` to start the Grid Control application.

### PyInstaller
For packaging, use PyInstaller:
- `pip install pyinstaller` 
- PyInstaller is used to package the software into EXE format so that you can run the application without having Python installed

### Python IDE
I recommend the free version of PyCharm IDE for Python development.

### Note about "QT Designer"
- For editing the User Interface (`mainwindow.ui`), install QT Designer as follows:
  - Install latest QT5 open source suite from [QT main site](https://www.qt.io/)
  - In the install wizard, make sure you include the "Qt 5.3 MinGW" component
  - QT Designer will be installed in `C:\Qt\5.x\mingw53_32\bin\designer.exe`
  - Note that the executable is named "designer.exe"
- To convert the `mainwindow.ui` to `mainwindow.py`run the following command:
  - `<python installation directory>\Scripts\pyuic5.exe mainwindow.ui -o mainwindow.py`

### Grid simulator
For troubleshooting, or if you would like to run Grid Control without a Grid device, please have a look at my "Grid Simulator" available [here](https://github.com/akej74/grid-simulator).
 
### Inspiration from other projects
I would like to thank the authors of the following projects that have been helpful in understanding the communication protocol the Grid uses.
- [gridfan](https://github.com/CapitalF/gridfan) by CapitalF
- [CamSucks](https://github.com/RoelGo/CamSucks) by RoelGo
- [leviathan](https://github.com/jaksi/leviathan) by jaksi

