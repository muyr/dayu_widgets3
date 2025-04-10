# Import built-in modules
import functools
from typing import Any, Dict, List, Optional, Union, Callable

# Import third-party modules
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets

# Import local modules
from dayu_widgets import dayu_theme
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.menu import MMenu
from dayu_widgets.push_button import MPushButton
from dayu_widgets.qt import get_scale_factor
from dayu_widgets.radio_button import MRadioButton
from dayu_widgets.tool_button import MToolButton


class MButtonGroupBase(QtWidgets.QWidget):
    """Base class for all button group widgets.

    This class provides common functionality for button groups, including layout management,
    button creation, and property handling.
    """

    def __init__(self, orientation: QtCore.Qt.Orientation = QtCore.Qt.Horizontal, parent=None):
        """Initialize the button group base class.

        Args:
            orientation: The orientation of the button group (horizontal or vertical)
            parent: The parent widget
        """
        super(MButtonGroupBase, self).__init__(parent=parent)

        self._main_layout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.LeftToRight
            if orientation == QtCore.Qt.Horizontal
            else QtWidgets.QBoxLayout.TopToBottom
        )

        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._main_layout)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self._button_group = QtWidgets.QButtonGroup()
        self._orientation = "horizontal" if orientation == QtCore.Qt.Horizontal else "vertical"

    def set_spacing(self, value: int) -> None:
        """Set the spacing between buttons.

        Args:
            value: The spacing value in pixels
        """
        self._main_layout.setSpacing(value)

    def get_button_group(self) -> QtWidgets.QButtonGroup:
        """Get the internal button group.

        Returns:
            The button group object
        """
        return self._button_group

    def create_button(self, data_dict: Dict[str, Any]) -> QtWidgets.QAbstractButton:
        """Create a button based on the provided data.

        This method must be implemented by subclasses.

        Args:
            data_dict: Dictionary containing button properties

        Returns:
            A button widget
        """
        raise NotImplementedError()

    def add_button(self, data_dict: Union[str, QtGui.QIcon, Dict[str, Any]], index: Optional[int] = None) -> QtWidgets.QAbstractButton:
        """Add a button to the group.

        Args:
            data_dict: Button data (string, icon, or dictionary with properties)
            index: Optional index for the button in the group

        Returns:
            The created button
        """
        if isinstance(data_dict, str):
            data_dict = {"text": data_dict}
        elif isinstance(data_dict, QtGui.QIcon):
            data_dict = {"icon": data_dict}

        button = self.create_button(data_dict)
        button.setProperty("combine", self._orientation)

        # Set button properties from data dictionary
        for prop in ["text", "icon", "data", "checked", "shortcut", "tooltip", "checkable"]:
            if data_dict.get(prop):
                # Special case for tooltip which uses a different property name
                if prop == "tooltip":
                    button.setProperty("toolTip", data_dict.get(prop))
                else:
                    button.setProperty(prop, data_dict.get(prop))

        # Connect signals
        if data_dict.get("clicked"):
            button.clicked.connect(data_dict.get("clicked"))
        if data_dict.get("toggled"):
            button.toggled.connect(data_dict.get("toggled"))

        # Add to button group
        if index is None:
            self._button_group.addButton(button)
        else:
            self._button_group.addButton(button, index)

        self._main_layout.insertWidget(self._main_layout.count(), button)
        return button

    def set_button_list(self, button_list: List[Dict[str, Any]]) -> None:
        """Set the list of buttons in the group.

        This removes any existing buttons and adds the new ones.

        Args:
            button_list: List of button data dictionaries
        """
        # Remove existing buttons
        for button in self._button_group.buttons():
            self._button_group.removeButton(button)
            self._main_layout.removeWidget(button)
            button.setVisible(False)

        # Add new buttons
        for index, data_dict in enumerate(button_list):
            button = self.add_button(data_dict, index)

            # Set position property for styling
            if index == 0:
                button.setProperty("position", "left")
            elif index == len(button_list) - 1:
                button.setProperty("position", "right")
            else:
                button.setProperty("position", "center")


