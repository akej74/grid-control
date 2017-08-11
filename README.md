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
- Support the Grid+ V2 device

### Disclaimer
NZXT is not involved in this project, do not contact them if your device is damaged while using this software.

Also, while it doesn't seem like the hardware could be damaged by silly USB messages (apart from overheating), I do **NOT** take any responsibility for any damage done to your cooler (applies to the Kraken watercooler, currently disabled).

### Experimental Kraken X61 support - (not applicable as Kraken support is disabled for now)
Release 1.0.3 adds experimental support for the Kraken X61 cooler. This requires the [LibUSB](http://libusb.info/) library to be installed, see next chapter.

### LibUSB installation - (not applicable as Kraken support is disabled for now)
1. To be able to communicate whith the Kraken X61 USB device, you need to download pre-compiled LibUSB DLL's from [here](https://sourceforge.net/projects/libusb/files/libusb-1.0/libusb-1.0.20/libusb-1.0.20.7z/download)
2. Unzip the archive
3. Assuming you are using a **64 bit** version of Windows:
 - Copy ...\libusb-1.0.20\MS32\dll\libusb-1.0.dll to C:\Windows\SysWOW64
 - Copy ...\libusb-1.0.20\MS64\dll\libusb-1.0.dll to C:\Windows\System32
 - Yes, the 64-bit DLL should be copied to "System32", and the 32-bit version to "SysWOW64" :-)

### Stand-alone installation
Grid Control is available as a stand-alone application (Python does not need to be installed):
- Download the latest release from [Releases](https://github.com/akej74/grid-control/releases)
- Unzip file
- Run "gridcontrol.exe"

### OpenHardwareMonitor (REQUIRED IN THIS FORK)
Grid Control uses [OpenHardwareMonitor](https://github.com/openhardwaremonitor/openhardwaremonitor) to get temperature information from the available sensors in the system. Grid-Control AUTOMATICALLY launches a new OHM process if none exist. The OHM process is optionally terminated according to user preference.

- Download latest release of OpenHardwareMonitor [here](http://openhardwaremonitor.org/files/openhardwaremonitor-v0.8.0-beta.zip)
- You must place the binaries directly into the ./grid-control/ohm/ directory. The OHM executable must be named "OpenHardwareMonitor.exe"

NOTE: Build 0.7.1 and 0.8 did not work on my machine. I built a more updated fork of OHM called LibreHardwareMonitor [here](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor)

### Driver for the Grid device
The Grid uses a MCP2200 USB-to-UART serial converter from [Microchip](http://www.microchip.com/wwwproducts/en/en546923).

Driver installation:
- Windows 10
 - No driver is needed, Windows 10 will detect the Grid device automatically and add a "USB Serial Device" in Device Manager
 
- Windows 7
 - A driver is needed, see "MCP2200/MCP2221 Windows Driver & Installer" on the [product page](http://www.microchip.com/wwwproducts/en/en546923)
 
### Python environment
Assuming you have Python 3.5 installed, the following additional modules are required (can be installed with "pip").
- pip install pyserial
- pip install wmi
- pip install pypiwin32
- pip install pyqt5
- pip install install pyinstaller (For python 3.6+, you will need the unstable dev version of pyinstaller)
- pip install pyusb

### QT Creator
QT Creator (including QT Designer for UI design) can be downloaded [here](https://www.qt.io/download-open-source/).
You need to convert the mainwindow.ui to mainwindow.py (because of PyQt5). This is taken care of my executing pyinstaller-build.bat

NOTE: It is used strictly for editing the ui/mainwindow.ui file directly. It is not necessary to create a QT Project.

### Packaging
PyInstaller is used to package the software into EXE format so that you dont have to call "python gridcontrol.py"

Run pyinstaller-build.bat to package the software.

### PyCharm (OPTIONAL)
The latest version of PyCharm Community edition was used because it is a fantastic IDE.
I used the ./grid-control/ directory as the root for the project.

### Grid simulator
For troubleshooting, or if you would like to run Grid Control without a Grid device, please have a look at the original grid simulator available [here](https://github.com/akej74/grid-simulator).
 
### Inspiration from other projects
I would like to thank the authors of the following projects that have been helpful in understanding the communication protocol the Grid and Kraken X61 uses.
- [gridfan](https://github.com/CapitalF/gridfan) by CapitalF
- [CamSucks](https://github.com/RoelGo/CamSucks) by RoelGo
- [leviathan](https://github.com/jaksi/leviathan) by jaksi

