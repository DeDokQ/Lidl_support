from os.path import exists
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTextEdit, QComboBox, QLabel,
                             QLineEdit, QFileDialog, QDialog, QFormLayout, QDialogButtonBox, QHBoxLayout)
from os import path

from FileCopier import copy_latest_files


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")

        self.layout = QFormLayout(self)

        self.column_dates_input = QLineEdit()
        self.column_dates_input.setMaxLength(3)

        self.row_dates_range_start_input = QLineEdit()
        self.row_dates_range_end_input = QLineEdit()

        self.row_dates_range_start_input.setMaxLength(4)
        self.row_dates_range_end_input.setMaxLength(4)

        row_dates_range_layout = QHBoxLayout()
        row_dates_range_layout.addWidget(self.row_dates_range_start_input)
        row_dates_range_layout.addWidget(self.row_dates_range_end_input)

        self.column_equipment_input = QLineEdit()
        self.column_equipment_input.setMaxLength(3)

        self.column_cards_id = QLineEdit()
        self.column_cards_id.setMaxLength(3)

        # add widgets to layout
        self.layout.addRow("Номер столбца для дат:", self.column_dates_input)
        self.layout.addRow("Диапазон строк для дат (начало и конец):", row_dates_range_layout)
        self.layout.addRow("Номер столбца для номеров оборудования:", self.column_equipment_input)
        self.layout.addRow("T-card ID column / Столбец Айди Т-карты:", self.column_cards_id)

        # Button ok / cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout.addWidget(self.buttonBox)

        self.apply_styles_from_file('static/styles/styles.qss')

    def get_settings(self):
        # Собираем все значения с полей ввода
        return {
            "column_dates": self.column_dates_input.text(),
            "row_dates_range_start": self.row_dates_range_start_input.text(),
            "row_dates_range_end": self.row_dates_range_end_input.text(),
            "column_equipment": self.column_equipment_input.text(),
            "column_cards_id": self.column_cards_id.text(),
        }

    def is_data_valid(self):
        if (len(self.column_dates_input.text()) == 0
                or len(self.row_dates_range_start_input.text()) == 0
                or len(self.row_dates_range_end_input.text()) == 0
                or len(self.column_equipment_input.text()) == 0
                or len(self.column_cards_id.text()) == 0
        ):
            return False
        else:
            return True

    def apply_styles_from_file(self, file_name):
        if path.exists(file_name):
            with open(file_name, 'r') as file:
                style_sheet = file.read()
            self.setStyleSheet(style_sheet)