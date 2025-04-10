"""
Mock module for Maya environment.
This module simulates the Maya Python API and UI environment for testing.
"""

# Import built-in modules
import os
import sys
from unittest import mock

# Import third-party modules
from qtpy import QtCore, QtWidgets


class MayaMainWindow(QtWidgets.QMainWindow):
    """Mock Maya main window for testing."""
    
    def __init__(self):
        super(MayaMainWindow, self).__init__()
        self.setObjectName("MayaWindow")
        self.setWindowTitle("Maya (Mock)")
        self.resize(1200, 800)


class MayaQtCore:
    """Mock Maya Qt core functionality."""
    
    @staticmethod
    def getMayaWindow():
        """Get the Maya main window instance."""
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if widget.objectName() == "MayaWindow":
                return widget
        
        # Create a new Maya window if none exists
        window = MayaMainWindow()
        return window


class MayaQtUI:
    """Mock Maya UI functionality."""
    
    @staticmethod
    def findControl(control_name):
        """Find a control by name."""
        return None
    
    @staticmethod
    def getMainWindow():
        """Get the Maya main window."""
        return MayaQtCore.getMayaWindow()


class MayaCommandsMock:
    """Mock Maya commands module."""
    
    @staticmethod
    def currentUnit(*args, **kwargs):
        """Mock currentUnit command."""
        return "cm"
    
    @staticmethod
    def workspace(*args, **kwargs):
        """Mock workspace command."""
        return os.path.expanduser("~/maya")
    
    @staticmethod
    def file(*args, **kwargs):
        """Mock file command."""
        if kwargs.get("query", False) and kwargs.get("sceneName", False):
            return "untitled.ma"
        return True


class MayaUtilMock:
    """Mock Maya util module."""
    
    @staticmethod
    def getMayaAppDir():
        """Get Maya application directory."""
        return os.path.expanduser("~/maya")


def setup_maya_mock():
    """Set up Maya mock environment."""
    # Create mock modules
    mock_modules = {
        'maya': mock.MagicMock(),
        'maya.cmds': MayaCommandsMock(),
        'maya.mel': mock.MagicMock(),
        'maya.utils': MayaUtilMock(),
        'maya.OpenMaya': mock.MagicMock(),
        'maya.OpenMayaUI': mock.MagicMock(),
        'maya.api.OpenMaya': mock.MagicMock(),
        'maya.api.OpenMayaUI': mock.MagicMock(),
        'maya.app.general.mayaMixin': mock.MagicMock(),
        'pymel.core': mock.MagicMock(),
        'shiboken2': mock.MagicMock(),
    }
    
    # Add Qt specific modules
    mock_modules['maya.OpenMayaUI'].MQtUtil = MayaQtCore()
    mock_modules['maya.cmds'].currentUnit = MayaCommandsMock.currentUnit
    mock_modules['maya.cmds'].workspace = MayaCommandsMock.workspace
    mock_modules['maya.cmds'].file = MayaCommandsMock.file
    
    # Add the modules to sys.modules
    for name, module in mock_modules.items():
        sys.modules[name] = module
    
    # Set environment variables
    os.environ['MAYA_APP_DIR'] = os.path.expanduser("~/maya")
    os.environ['MAYA_LOCATION'] = os.path.expanduser("~/maya")
    
    # Create a Maya main window
    maya_window = MayaMainWindow()
    maya_window.show()
    
    return maya_window
