"""
MClickBrowserFilePushButton, MClickBrowserFileToolButton
MClickBrowserFolderPushButton, MClickBrowserFolderToolButton
Browser files or folders by selecting.
MDragFileButton, MDragFolderButton
Browser files or folders by dragging.
"""

# Import built-in modules
import os
from typing import List, Optional, Union

# Import third-party modules
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets

# Import local modules
from dayu_widgets import dayu_theme
from dayu_widgets.mixin import cursor_mixin
from dayu_widgets.mixin import property_mixin
from dayu_widgets.push_button import MPushButton
from dayu_widgets.tool_button import MToolButton


# NOTE PySide2 Crash without QObject wrapper

# @Slot()
def _slot_browser_file(self):
    """Slot function to browse files using QFileDialog."""
    filter_list = (
        "File(%s)" % (" ".join(["*" + e for e in self.get_dayu_filters()]))
        if self.get_dayu_filters()
        else "Any File(*)"
    )

    if self.get_dayu_multiple():
        r_files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            "Browser File",
            self.get_dayu_path(),
            filter_list
        )
        if r_files:
            self.sig_files_changed.emit(r_files)
            self.set_dayu_path(r_files[0])
    else:
        r_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Browser File",
            self.get_dayu_path(),
            filter_list
        )
        if r_file:
            self.sig_file_changed.emit(r_file)
            self.set_dayu_path(r_file)


# @Slot()
def _slot_browser_folder(self):
    """Slot function to browse folders using QFileDialog."""
    title = "Browser Folder"
    r_folder = QtWidgets.QFileDialog.getExistingDirectory(self, title, self.get_dayu_path())
    if r_folder:
        if self.get_dayu_multiple():
            self.sig_folders_changed.emit([r_folder])
        else:
            self.sig_folder_changed.emit(r_folder)
        self.set_dayu_path(r_folder)


# @Slot()
def _slot_save_file(self):
    """Slot function to save a file using QFileDialog."""
    filter_list = "Any File(*)"
    if self.get_dayu_filters():
        extensions = [f"*{e}" for e in self.get_dayu_filters()]
        filter_list = f"File({' '.join(extensions)})"

    title = "Save File"
    r_file, _ = QtWidgets.QFileDialog.getSaveFileName(
        self, title, self.get_dayu_path(), filter_list
    )
    if r_file:
        self.sig_file_changed.emit(r_file)
        self.set_dayu_path(r_file)


class MBrowserMixin:
    """Mixin class for browser components with common properties and methods."""

    def __init__(self, multiple: bool = False):
        """Initialize the browser mixin.

        Args:
            multiple: Whether to allow multiple selection
        """
        self._path = None
        self._multiple = multiple
        self._filters = []

    def get_dayu_filters(self) -> List[str]:
        """Get browser's format filters.

        Returns:
            List of file extensions to filter
        """
        return self._filters

    def set_dayu_filters(self, value: List[str]) -> None:
        """Set browser file format filters.

        Args:
            value: List of file extensions to filter
        """
        self._filters = value

    def get_dayu_path(self) -> Optional[str]:
        """Get last browser file path.

        Returns:
            The last browsed path
        """
        return self._path

    def set_dayu_path(self, value: Union[str, List[str]]) -> None:
        """Set browser file start path.

        Args:
            value: Path to start browsing from
        """
        self._path = value

    def get_dayu_multiple(self) -> bool:
        """Get browser can select multiple file or not.

        Returns:
            Whether multiple selection is enabled
        """
        return self._multiple

    def set_dayu_multiple(self, value: bool) -> None:
        """Set browser can select multiple file or not.

        Args:
            value: Whether to allow multiple selection
        """
        self._multiple = value


class MClickBrowserFilePushButton(MPushButton, MBrowserMixin):
    """A Clickable push button to browser files."""

    sig_file_changed = QtCore.Signal(str)
    sig_files_changed = QtCore.Signal(list)
    slot_browser_file = _slot_browser_file

    def __init__(self, text: str = "Browser", multiple: bool = False, parent=None):
        MPushButton.__init__(self, text=text, parent=parent)
        MBrowserMixin.__init__(self, multiple=multiple)
        self.setProperty("multiple", multiple)
        self.clicked.connect(self.slot_browser_file)
        self.setToolTip(self.tr("Click to browser file"))

    # Define Qt properties
    dayu_multiple = QtCore.Property(bool, MBrowserMixin.get_dayu_multiple, MBrowserMixin.set_dayu_multiple)
    dayu_path = QtCore.Property(str, MBrowserMixin.get_dayu_path, MBrowserMixin.set_dayu_path)
    dayu_filters = QtCore.Property(list, MBrowserMixin.get_dayu_filters, MBrowserMixin.set_dayu_filters)


