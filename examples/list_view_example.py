# Import third-party modules
from qtpy import QtWidgets

# Import local modules
from dayu_widgets import dayu_theme
from dayu_widgets.divider import MDivider
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MListView
from dayu_widgets.line_edit import MLineEdit
import examples._mock_data as mock


class ListViewExample(QtWidgets.QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(ListViewExample, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        table_small = MListView(size=dayu_theme.small)
        table_default = MListView()
        table_large = MListView(size=dayu_theme.large)

        model_1 = MTableModel()
        model_1.set_header_list(mock.header_list)
        model_sort = MSortFilterModel()
        model_sort.setSourceModel(model_1)
        table_small.setModel(model_sort)
        table_default.setModel(model_sort)
        table_large.setModel(model_sort)
        model_sort.set_header_list(mock.header_list)
        table_small.set_header_list(mock.header_list)
        table_default.set_header_list(mock.header_list)
        table_large.set_header_list(mock.header_list)
        model_1.set_data_list(mock.data_list)

        line_edit = MLineEdit().search().small()
        line_edit.textChanged.connect(model_sort.set_search_pattern)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(line_edit)
        main_lay.addWidget(MDivider("Small Size"))
        main_lay.addWidget(table_small)
        main_lay.addWidget(MDivider("Default Size"))
        main_lay.addWidget(table_default)
        main_lay.addWidget(MDivider("Large Size"))
        main_lay.addWidget(table_large)
        main_lay.addStretch()
        self.setLayout(main_lay)


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = ListViewExample()
        dayu_theme.apply(test)
        test.show()
