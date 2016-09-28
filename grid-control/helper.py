"""
    helper.py
    ---------
    Implements various helper functions, e.g. to display messages using a QT Message box.
"""

import io
import sys
import traceback

from PyQt5 import QtCore, QtWidgets, QtGui


def excepthook(excType, excValue, tracebackobj):
    """Rewritten "excepthook" function, to display a message box with details about the exception.

    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    separator = '-' * 40
    notice = "An unhandled exception has occurred\n"

    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    sections = [separator, errmsg, separator, tbinfo]
    msg = '\n'.join(sections)

    # Create a QMessagebox
    error_box = QtWidgets.QMessageBox()

    error_box.setText(str(notice)+str(msg))
    error_box.setWindowTitle("Grid Control - unhandled exception")
    error_box.setIcon(QtWidgets.QMessageBox.Critical)
    error_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    error_box.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

    # Show the window
    error_box.exec_()
    sys.exit(1)

def exception_message_qthread(excType, excValue, tracebackobj):
    """Display an error message box with the exception details."""

    separator = '-' * 40
    notice = "An exception occurred in the polling thread!\n"

    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    sections = [notice, separator, errmsg, separator, tbinfo]
    msg = '\n'.join(sections)

    return msg

def show_error(message):
    """Display "message" in a "Critical error" message box with 'OK' button."""

    # Create a QMessagebox
    message_box = QtWidgets.QMessageBox()

    message_box.setText(message)
    message_box.setWindowTitle("Error")
    message_box.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/grid.png")))
    message_box.setIcon(QtWidgets.QMessageBox.Critical)
    message_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    message_box.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

    #Show the window
    message_box.exec_()

def show_notification(message):
    """Display "message" in a "Information" message box with 'OK' button."""

    # Create a QMessagebox
    message_box = QtWidgets.QMessageBox()

    message_box.setText(message)
    message_box.setWindowTitle("Note")
    message_box.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/grid.png")))
    message_box.setIcon(QtWidgets.QMessageBox.Information)
    message_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    message_box.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

    #Show the window
    message_box.exec_()