class MClickBrowserFileToolButton(MToolButton, MBrowserMixin):
    """A Clickable tool button to browser files."""

    sig_file_changed = QtCore.Signal(str)
    sig_files_changed = QtCore.Signal(list)
    slot_browser_file = _slot_browser_file

    def __init__(self, multiple: bool = False, parent=None):
        MToolButton.__init__(self, parent=parent)
        MBrowserMixin.__init__(self, multiple=multiple)
        self.set_dayu_svg("cloud_line.svg")
        self.icon_only()
        self.clicked.connect(self.slot_browser_file)
        self.setToolTip(self.tr("Click to browser file"))

    # Define Qt properties
    dayu_multiple = QtCore.Property(bool, MBrowserMixin.get_dayu_multiple, MBrowserMixin.set_dayu_multiple)
    dayu_path = QtCore.Property(str, MBrowserMixin.get_dayu_path, MBrowserMixin.set_dayu_path)
    dayu_filters = QtCore.Property(list, MBrowserMixin.get_dayu_filters, MBrowserMixin.set_dayu_filters)


class MClickSaveFileToolButton(MToolButton, MBrowserMixin):
    """A Clickable tool button to save files."""

    sig_file_changed = QtCore.Signal(str)
    slot_browser_file = _slot_save_file

    def __init__(self, multiple: bool = False, parent=None):
        MToolButton.__init__(self, parent=parent)
        MBrowserMixin.__init__(self, multiple=multiple)
        self.set_dayu_svg("save_line.svg")
        self.icon_only()
        self.clicked.connect(self.slot_browser_file)
        self.setToolTip(self.tr("Click to save file"))

    # Define Qt properties
    dayu_path = QtCore.Property(str, MBrowserMixin.get_dayu_path, MBrowserMixin.set_dayu_path)
    dayu_filters = QtCore.Property(list, MBrowserMixin.get_dayu_filters, MBrowserMixin.set_dayu_filters)


class MDragFileButton(MToolButton, MBrowserMixin):
    """A Clickable and draggable tool button to upload files."""

    sig_file_changed = QtCore.Signal(str)
    sig_files_changed = QtCore.Signal(list)
    slot_browser_file = _slot_browser_file

    def __init__(self, text: str = "", multiple: bool = False, parent=None):
        MToolButton.__init__(self, parent=parent)
        MBrowserMixin.__init__(self, multiple=multiple)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.text_under_icon()
        self.setText(text)

        size = dayu_theme.drag_size
        self.set_dayu_size(size)
        self.setIconSize(QtCore.QSize(size, size))
        self.set_dayu_svg("cloud_line.svg")

        self.clicked.connect(self.slot_browser_file)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setToolTip(self.tr("Click to browser file"))

    # Define Qt properties
    dayu_multiple = QtCore.Property(bool, MBrowserMixin.get_dayu_multiple, MBrowserMixin.set_dayu_multiple)
    dayu_path = QtCore.Property(str, MBrowserMixin.get_dayu_path, MBrowserMixin.set_dayu_path)
    dayu_filters = QtCore.Property(list, MBrowserMixin.get_dayu_filters, MBrowserMixin.set_dayu_filters)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        """Override dragEnterEvent. Validate dragged files.

        Args:
            event: The drag enter event
        """
        if event.mimeData().hasFormat("text/uri-list"):
            file_list = self._get_valid_file_list(event.mimeData().urls())
            count = len(file_list)
            if count == 1 or (count > 1 and self.get_dayu_multiple()):
                event.acceptProposedAction()
                return

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        """Override dropEvent to accept the dropped files.

        Args:
            event: The drop event
        """
        file_list = self._get_valid_file_list(event.mimeData().urls())
        if self.get_dayu_multiple():
            self.sig_files_changed.emit(file_list)
            self.set_dayu_path(file_list)
        else:
            self.sig_file_changed.emit(file_list[0])
            self.set_dayu_path(file_list[0])

    def _get_valid_file_list(self, url_list) -> List[str]:
        """Get a list of valid files from the dropped URLs.

        Args:
            url_list: List of QUrls from the drop event

        Returns:
            List of valid file paths
        """
        # Import built-in modules
        import subprocess
        import sys

        file_list = []
        for url in url_list:
            file_name = url.toLocalFile()
            if sys.platform == "darwin":
                cmd = 'osascript -e \'get posix path of posix file "file://{0}"\''.format(file_name)
                sub_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    shell=True
                )
                file_name = sub_process.communicate()[0].strip()
                sub_process.wait()

            if os.path.isfile(file_name):
                if self.get_dayu_filters():
                    if os.path.splitext(file_name)[-1] in self.get_dayu_filters():
                        file_list.append(file_name)
                else:
                    file_list.append(file_name)

        return file_list


