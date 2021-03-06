#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2019.2
# Email : muyanru345@163.com
###################################################################

from dayu_widgets3.qt import QProgressBar, Qt, Property, Slot


class MProgressBar(QProgressBar):
    '''
    props:
        status: str

    '''
    ErrorStatus = 'error'
    NormalStatus = 'primary'
    SuccessStatus = 'success'

    def __init__(self, parent=None):
        super(MProgressBar, self).__init__(parent=parent)
        self.setAlignment(Qt.AlignCenter)
        self._status = MProgressBar.NormalStatus

    def auto_color(self):
        self.valueChanged.connect(self._update_color)
        return self

    @Slot(int)
    def _update_color(self, value):
        if value >= self.maximum():
            self.set_dayu_status(MProgressBar.SuccessStatus)
        else:
            self.set_dayu_status(MProgressBar.NormalStatus)

    def get_dayu_status(self):
        return self._status

    def set_dayu_status(self, value):
        self._status = value
        self.style().polish(self)

    dayu_status = Property(str, get_dayu_status, set_dayu_status)

    def normal(self):
        self.set_dayu_status(MProgressBar.NormalStatus)
        return self

    def error(self):
        self.set_dayu_status(MProgressBar.ErrorStatus)
        return self

    def success(self):
        self.set_dayu_status(MProgressBar.SuccessStatus)
        return self

    # def paintEvent(self, event):
    #     pass


"""
MProgressBar {
    font-size: @font_size_small;
    color: @primary_text_color;
    border: 0 solid @border_color;
    background-color: @border_color;
    min-height: 12px;
    max-height: 12px;
    border-radius: 6px;
}

MProgressBar::chunk {
    min-height: 12px;
    max-height: 12px;
    border-radius: 5px;
}
MProgressBar[status=error]::chunk {
    background-color: @error_6;
}
MProgressBar[status=success]::chunk {
    background-color: @success_6;
}
MProgressBar[status=primary]::chunk {
    background-color: @primary_color;
}"""
