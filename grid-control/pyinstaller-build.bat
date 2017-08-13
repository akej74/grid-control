REM packages grid-control into dist\gridcontrol

pyinstaller --noconsole --noconfirm --uac-admin gridcontrol.py

REM copy LHM/OHM to dist\gridcontrol\ohm

xcopy ohm dist\gridcontrol\ohm\ /S /Y