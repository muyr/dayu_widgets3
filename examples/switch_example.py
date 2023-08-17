#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2019.2
# Email : muyanru345@163.com
###################################################################

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import third-party modules
from qtpy import QtWidgets

# Import local modules
from dayu_widgets3 import dayu_theme
from dayu_widgets3.divider import MDivider
from dayu_widgets3.field_mixin import MFieldMixin
from dayu_widgets3.switch import MSwitch


class SwitchExample(QtWidgets.QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(SwitchExample, self).__init__(parent)
        self.setWindowTitle("Examples for MSwitch")
        self._init_ui()

    def _init_ui(self):
        check_box_1 = MSwitch()
        check_box_1.setChecked(True)
        check_box_2 = MSwitch()
        check_box_3 = MSwitch()
        check_box_3.setEnabled(False)
        lay = QtWidgets.QHBoxLayout()
        lay.addWidget(check_box_1)
        lay.addWidget(check_box_2)
        lay.addWidget(check_box_3)

        size_lay = QtWidgets.QFormLayout()
        size_lay.addRow("Huge", MSwitch().huge())
        size_lay.addRow("Large", MSwitch().large())
        size_lay.addRow("Medium", MSwitch().medium())
        size_lay.addRow("Small", MSwitch().small())
        size_lay.addRow("Tiny", MSwitch().tiny())

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(MDivider("Basic"))
        main_lay.addLayout(lay)
        main_lay.addWidget(MDivider("different size"))
        main_lay.addLayout(size_lay)
        main_lay.addStretch()
        self.setLayout(main_lay)


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets3.qt import application

    with application() as app:
        test = SwitchExample()
        dayu_theme.apply(test)
        test.show()
