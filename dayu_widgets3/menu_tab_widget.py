#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2019.3
# Email : muyanru345@163.com
###################################################################
"""A Navigation menu"""

from dayu_widgets3.tool_button import MToolButton
from dayu_widgets3.button_group import MButtonGroupBase
from dayu_widgets3.divider import MDivider
from dayu_widgets3.qt import Signal, QWidget, Property, QHBoxLayout, QVBoxLayout, Qt
from dayu_widgets3 import dayu_theme


class MBlockButton(MToolButton):
    """MBlockButton"""

    def __init__(self, parent=None):
        super(MBlockButton, self).__init__(parent)
        self.setCheckable(True)


class MBlockButtonGroup(MButtonGroupBase):
    """MBlockButtonGroup"""
    sig_checked_changed = Signal(int)

    def __init__(self, parent=None):
        super(MBlockButtonGroup, self).__init__(parent=parent)
        self.set_spacing(1)
        self._button_group.setExclusive(True)
        self._button_group.buttonClicked[int].connect(self.sig_checked_changed)

    def create_button(self, data_dict):
        button = MBlockButton()
        if data_dict.get('svg'):
            button.svg(data_dict.get('svg'))
        if data_dict.get('text'):
            if data_dict.get('svg') or data_dict.get('icon'):
                button.text_beside_icon()
            else:
                button.text_only()
        else:
            button.icon_only()
        button.set_dayu_size(dayu_theme.large)
        return button

    def set_dayu_checked(self, value):
        """Set current checked button's id"""
        button = self._button_group.button(value)
        button.setChecked(True)
        self.sig_checked_changed.emit(value)

    def get_dayu_checked(self):
        """Get current checked button's id"""
        return self._button_group.checkedId()

    dayu_checked = Property(int, get_dayu_checked, set_dayu_checked, notify=sig_checked_changed)


class MMenuTabWidget(QWidget):
    """MMenuTabWidget"""

    def __init__(self, parent=None):
        super(MMenuTabWidget, self).__init__(parent=parent)
        self.tool_button_group = MBlockButtonGroup()
        self._bar_layout = QHBoxLayout()
        self._bar_layout.setContentsMargins(10, 0, 10, 0)
        self._bar_layout.addWidget(self.tool_button_group)
        self._bar_layout.addStretch()
        bar_widget = QWidget()
        bar_widget.setObjectName('bar_widget')
        bar_widget.setLayout(self._bar_layout)
        bar_widget.setAttribute(Qt.WA_StyledBackground)
        main_lay = QVBoxLayout()
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(0)
        main_lay.addWidget(bar_widget)
        main_lay.addWidget(MDivider())
        main_lay.addSpacing(5)
        self.setLayout(main_lay)
        self.setFixedHeight(dayu_theme.large + 10)

    def tool_bar_append_widget(self, widget):
        """Add the widget too menubar's right position."""
        self._bar_layout.addWidget(widget)

    def tool_bar_insert_widget(self, widget):
        """Insert the widget to menubar's left position."""
        self._bar_layout.insertWidget(0, widget)

    def add_menu(self, data_dict, index=None):
        """Add a menu"""
        self.tool_button_group.add_button(data_dict, index)