class MPushButtonGroup(MButtonGroupBase):
    """A group of push buttons.

    This class provides a group of MPushButton widgets with consistent styling and behavior.
    """

    def __init__(self, orientation: QtCore.Qt.Orientation = QtCore.Qt.Horizontal, parent=None):
        """Initialize the push button group.

        Args:
            orientation: The orientation of the button group (horizontal or vertical)
            parent: The parent widget
        """
        super(MPushButtonGroup, self).__init__(orientation=orientation, parent=parent)
        self.set_spacing(1)
        self._dayu_type = MPushButton.PrimaryType
        self._dayu_size = dayu_theme.default_size
        self._button_group.setExclusive(False)

    def create_button(self, data_dict: Dict[str, Any]) -> MPushButton:
        """Create a push button with the specified properties.

        Args:
            data_dict: Dictionary containing button properties

        Returns:
            A configured MPushButton instance
        """
        button = MPushButton()
        button.set_dayu_size(data_dict.get("dayu_size", self._dayu_size))
        button.set_dayu_type(data_dict.get("dayu_type", self._dayu_type))
        return button

    def get_dayu_size(self) -> int:
        """Get the button size.

        Returns:
            The button size value
        """
        return self._dayu_size

    def get_dayu_type(self) -> str:
        """Get the button type.

        Returns:
            The button type value
        """
        return self._dayu_type

    def set_dayu_size(self, value: int) -> None:
        """Set the button size.

        Args:
            value: The button size value
        """
        self._dayu_size = value

    def set_dayu_type(self, value: str) -> None:
        """Set the button type.

        Args:
            value: The button type value
        """
        self._dayu_type = value

    # Define Qt properties
    dayu_size = QtCore.Property(int, get_dayu_size, set_dayu_size)
    dayu_type = QtCore.Property(str, get_dayu_type, set_dayu_type)


class MCheckBoxGroup(MButtonGroupBase):
    """A group of checkboxes.

    This class provides a group of MCheckBox widgets with consistent styling and behavior.
    It supports selecting multiple items and provides context menu options for selection management.
    """

    sig_checked_changed = QtCore.Signal(list)

    def __init__(self, orientation: QtCore.Qt.Orientation = QtCore.Qt.Horizontal, parent=None):
        """Initialize the checkbox group.

        Args:
            orientation: The orientation of the button group (horizontal or vertical)
            parent: The parent widget
        """
        super(MCheckBoxGroup, self).__init__(orientation=orientation, parent=parent)
        scale_x, _ = get_scale_factor()
        self.set_spacing(15 * scale_x)
        self._button_group.setExclusive(False)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._slot_context_menu)
        self._button_group.idClicked.connect(self._slot_map_signal)
        self._dayu_checked = []

    def create_button(self, data_dict: Dict[str, Any]) -> MCheckBox:
        """Create a checkbox with the specified properties.

        Args:
            data_dict: Dictionary containing button properties

        Returns:
            A configured MCheckBox instance
        """
        return MCheckBox()

    @QtCore.Slot(QtCore.QPoint)
    def _slot_context_menu(self, point: QtCore.QPoint) -> None:
        """Show context menu for checkbox selection operations.

        Args:
            point: The position where the context menu should be shown
        """
        context_menu = MMenu(parent=self)
        action_select_all = context_menu.addAction("Select All")
        action_select_none = context_menu.addAction("Select None")
        action_select_invert = context_menu.addAction("Select Invert")
        action_select_all.triggered.connect(functools.partial(self._slot_set_select, True))
        action_select_none.triggered.connect(functools.partial(self._slot_set_select, False))
        action_select_invert.triggered.connect(functools.partial(self._slot_set_select, None))
        context_menu.exec_(QtGui.QCursor.pos() + QtCore.QPoint(10, 10))

    @QtCore.Slot(bool)
    def _slot_set_select(self, state: Optional[bool]) -> None:
        """Set the selection state of all checkboxes.

        Args:
            state: True to select all, False to deselect all, None to invert selection
        """
        for check_box in self._button_group.buttons():
            if state is None:
                old_state = check_box.isChecked()
                check_box.setChecked(not old_state)
            else:
                check_box.setChecked(state)
        self._slot_map_signal()

    @QtCore.Slot(int)
    def _slot_map_signal(self, state: Optional[int] = None) -> None:
        """Update the checked state and emit the signal.

        Args:
            state: The state that triggered the signal (not used)
        """
        checked_buttons = [
            check_box.text()
            for check_box in self._button_group.buttons()
            if check_box.isChecked()
        ]
        self.sig_checked_changed.emit(checked_buttons)

    def set_dayu_checked(self, value: Union[str, List[str]]) -> None:
        """Set the checked items.

        Args:
            value: String or list of strings representing the items to check
        """
        if not isinstance(value, list):
            value = [value]

        if value == self.get_dayu_checked():
            return

        self._dayu_checked = value
        for check_box in self._button_group.buttons():
            flag = QtCore.Qt.Checked if check_box.text() in value else QtCore.Qt.Unchecked

            if flag != check_box.checkState():
                check_box.setCheckState(flag)

        self.sig_checked_changed.emit(value)

    def get_dayu_checked(self) -> List[str]:
        """Get the currently checked items.

        Returns:
            List of strings representing the checked items
        """
        checked_buttons = [
            check_box.text()
            for check_box in self._button_group.buttons()
            if check_box.isChecked()
        ]
        return checked_buttons

    # Define Qt property
    dayu_checked = QtCore.Property(
        "QVariantList",
        get_dayu_checked,
        set_dayu_checked,
        notify=sig_checked_changed
    )


