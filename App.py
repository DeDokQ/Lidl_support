import json
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTextEdit, QComboBox, QLabel,
                             QLineEdit, QFileDialog, QDialog, QCheckBox)
from PyQt5.QtCore import QTimer


def get_instruction(language):
    from instruction import get_instruction
    return get_instruction(language)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.translations = {
            'en': {
                "instruction": 'Instruction',
                "create_folders": 'Create Folders',
                "start": 'Start',
                "settings": 'Settings',
                "t_card_id": 'T-card ID',
                "software_logs": 'Software logs',
                "settings_error": 'Check that the settings are filled in correctly',
                "checkbox_folders": "Open the folder with the copied files",
                "checkbox_screenshot": "Open the screenshot",
            },
            'ru': {
                "instruction": 'Инструкция',
                "create_folders": 'Создать папки',
                "start": 'Начать',
                "settings": 'Настройки',
                "t_card_id": 'Айди Т-карты',
                "software_logs": 'Программные логи',
                "settings_error": 'Проверьте правильность заполнения настроек',
                "checkbox_folders": "Открывать папку с скопированными файлами",
                "checkbox_screenshot": "Открывать сделанный скриншот",
            }
        }

        self.setWindowTitle("Hex Merge Helper")
        self.current_language = 'ru'
        self.is_countdown_active = False
        self.countdown_time = 3

        self.layout = QVBoxLayout()
        self.init_ui()
        self.setLayout(self.layout)

        self.resize(960, 540)
        self.apply_styles_from_file('static/styles/styles.qss')
        self.update_language()

        # Таймер для отсчета времени
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)

    def init_ui(self):
        self.input_field = QLineEdit()
        self.input_field.setFixedWidth(self.width() * 0.25)

        self.log_field = QTextEdit()
        self.log_field.setReadOnly(True)
        self.label = QLabel()

        self.instruction_button = QPushButton()
        self.folders_button = QPushButton()
        self.settings_button = QPushButton()
        self.send_text_button = QPushButton()

        self.checkbox_folders = QCheckBox()
        self.checkbox_screenshot = QCheckBox()
        self.checkbox_folders.setChecked(True)
        self.checkbox_screenshot.setChecked(True)

        self.instruction_button.clicked.connect(self.handle_get_instruction)
        self.folders_button.clicked.connect(self.handle_create_folders)
        self.send_text_button.clicked.connect(self.handle_create_data)
        self.settings_button.clicked.connect(self.show_settings_dialog)

        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.log_field)
        self.layout.addWidget(self.checkbox_folders)
        self.layout.addWidget(self.checkbox_screenshot)
        self.layout.addWidget(self.instruction_button)
        self.layout.addWidget(self.folders_button)
        self.layout.addWidget(self.settings_button)
        self.layout.addWidget(self.send_text_button)

        self.language_selector = QComboBox()
        self.language_selector.addItem('Русский', 'ru')
        self.language_selector.addItem('English', 'en')
        self.language_selector.currentIndexChanged.connect(self.change_language)
        self.layout.addWidget(self.language_selector)

        from SettingsDialog import SettingsDialog
        self.dialog = SettingsDialog()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)

    def handle_get_instruction(self):
        self.log_action("\n\n")
        self.log_field.insertHtml(get_instruction(self.current_language))
        self.log_action("\n\n")

    def handle_create_folders(self):
        if self.dialog.is_data_valid():
            file_path, _ = QFileDialog.getOpenFileName(self, "Выберите Excel файл", "",
                                                       "Excel Files (*.xlsx);;All Files (*)")
            if file_path:
                self.log_action(f"Выбран файл: {file_path}")
                self.process_file(file_path)
        else:
            self.log_action(self.translations[self.current_language]["settings_error"])

    def handle_create_data(self):
        if self.is_countdown_active:
            self.cancel_countdown()
        else:
            self.start_countdown()

    def start_countdown(self):
        self.is_countdown_active = True
        self.countdown_time = 1
        self.log_action(self.get_log_message("Processing in {time} seconds... Click again to cancel.",
                                             "Запуск через {time} секунды... Нажмите повторно для отмены."))
        self.timer.start(1000)

    def update_countdown(self):
        self.countdown_time -= 1
        if self.countdown_time > 0:
            self.log_action(self.get_log_message("Processing in {time} seconds... Click again to cancel.",
                                                 "Запуск через {time} секунды... Нажмите повторно для отмены."))
        else:
            self.timer.stop()
            self.is_countdown_active = False
            if self.input_field.text():
                self.create_data()
            else:
                self.log_action("ID T-CARD is EMPTY! / Айди Т-карты пустое!")

    def get_log_message(self, en_message, ru_message):
        return en_message.format(time=self.countdown_time) if self.current_language == "en" else ru_message.format(
            time=self.countdown_time)

    def cancel_countdown(self):
        self.timer.stop()
        self.is_countdown_active = False
        if self.current_language == "en":
            self.log_action("Process cancelled.")
        else:
            self.log_action("Процесс прекращен.")

    def create_data(self):
        text = self.input_field.text()
        self.log_action(f">>> {text}")

        from FileCopier import copy_latest_files
        self.log_action(copy_latest_files(target_folder_name=text, is_folder=self.checkbox_folders.isChecked(),
                                          is_screenshot=self.checkbox_screenshot.isChecked()))
        self.input_field.clear()

    def log_action(self, message, countdown_time=None):
        if countdown_time is not None:
            message = message.format(countdown_time)
        self.log_field.append(message)

    def process_file(self, file_path):
        from FoldersCreator import create_folders
        self.log_action(f"\n\n{file_path} -> Успешно выбран")
        self.log_action("Создание папок\n\n")

        self.log_action(create_folders(path=file_path, language=self.current_language,
                                       column_date=self.dialog.column_dates_input.text(),
                                       row_date_start=self.dialog.row_dates_range_start_input.text(),
                                       row_date_end=self.dialog.row_dates_range_end_input.text(),
                                       column_eqp=self.dialog.column_equipment_input.text(),
                                       column_cards_id=self.dialog.column_cards_id.text()))

    def apply_styles_from_file(self, file_name):
        self.setStyleSheet("""
                   QWidget {
                        background-color: #f0f0f0;
                    }
                    
                    /* Стиль кнопок */
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border-radius: 10px;
                        padding: 10px;
                        font-size: 16px;
                    }
                    
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                    
                    /* Стиль текстового поля */
                    QTextEdit {
                        background-color: #ffffff;
                        color: #333;
                        font-family: Courier;
                        font-size: 14px;
                        border: 2px solid #ccc;
                        border-radius: 5px;
                        padding: 10px;
                    }
                    
                    /* Стиль поля для ввода */
                    QLineEdit {
                        background-color: #ffffff;
                        color: #333;
                        font-family: Courier;
                        font-size: 16px;
                        font-weight: bold;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        padding: 3px;
                        min-height: 30px;  /* Установка минимальной высоты */
                    }
                    
                    /* Стиль выпадающего списка */
                    QComboBox {
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        padding: 5px;
                        background-color: #ffffff;
                        font-family: Courier;
                        font-size: 16px;
                    }
                    
                    QComboBox::drop-down {
                        subcontrol-origin: padding;
                        subcontrol-position: top right;
                        width: 20px;
                    }
                    
                    QComboBox::down-arrow {
                        image: url(:/icons/down_arrow.png); /* Убедитесь, что иконка доступна */
                    }
                    
                    QComboBox QAbstractItemView {
                        background-color: #ffffff;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        selection-background-color: #4CAF50;
                        selection-color: white;
                    }
               """)

    def update_language(self):
        self.instruction_button.setText(self.translations[self.current_language]["instruction"])
        self.folders_button.setText(self.translations[self.current_language]["create_folders"])
        self.send_text_button.setText(self.translations[self.current_language]["start"])
        self.settings_button.setText(self.translations[self.current_language]["settings"])
        self.label.setText(self.translations[self.current_language]["software_logs"])
        self.input_field.setPlaceholderText(self.translations[self.current_language]["t_card_id"])
        self.checkbox_folders.setText(self.translations[self.current_language]["checkbox_folders"])
        self.checkbox_screenshot.setText(self.translations[self.current_language]["checkbox_screenshot"])

    def change_language(self, index):
        language_code = self.language_selector.itemData(index)
        if language_code in self.translations:
            self.current_language = language_code
            self.update_language()
            self.dialog.set_language(self.current_language)
        else:
            self.log_action(f"Language '{language_code}' not found.")

    def show_settings_dialog(self):
        self.dialog.exec_()
