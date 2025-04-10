"""
Test button group components in DCC environments.
"""

# Import built-in modules
import os

# Import third-party modules
import pytest
from qtpy import QtCore

# Import local modules
from dayu_widgets.button_group import MPushButtonGroup, MCheckBoxGroup, MRadioButtonGroup, MToolButtonGroup
from tests.dcc_mocks.dcc_test_utils import DCCType, requires_dcc, skip_in_dcc


def test_push_button_group_in_current_environment(qtbot, dcc_type):
    """Test push button group in the current environment."""
    # Create a button group
    button_group = MPushButtonGroup()
    
    # Add buttons
    button_group.set_button_list([
        {"text": "Button 1", "clicked": lambda: print("Button 1 clicked")},
        {"text": "Button 2", "clicked": lambda: print("Button 2 clicked")},
        {"text": "Button 3", "clicked": lambda: print("Button 3 clicked")}
    ])
    
    # Add widget to qtbot
    qtbot.addWidget(button_group)
    
    # Check button count
    assert len(button_group.get_button_group().buttons()) == 3
    
    # Check button texts
    buttons = button_group.get_button_group().buttons()
    assert buttons[0].text() == "Button 1"
    assert buttons[1].text() == "Button 2"
    assert buttons[2].text() == "Button 3"
    
    # Log the current environment
    print(f"Push button group test running in {dcc_type.name} environment")


def test_checkbox_group_in_current_environment(qtbot, dcc_type):
    """Test checkbox group in the current environment."""
    # Create a checkbox group
    checkbox_group = MCheckBoxGroup()
    
    # Add checkboxes
    checkbox_group.set_button_list([
        {"text": "Option 1"},
        {"text": "Option 2"},
        {"text": "Option 3"}
    ])
    
    # Add widget to qtbot
    qtbot.addWidget(checkbox_group)
    
    # Check checkbox count
    assert len(checkbox_group.get_button_group().buttons()) == 3
    
    # Check checkbox texts
    checkboxes = checkbox_group.get_button_group().buttons()
    assert checkboxes[0].text() == "Option 1"
    assert checkboxes[1].text() == "Option 2"
    assert checkboxes[2].text() == "Option 3"
    
    # Set checked items
    checkbox_group.set_dayu_checked(["Option 1", "Option 3"])
    
    # Check checked items
    assert checkbox_group.get_dayu_checked() == ["Option 1", "Option 3"]
    assert checkboxes[0].isChecked() == True
    assert checkboxes[1].isChecked() == False
    assert checkboxes[2].isChecked() == True
    
    # Log the current environment
    print(f"Checkbox group test running in {dcc_type.name} environment")


def test_radio_button_group_in_current_environment(qtbot, dcc_type):
    """Test radio button group in the current environment."""
    # Create a radio button group
    radio_group = MRadioButtonGroup()
    
    # Add radio buttons
    radio_group.set_button_list([
        {"text": "Option 1"},
        {"text": "Option 2"},
        {"text": "Option 3"}
    ])
    
    # Add widget to qtbot
    qtbot.addWidget(radio_group)
    
    # Check radio button count
    assert len(radio_group.get_button_group().buttons()) == 3
    
    # Check radio button texts
    radio_buttons = radio_group.get_button_group().buttons()
    assert radio_buttons[0].text() == "Option 1"
    assert radio_buttons[1].text() == "Option 2"
    assert radio_buttons[2].text() == "Option 3"
    
    # Set checked item
    radio_group.set_dayu_checked(1)  # Index 1 (Option 2)
    
    # Check checked item
    assert radio_group.get_dayu_checked() == 1
    assert radio_buttons[0].isChecked() == False
    assert radio_buttons[1].isChecked() == True
    assert radio_buttons[2].isChecked() == False
    
    # Log the current environment
    print(f"Radio button group test running in {dcc_type.name} environment")


@requires_dcc(DCCType.MAYA)
def test_button_groups_in_maya(qtbot, dcc_main_window):
    """Test button groups in Maya environment."""
    # This test only runs in Maya environment
    assert dcc_main_window is not None
    assert dcc_main_window.objectName() == "MayaWindow"
    
    # Create button groups
    push_group = MPushButtonGroup(parent=dcc_main_window)
    check_group = MCheckBoxGroup(parent=dcc_main_window)
    radio_group = MRadioButtonGroup(parent=dcc_main_window)
    
    # Add buttons
    push_group.set_button_list([
        {"text": "Maya Button 1"},
        {"text": "Maya Button 2"}
    ])
    
    check_group.set_button_list([
        {"text": "Maya Check 1"},
        {"text": "Maya Check 2"}
    ])
    
    radio_group.set_button_list([
        {"text": "Maya Radio 1"},
        {"text": "Maya Radio 2"}
    ])
    
    # Add widgets to qtbot
    qtbot.addWidget(push_group)
    qtbot.addWidget(check_group)
    qtbot.addWidget(radio_group)
    
    # Check parent chain
    assert push_group.parent() == dcc_main_window
    assert check_group.parent() == dcc_main_window
    assert radio_group.parent() == dcc_main_window
    
    # Check button texts
    assert push_group.get_button_group().buttons()[0].text() == "Maya Button 1"
    assert check_group.get_button_group().buttons()[0].text() == "Maya Check 1"
    assert radio_group.get_button_group().buttons()[0].text() == "Maya Radio 1"


@requires_dcc(DCCType.BLENDER)
def test_button_groups_in_blender(qtbot, dcc_main_window):
    """Test button groups in Blender environment."""
    # This test only runs in Blender environment
    assert dcc_main_window is not None
    assert dcc_main_window.objectName() == "BlenderWindow"
    
    # Create button groups
    push_group = MPushButtonGroup(parent=dcc_main_window)
    check_group = MCheckBoxGroup(parent=dcc_main_window)
    radio_group = MRadioButtonGroup(parent=dcc_main_window)
    
    # Add buttons
    push_group.set_button_list([
        {"text": "Blender Button 1"},
        {"text": "Blender Button 2"}
    ])
    
    check_group.set_button_list([
        {"text": "Blender Check 1"},
        {"text": "Blender Check 2"}
    ])
    
    radio_group.set_button_list([
        {"text": "Blender Radio 1"},
        {"text": "Blender Radio 2"}
    ])
    
    # Add widgets to qtbot
    qtbot.addWidget(push_group)
    qtbot.addWidget(check_group)
    qtbot.addWidget(radio_group)
    
    # Check parent chain
    assert push_group.parent() == dcc_main_window
    assert check_group.parent() == dcc_main_window
    assert radio_group.parent() == dcc_main_window
    
    # Check button texts
    assert push_group.get_button_group().buttons()[0].text() == "Blender Button 1"
    assert check_group.get_button_group().buttons()[0].text() == "Blender Check 1"
    assert radio_group.get_button_group().buttons()[0].text() == "Blender Radio 1"