class MRadioButtonGroup(MButtonGroupBase):
    """A group of radio buttons.

    This class provides a group of MRadioButton widgets with consistent styling and behavior.
    It supports selecting a single item at a time.

    Property:
        dayu_checked: The ID of the currently checked radio button
    """

    sig_checked_changed = QtCore.Signal(int)

    def __init__(self, orientation: QtCore.Qt.Orientation = QtCore.Qt.Horizontal, parent=None):
        """Initialize the radio button group.

        Args:
            orientation: The orientation of the button group (horizontal or vertical)
            parent: The parent widget
        """
        super(MRadioButtonGroup, self).__init__(orientation=orientation, parent=parent)
        scale_x, _ = get_scale_factor()
        self.set_spacing(15 * scale_x)
        self._button_group.setExclusive(True)
        self._button_group.idClicked.connect(self.sig_checked_changed)

    def create_button(self, data_dict: Dict[str, Any]) -> MRadioButton:
        """Create a radio button with the specified properties.

        Args:
            data_dict: Dictionary containing button properties

        Returns:
            A configured MRadioButton instance
        """
        return MRadioButton()

    def set_dayu_checked(self, value: int) -> None:
        """Set the checked radio button by ID.

        Args:
            value: The ID of the radio button to check
        """
        if value == self.get_dayu_checked():
            return

        button = self._button_group.button(value)
        if button:
            button.setChecked(True)
            self.sig_checked_changed.emit(value)
        else:
            print("Error: No radio button with ID {}".format(value))

    def get_dayu_checked(self) -> int:
        """Get the ID of the currently checked radio button.

        Returns:
            The ID of the checked radio button
        """
        return self._button_group.checkedId()

    # Define Qt property
    dayu_checked = QtCore.Property(
        int,
        get_dayu_checked,
        set_dayu_checked,
        notify=sig_checked_changed
    )


class MToolButtonGroup(MButtonGroupBase):
    """A group of tool buttons.

    This class provides a group of MToolButton widgets with consistent styling and behavior.
    It can be configured to allow either single or multiple selection.

    Property:
        dayu_checked: The ID of the currently checked tool button
    """

    sig_checked_changed = QtCore.Signal(int)

    def __init__(
        self,
        size: Optional[int] = None,
        type: Optional[str] = None,
        exclusive: bool = False,
        orientation: QtCore.Qt.Orientation = QtCore.Qt.Horizontal,
        parent=None,
    ):
        """Initialize the tool button group.

        Args:
            size: Optional size for all buttons in the group
            type: Optional type for all buttons in the group
            exclusive: Whether only one button can be checked at a time
            orientation: The orientation of the button group (horizontal or vertical)
            parent: The parent widget
        """
        super(MToolButtonGroup, self).__init__(orientation=orientation, parent=parent)
        self.set_spacing(1)
        self._button_group.setExclusive(exclusive)
        self._size = size
        self._type = type
        self._button_group.idClicked.connect(self.sig_checked_changed)

    def create_button(self, data_dict: Dict[str, Any]) -> MToolButton:
        """Create a tool button with the specified properties.

        Args:
            data_dict: Dictionary containing button properties

        Returns:
            A configured MToolButton instance
        """
        button = MToolButton()
        if data_dict.get("svg"):
            button.svg(data_dict.get("svg"))
        if data_dict.get("text"):
            if data_dict.get("svg") or data_dict.get("icon"):
                button.text_beside_icon()
            else:
                button.text_only()
        else:
            button.icon_only()
        return button

    def set_dayu_checked(self, value: int) -> None:
        """Set the checked tool button by ID.

        Args:
            value: The ID of the tool button to check
        """
        if value == self.get_dayu_checked():
            return
        button = self._button_group.button(value)
        if button:
            button.setChecked(True)
            self.sig_checked_changed.emit(value)
        else:
            print("Error: No tool button with ID {}".format(value))

    def get_dayu_checked(self) -> int:
        """Get the ID of the currently checked tool button.

        Returns:
            The ID of the checked tool button
        """
        return self._button_group.checkedId()

    # Define Qt property
    dayu_checked = QtCore.Property(
        int,
        get_dayu_checked,
        set_dayu_checked,
        notify=sig_checked_changed
    )
