from os.path import exists
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTextEdit, QComboBox, QLabel,
                             QLineEdit, QFileDialog, QDialog, QFormLayout, QDialogButtonBox, QHBoxLayout)
from os import path

from FileCopier import copy_latest_files


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.translations = {
            'en': {
                'COLUMN_DATES': 'The letter of the date column:',
                'ROW_DATES_RANGE': "The range of your team's lines:",
                'COLUMN_EQUIPMENT': "The letter of the 'Store ID Domain' column:",
                'COLUMN_CARDS': "The letter of the 'No. of cards' column:",
                'SETTINGS_TITLE': 'Settings',
                'ROW_DATES_RANGE_START': 'The beginning of the range: ',
                'ROW_DATES_RANGE_END': 'End of the range: ',
            },
            'ru': {
                'COLUMN_DATES': 'Буква столбика с датами:',
                'ROW_DATES_RANGE': 'Диапазон строк вашей бригады:',
                'COLUMN_EQUIPMENT': "Буква столбика 'Store ID Domain':",
                'COLUMN_CARDS': "Буква столбика 'No. of cards':",
                'SETTINGS_TITLE': 'Настройки',
                'ROW_DATES_RANGE_START': 'Начало диапазона: ',
                'ROW_DATES_RANGE_END': 'Конец диапазона: ',
            }
        }

        self.language = 'ru'
        self.layout = QFormLayout(self)
        self.row_dates_range_layout = QHBoxLayout()

        self.update_ui()

    def update_ui(self):

        # Очищаем старый layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        while self.row_dates_range_layout.count():
            child = self.row_dates_range_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Создаем новый layout с текущим языком
        self.row_dates_range_start_input = QLineEdit()
        self.row_dates_range_end_input = QLineEdit()

        self.row_dates_range_layout.addWidget(self.row_dates_range_start_input)
        self.row_dates_range_layout.addWidget(self.row_dates_range_end_input)

        self.column_dates_input = QLineEdit()
        self.column_dates_input.setMaxLength(3)

        self.row_dates_range_start_input.setMaxLength(4)
        self.row_dates_range_end_input.setMaxLength(4)

        self.column_equipment_input = QLineEdit()
        self.column_equipment_input.setMaxLength(3)
        self.column_cards_id = QLineEdit()
        self.column_cards_id.setMaxLength(3)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Обновляем заголовок окна
        self.setWindowTitle(self.translations[self.language]['SETTINGS_TITLE'])

        self.layout.addRow(self.translations[self.language]['COLUMN_DATES'], self.column_dates_input)
        self.layout.addRow(self.translations[self.language]['ROW_DATES_RANGE'], self.row_dates_range_layout)
        self.layout.addRow(self.translations[self.language]['COLUMN_EQUIPMENT'], self.column_equipment_input)
        self.layout.addRow(self.translations[self.language]['COLUMN_CARDS'], self.column_cards_id)
        self.layout.addWidget(self.buttonBox)

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

    def set_language(self, update_language):
        self.language = update_language
        self.update_ui()  # Обновляем UI после смены языка

    def apply_styles_from_file(self, file_name):
        if path.exists(file_name):
            with open(file_name, 'r') as file:
                style_sheet = file.read()
            self.setStyleSheet(style_sheet)