class MClickBrowserFolderPushButton(MPushButton, MBrowserMixin):
    """A Clickable push button to browser folders."""

    sig_folder_changed = QtCore.Signal(str)
    sig_folders_changed = QtCore.Signal(list)
    slot_browser_folder = _slot_browser_folder

    def __init__(self, text: str = "", multiple: bool = False, parent=None):
        MPushButton.__init__(self, text=text, parent=parent)
        MBrowserMixin.__init__(self, multiple=multiple)
        self.setProperty("multiple", multiple)
        self.clicked.connect(self.slot_browser_folder)
        self.setToolTip(self.tr("Click to browser folder"))

    # Define Qt properties
    dayu_multiple = QtCore.Property(bool, MBrowserMixin.get_dayu_multiple, MBrowserMixin.set_dayu_multiple)
    dayu_path = QtCore.Property(str, MBrowserMixin.get_dayu_path, MBrowserMixin.set_dayu_path)


@property_mixin
class MClickBrowserFolderToolButton(MToolButton, MBrowserMixin):
    """A Clickable tool button to browser folders."""

    sig_folder_changed = QtCore.Signal(str)
    sig_folders_changed = QtCore.Signal(list)
    slot_browser_folder = _slot_browser_folder

    def __init__(self, multiple: bool = False, parent=None):
        MToolButton.__init__(self, parent=parent)
        MBrowserMixin.__init__(self, multiple=multiple)
        self.set_dayu_svg("folder_line.svg")
        self.icon_only()
        self.clicked.connect(self.slot_browser_folder)
        self.setToolTip(self.tr("Click to browser folder"))

    # Define Qt properties
    dayu_multiple = QtCore.Property(bool, MBrowserMixin.get_dayu_multiple, MBrowserMixin.set_dayu_multiple)
    dayu_path = QtCore.Property(str, MBrowserMixin.get_dayu_path, MBrowserMixin.set_dayu_path)


@property_mixin
@cursor_mixin
class MDragFolderButton(MToolButton, MBrowserMixin):
    """A Clickable and draggable tool button to browser folders."""

    sig_folder_changed = QtCore.Signal(str)
    sig_folders_changed = QtCore.Signal(list)
    slot_browser_folder = _slot_browser_folder

    def __init__(self, multiple: bool = False, parent=None):
        MToolButton.__init__(self, parent=parent)
        MBrowserMixin.__init__(self, multiple=multiple)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.text_under_icon()
        self.set_dayu_svg("folder_line.svg")

        size = dayu_theme.drag_size
        self.set_dayu_size(size)
        self.setIconSize(QtCore.QSize(size, size))
        self.setText(self.tr("Click or drag folder here"))
        self.clicked.connect(self.slot_browser_folder)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setToolTip(self.tr("Click to browser folder or drag folder here"))

    # Define Qt properties
    dayu_multiple = QtCore.Property(bool, MBrowserMixin.get_dayu_multiple, MBrowserMixin.set_dayu_multiple)
    dayu_path = QtCore.Property(str, MBrowserMixin.get_dayu_path, MBrowserMixin.set_dayu_path)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        """Override dragEnterEvent. Validate dragged folders.

        Args:
            event: The drag enter event
        """
        if event.mimeData().hasFormat("text/uri-list"):
            # Get list of valid folders from dragged items
            folder_list = [
                url.toLocalFile()
                for url in event.mimeData().urls()
                if os.path.isdir(url.toLocalFile())
            ]
            count = len(folder_list)
            if count == 1 or (count > 1 and self.get_dayu_multiple()):
                event.acceptProposedAction()
                return

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        """Override dropEvent to accept the dropped folders.

        Args:
            event: The drop event
        """
        folder_list = [
            url.toLocalFile()
            for url in event.mimeData().urls()
            if os.path.isdir(url.toLocalFile())
        ]
        if self.get_dayu_multiple():
            self.sig_folders_changed.emit(folder_list)
        else:
            self.sig_folder_changed.emit(folder_list[0])
        self.set_dayu_path(folder_list[0])
