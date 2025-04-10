"""
Utility functions for testing dayu_widgets in DCC environments.
"""

# Import built-in modules
import os
import sys
from enum import Enum, auto

# Import third-party modules
import pytest
from qtpy import QtWidgets

# Import local modules
from tests.dcc_mocks import maya_mock, blender_mock


class DCCType(Enum):
    """Enum for DCC application types."""
    STANDALONE = auto()
    MAYA = auto()
    BLENDER = auto()


def get_dcc_type():
    """Get the current DCC type from environment variables."""
    dcc_env = os.environ.get("DAYU_TEST_DCC", "").upper()
    
    if dcc_env == "MAYA":
        return DCCType.MAYA
    elif dcc_env == "BLENDER":
        return DCCType.BLENDER
    else:
        return DCCType.STANDALONE


def setup_dcc_environment():
    """Set up the DCC environment based on the environment variable."""
    dcc_type = get_dcc_type()
    
    if dcc_type == DCCType.MAYA:
        return maya_mock.setup_maya_mock()
    elif dcc_type == DCCType.BLENDER:
        return blender_mock.setup_blender_mock()
    else:
        # For standalone, just return None
        return None


def get_dcc_main_window():
    """Get the main window of the current DCC application."""
    dcc_type = get_dcc_type()
    
    if dcc_type == DCCType.MAYA:
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if widget.objectName() == "MayaWindow":
                return widget
    elif dcc_type == DCCType.BLENDER:
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if widget.objectName() == "BlenderWindow":
                return widget
    
    # For standalone or if no DCC window found
    return None


def requires_dcc(dcc_type):
    """Decorator to skip tests if the required DCC is not available."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_dcc = get_dcc_type()
            if current_dcc != dcc_type:
                pytest.skip(f"Test requires {dcc_type.name} environment")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def skip_in_dcc(dcc_type):
    """Decorator to skip tests in specific DCC environments."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_dcc = get_dcc_type()
            if current_dcc == dcc_type:
                pytest.skip(f"Test skipped in {dcc_type.name} environment")
            return func(*args, **kwargs)
        return wrapper
    return decorator
