"""
Pytest configuration file for dayu_widgets tests.
"""

# Import built-in modules
import os
import sys

# Import third-party modules
import pytest
from qtpy import QtWidgets

# Import local modules
from tests.dcc_mocks.dcc_test_utils import setup_dcc_environment, get_dcc_main_window, DCCType, get_dcc_type


@pytest.fixture(scope="session", autouse=True)
def setup_dcc():
    """Set up the DCC environment for testing."""
    # Set up the DCC environment
    dcc_window = setup_dcc_environment()
    
    # Yield to allow tests to run
    yield dcc_window
    
    # Clean up (if needed)
    if dcc_window:
        dcc_window.close()


@pytest.fixture
def dcc_main_window():
    """Get the main window of the current DCC application."""
    return get_dcc_main_window()


@pytest.fixture
def dcc_type():
    """Get the current DCC type."""
    return get_dcc_type()


@pytest.fixture
def is_maya():
    """Check if the current environment is Maya."""
    return get_dcc_type() == DCCType.MAYA


@pytest.fixture
def is_blender():
    """Check if the current environment is Blender."""
    return get_dcc_type() == DCCType.BLENDER


@pytest.fixture
def is_standalone():
    """Check if the current environment is standalone."""
    return get_dcc_type() == DCCType.STANDALONE
