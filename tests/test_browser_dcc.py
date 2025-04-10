"""
Test browser components in DCC environments.
"""

# Import built-in modules
import os
import tempfile

# Import third-party modules
import pytest
from qtpy import QtCore

# Import local modules
from dayu_widgets.browser import MClickBrowserFilePushButton, MClickBrowserFolderPushButton
from dayu_widgets.browser import MDragFileButton, MDragFolderButton
from tests.dcc_mocks.dcc_test_utils import DCCType, requires_dcc, skip_in_dcc


def test_browser_file_button_in_current_environment(qtbot, dcc_type):
    """Test file browser button in the current environment."""
    # Create a browser button
    browser_button = MClickBrowserFilePushButton(text="Browse File")
    
    # Add widget to qtbot
    qtbot.addWidget(browser_button)
    
    # Set some properties
    browser_button.set_dayu_filters([".txt", ".py"])
    browser_button.set_dayu_path(os.path.expanduser("~"))
    
    # Check properties
    assert browser_button.get_dayu_filters() == [".txt", ".py"]
    assert browser_button.get_dayu_path() == os.path.expanduser("~")
    
    # Log the current environment
    print(f"File browser test running in {dcc_type.name} environment")


def test_browser_folder_button_in_current_environment(qtbot, dcc_type):
    """Test folder browser button in the current environment."""
    # Create a browser button
    browser_button = MClickBrowserFolderPushButton(text="Browse Folder")
    
    # Add widget to qtbot
    qtbot.addWidget(browser_button)
    
    # Set some properties
    browser_button.set_dayu_path(os.path.expanduser("~"))
    
    # Check properties
    assert browser_button.get_dayu_path() == os.path.expanduser("~")
    
    # Log the current environment
    print(f"Folder browser test running in {dcc_type.name} environment")


@requires_dcc(DCCType.MAYA)
def test_browser_in_maya(qtbot, dcc_main_window):
    """Test browser components in Maya environment."""
    # This test only runs in Maya environment
    assert dcc_main_window is not None
    assert dcc_main_window.objectName() == "MayaWindow"
    
    # Create browser buttons
    file_button = MClickBrowserFilePushButton(text="Maya File", parent=dcc_main_window)
    folder_button = MClickBrowserFolderPushButton(text="Maya Folder", parent=dcc_main_window)
    
    # Add widgets to qtbot
    qtbot.addWidget(file_button)
    qtbot.addWidget(folder_button)
    
    # Check parent chain
    assert file_button.parent() == dcc_main_window
    assert folder_button.parent() == dcc_main_window
    
    # Set Maya-specific paths
    maya_dir = os.path.expanduser("~/maya")
    file_button.set_dayu_path(maya_dir)
    folder_button.set_dayu_path(maya_dir)
    
    # Check paths
    assert file_button.get_dayu_path() == maya_dir
    assert folder_button.get_dayu_path() == maya_dir


@requires_dcc(DCCType.BLENDER)
def test_browser_in_blender(qtbot, dcc_main_window):
    """Test browser components in Blender environment."""
    # This test only runs in Blender environment
    assert dcc_main_window is not None
    assert dcc_main_window.objectName() == "BlenderWindow"
    
    # Create browser buttons
    file_button = MClickBrowserFilePushButton(text="Blender File", parent=dcc_main_window)
    folder_button = MClickBrowserFolderPushButton(text="Blender Folder", parent=dcc_main_window)
    
    # Add widgets to qtbot
    qtbot.addWidget(file_button)
    qtbot.addWidget(folder_button)
    
    # Check parent chain
    assert file_button.parent() == dcc_main_window
    assert folder_button.parent() == dcc_main_window
    
    # Set Blender-specific paths
    blender_dir = os.path.expanduser("~/blender")
    file_button.set_dayu_path(blender_dir)
    folder_button.set_dayu_path(blender_dir)
    
    # Check paths
    assert file_button.get_dayu_path() == blender_dir
    assert folder_button.get_dayu_path() == blender_dir


def test_drag_file_button(qtbot, dcc_type, monkeypatch):
    """Test drag file button in the current environment."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
        temp_file.write(b"Test content")
        temp_path = temp_file.name
    
    try:
        # Create a drag file button
        drag_button = MDragFileButton(text="Drag File")
        
        # Add widget to qtbot
        qtbot.addWidget(drag_button)
        
        # Set properties
        drag_button.set_dayu_filters([".txt"])
        
        # Check properties
        assert drag_button.get_dayu_filters() == [".txt"]
        
        # Mock the drag and drop event
        # This is a simplified simulation since actual drag and drop is hard to test
        def mock_get_valid_file_list(self, urls):
            return [temp_path]
        
        # Patch the method
        monkeypatch.setattr(MDragFileButton, "_get_valid_file_list", mock_get_valid_file_list)
        
        # Create a signal spy
        spy = QtCore.QSignalSpy(drag_button.sig_file_changed)
        
        # Simulate drop event
        mime_data = QtCore.QMimeData()
        mime_data.setUrls([QtCore.QUrl.fromLocalFile(temp_path)])
        
        drop_event = QtGui.QDropEvent(
            QtCore.QPoint(10, 10),
            QtCore.Qt.CopyAction,
            mime_data,
            QtCore.Qt.LeftButton,
            QtCore.Qt.NoModifier
        )
        
        drag_button.dropEvent(drop_event)
        
        # Check signal emission
        assert len(spy) == 1
        assert spy[0][0] == temp_path
        
        # Log the current environment
        print(f"Drag file test running in {dcc_type.name} environment")
    
    finally:
        # Clean up
        os.unlink(temp_path)
