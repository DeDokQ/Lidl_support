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
                'COLUMN_DATES': 'The letter designation of the DATE column:',
                'ROW_DATES_RANGE': "The range of work lines FROM and TO:",
                'COLUMN_EQUIPMENT': "The letter designation of the column 'Store ID Domain:",
                'COLUMN_CARDS': "The letter designation of the column 'No. of cards':",
                'SETTINGS_TITLE': 'Settings',
                'ROW_DATES_RANGE_START': 'The beginning of the range: ',
                'ROW_DATES_RANGE_END': 'End of the range: ',
            },
            'ru': {
                'COLUMN_DATES': 'Буквенное обозначение столбика ДАТЫ:',
                'ROW_DATES_RANGE': 'Диапазон строк работы ОТ и ДО:',
                'COLUMN_EQUIPMENT': "Буквенное обозначение столбика 'Store ID Domain':",
                'COLUMN_CARDS': "Буквенное обозначение столбика 'No. of cards':",
                'SETTINGS_TITLE': 'Настройки',
                'ROW_DATES_RANGE_START': 'Начало диапазона: ',
                'ROW_DATES_RANGE_END': 'Конец диапазона: ',
            }
        }

        self.language = 'ru'
        self.layout = QFormLayout(self)
        self.row_dates_range_layout = QHBoxLayout()

        self.update_ui()
        self.apply_styles_from_file()

    def update_ui(self):

        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        while self.row_dates_range_layout.count():
            child = self.row_dates_range_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

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

        self.setWindowTitle(self.translations[self.language]['SETTINGS_TITLE'])
        self.layout.addRow(self.translations[self.language]['COLUMN_DATES'], self.column_dates_input)
        self.layout.addRow(self.translations[self.language]['ROW_DATES_RANGE'], self.row_dates_range_layout)
        self.layout.addRow(self.translations[self.language]['COLUMN_EQUIPMENT'], self.column_equipment_input)
        self.layout.addRow(self.translations[self.language]['COLUMN_CARDS'], self.column_cards_id)
        self.layout.addWidget(self.buttonBox)

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
        self.update_ui()

    def apply_styles_from_file(self):
        self.setStyleSheet("""
                           QWidget {
                                background-color: #F4F4F9;
                                font-family: "Arial", sans-serif;
                                color: #333;
                            }
                            
                            /* Шапка окна (Заголовок) */
                            QDialog {
                                border: 2px solid #A0A0A0;
                                background-color: #E9ECEF;
                                border-radius: 10px;
                            }
                            
                            /* Поля ввода */
                            QLineEdit {
                                border: 1px solid #A0A0A0;
                                border-radius: 5px;
                                padding: 5px;
                                font-size: 14px;
                                color: #333;
                                background-color: #FFF;
                            }
                            
                            QLineEdit:focus {
                                border: 1px solid #007BFF;
                            }
                            
                            /* Метки (Labels) */
                            QLabel {
                                font-size: 14px;
                                font-weight: bold;
                                color: #333;
                            }
                            
                            /* Кнопки */
                            QPushButton {
                                background-color: #007BFF;
                                color: white;
                                padding: 6px 12px;
                                border: none;
                                border-radius: 5px;
                                font-size: 14px;
                            }
                            
                            QPushButton:hover {
                                background-color: #0056b3;
                            }
                            
                            QPushButton:pressed {
                                background-color: #004085;
                            }
                            
                            /* Комбинированный стиль для формы */
                            QFormLayout {
                                margin: 20px;
                            }
                            
                            QDialogButtonBox {
                                padding-top: 10px;
                            }

                       """)
