"""
Mock module for Blender environment.
This module simulates the Blender Python API and UI environment for testing.
"""

# Import built-in modules
import os
import sys
from unittest import mock

# Import third-party modules
from qtpy import QtCore, QtWidgets


class BlenderMainWindow(QtWidgets.QMainWindow):
    """Mock Blender main window for testing."""
    
    def __init__(self):
        super(BlenderMainWindow, self).__init__()
        self.setObjectName("BlenderWindow")
        self.setWindowTitle("Blender (Mock)")
        self.resize(1200, 800)


class BlenderContext:
    """Mock Blender context."""
    
    def __init__(self):
        self.scene = BlenderScene()
        self.window = BlenderMainWindow()
        self.area = mock.MagicMock()
        self.region = mock.MagicMock()
        self.space_data = mock.MagicMock()
        self.screen = mock.MagicMock()


class BlenderScene:
    """Mock Blender scene."""
    
    def __init__(self):
        self.objects = BlenderCollection()
        self.collection = BlenderCollection()
        self.frame_current = 1
        self.frame_start = 1
        self.frame_end = 250
        self.render = mock.MagicMock()
        self.render.fps = 24
        self.render.resolution_x = 1920
        self.render.resolution_y = 1080


class BlenderCollection:
    """Mock Blender collection."""
    
    def __init__(self):
        self._items = {}
    
    def __iter__(self):
        return iter(self._items.values())
    
    def __getitem__(self, key):
        return self._items.get(key)
    
    def __len__(self):
        return len(self._items)


class BlenderOperator:
    """Mock Blender operator."""
    
    def __init__(self, name):
        self.name = name
    
    def poll(self, context):
        return True
    
    def execute(self, context):
        return {'FINISHED'}


class BlenderData:
    """Mock Blender data."""
    
    def __init__(self):
        self.objects = BlenderCollection()
        self.materials = BlenderCollection()
        self.meshes = BlenderCollection()
        self.scenes = BlenderCollection()


class BlenderBpy:
    """Mock Blender bpy module."""
    
    def __init__(self):
        self.context = BlenderContext()
        self.data = BlenderData()
        self.ops = mock.MagicMock()
        self.types = mock.MagicMock()
        self.utils = mock.MagicMock()
        self.path = mock.MagicMock()
        
        # Set up path methods
        self.path.abspath = lambda path: os.path.abspath(path)
        self.path.basename = lambda path: os.path.basename(path)
        self.path.dirname = lambda path: os.path.dirname(path)
        self.path.join = lambda *paths: os.path.join(*paths)
        self.path.exists = lambda path: os.path.exists(path)
        self.path.user_resource = lambda resource_type, path="": os.path.join(os.path.expanduser("~/blender"), path)


def setup_blender_mock():
    """Set up Blender mock environment."""
    # Create mock modules
    mock_bpy = BlenderBpy()
    
    mock_modules = {
        'bpy': mock_bpy,
        'bpy.context': mock_bpy.context,
        'bpy.data': mock_bpy.data,
        'bpy.ops': mock_bpy.ops,
        'bpy.types': mock_bpy.types,
        'bpy.utils': mock_bpy.utils,
        'bpy.path': mock_bpy.path,
        'bgl': mock.MagicMock(),
        'blf': mock.MagicMock(),
        'gpu': mock.MagicMock(),
        'mathutils': mock.MagicMock(),
        'bmesh': mock.MagicMock(),
    }
    
    # Add the modules to sys.modules
    for name, module in mock_modules.items():
        sys.modules[name] = module
    
    # Set environment variables
    os.environ['BLENDER_USER_SCRIPTS'] = os.path.expanduser("~/blender/scripts")
    
    # Create a Blender main window
    blender_window = BlenderMainWindow()
    blender_window.show()
    
    return blender_window
