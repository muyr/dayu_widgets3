#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2019.4
# Email : muyanru345@163.com
###################################################################

from dayu_widgets3.form import MForm
from dayu_widgets3.qt import *
# from schematics.models import Model
# from schematics.types import StringType
#
# class LoginForm(Model):
#     user_name = StringType(min_length=5, max_length=15)
#     password = StringType(min_length=5, max_length=15)
#
#     class Options()
#
#
# class MFormTest(QWidget):
#     def __init__(self, parent=None):
#         super(MFormTest, self).__init__(parent)



if __name__ == '__main__':
    import sys
    from dayu_widgets3 import dayu_theme
    app = QApplication(sys.argv)
    test = MFormTest()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())
