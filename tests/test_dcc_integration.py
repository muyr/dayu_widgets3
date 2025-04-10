"""
Test dayu_widgets integration with DCC applications.
"""

# Import built-in modules
import os

# Import third-party modules
import pytest
from qtpy import QtCore, QtWidgets

# Import local modules
from dayu_widgets.button import MPushButton
from dayu_widgets.label import MLabel
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.menu import MMenu
from dayu_widgets.message import MMessage
from tests.dcc_mocks.dcc_test_utils import DCCType, requires_dcc, skip_in_dcc


def test_basic_widgets_in_current_environment(qtbot, dcc_type):
    """Test that basic widgets work in the current environment."""
    # Create some basic widgets
    button = MPushButton(text="Test Button")
    label = MLabel(text="Test Label")
    line_edit = MLineEdit(text="Test Input")
    
    # Add widgets to qtbot
    qtbot.addWidget(button)
    qtbot.addWidget(label)
    qtbot.addWidget(line_edit)
    
    # Check that widgets have correct properties
    assert button.text() == "Test Button"
    assert label.text() == "Test Label"
    assert line_edit.text() == "Test Input"
    
    # Log the current environment
    print(f"Test running in {dcc_type.name} environment")


@requires_dcc(DCCType.MAYA)
def test_maya_specific_integration(qtbot, dcc_main_window):
    """Test Maya-specific integration."""
    # This test only runs in Maya environment
    assert dcc_main_window is not None
    assert dcc_main_window.objectName() == "MayaWindow"
    
    # Create a widget that would be parented to Maya's main window
    widget = QtWidgets.QWidget(dcc_main_window)
    button = MPushButton(text="Maya Button", parent=widget)
    
    # Add widget to qtbot
    qtbot.addWidget(widget)
    
    # Check that the button has the correct parent chain
    assert button.parent() == widget
    assert widget.parent() == dcc_main_window


@requires_dcc(DCCType.BLENDER)
def test_blender_specific_integration(qtbot, dcc_main_window):
    """Test Blender-specific integration."""
    # This test only runs in Blender environment
    assert dcc_main_window is not None
    assert dcc_main_window.objectName() == "BlenderWindow"
    
    # Create a widget that would be parented to Blender's main window
    widget = QtWidgets.QWidget(dcc_main_window)
    button = MPushButton(text="Blender Button", parent=widget)
    
    # Add widget to qtbot
    qtbot.addWidget(widget)
    
    # Check that the button has the correct parent chain
    assert button.parent() == widget
    assert widget.parent() == dcc_main_window


def test_message_in_dcc(qtbot, dcc_type, dcc_main_window):
    """Test MMessage in DCC environment."""
    # Create a message
    if dcc_main_window:
        # If in a DCC environment, parent to the main window
        MMessage.info(
            title=f"Test in {dcc_type.name}",
            content=f"This is a test message in {dcc_type.name}",
            parent=dcc_main_window
        )
    else:
        # If in standalone, no parent
        MMessage.info(
            title="Test in Standalone",
            content="This is a test message in standalone mode"
        )
    
    # Wait for the message to appear and then disappear
    qtbot.wait(500)


def test_menu_in_dcc(qtbot, dcc_type, dcc_main_window):
    """Test MMenu in DCC environment."""
    # Create a menu
    menu = MMenu(parent=dcc_main_window)
    menu.addAction("Action 1")
    menu.addAction("Action 2")
    menu.addSeparator()
    menu.addAction("Action 3")
    
    # Create a button to show the menu
    button = MPushButton(text="Show Menu", parent=dcc_main_window)
    button.clicked.connect(lambda: menu.exec_(QtCore.QPoint(100, 100)))
    
    # Add widgets to qtbot
    qtbot.addWidget(menu)
    qtbot.addWidget(button)
    
    # Check menu properties
    assert menu.actions()[0].text() == "Action 1"
    assert menu.actions()[1].text() == "Action 2"
    assert menu.actions()[3].text() == "Action 3"
    
    # Log the current environment
    print(f"Menu test running in {dcc_type.name} environment")
