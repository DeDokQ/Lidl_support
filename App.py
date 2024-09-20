import json
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTextEdit, QComboBox, QLabel,
                             QLineEdit, QFileDialog, QDialog)
from PyQt5.QtCore import QTimer

BUTTON1_TEXT = 'button1'
BUTTON2_TEXT = 'button2'
SEND_TEXT_BUTTON = 'send_text_button'
SETTINGS_BUTTON_TEXT = 'settings_button'
USER_INPUT_FIELD = 'T-card ID'
LOG_TITLE = 'Software logs'
LOG_ACTION2_TEXT = 'log_action_2'
SETTINGS_ERROR = "None"


def get_instruction(language):
    import json
    with open('instruction.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    if language == 'ru':
        return data["languages"]["ru-ru"]
    else:
        return data["languages"]["en-en"]


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.translations = {
            'en': {
                BUTTON1_TEXT: 'Instruction',
                BUTTON2_TEXT: 'Create Folders',
                SEND_TEXT_BUTTON: 'Start',
                SETTINGS_BUTTON_TEXT: 'Settings',
                USER_INPUT_FIELD: 'T-card ID',
                LOG_TITLE: 'Software logs',
                LOG_ACTION2_TEXT: 'Button 2 pressed',
                SETTINGS_ERROR: 'Check that the settings are filled in correctly',
            },
            'ru': {
                BUTTON1_TEXT: 'Инструкция',
                BUTTON2_TEXT: 'Создать папки',
                SEND_TEXT_BUTTON: 'Начать',
                SETTINGS_BUTTON_TEXT: 'Настройки',
                USER_INPUT_FIELD: 'Айди Т-карты',
                LOG_TITLE: 'Программные логи',
                LOG_ACTION2_TEXT: 'Нажата Кнопка 2',
                SETTINGS_ERROR: 'Проверьте правильность заполнения настроек',
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

        from SettingsDialog import SettingsDialog
        self.dialog = SettingsDialog()

        # Таймер для отсчета времени
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)

    def init_ui(self):
        self.input_field = QLineEdit()
        self.input_field.setFixedWidth(self.width() * 0.25)

        self.log_field = QTextEdit()
        self.log_field.setReadOnly(True)
        self.label = QLabel()

        self.button1 = QPushButton()
        self.button2 = QPushButton()
        self.settings_button = QPushButton()
        self.send_text_button = QPushButton()

        # Привязка событий кнопок
        self.button1.clicked.connect(self.handle_get_instruction)
        self.button2.clicked.connect(self.handle_create_folders)
        self.send_text_button.clicked.connect(self.handle_create_data)
        self.settings_button.clicked.connect(self.show_settings_dialog)

        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.log_field)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.settings_button)
        self.layout.addWidget(self.send_text_button)

        # Выбор языка
        self.language_selector = QComboBox()
        self.language_selector.addItem('Русский', 'ru')
        self.language_selector.addItem('English', 'en')
        self.language_selector.currentIndexChanged.connect(self.change_language)
        self.layout.addWidget(self.language_selector)

        from SettingsDialog import SettingsDialog
        self.dialog = SettingsDialog()

        # Таймер для отсчета времени
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)

    def handle_get_instruction(self):
        self.log_action(get_instruction(self.current_language))

    def handle_create_folders(self):
        if self.dialog.is_data_valid():
            file_path, _ = QFileDialog.getOpenFileName(self, "Выберите Excel файл", "",
                                                       "Excel Files (*.xlsx);;All Files (*)")
            if file_path:
                self.log_action(f"Выбран файл: {file_path}")
                self.process_file(file_path)
        else:
            self.log_action(self.translations[self.current_language][SETTINGS_ERROR])

    def handle_create_data(self):
        if self.is_countdown_active:
            self.cancel_countdown()
        else:
            self.start_countdown()

    def start_countdown(self):
        self.is_countdown_active = True
        self.countdown_time = 3
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
        self.log_action(copy_latest_files(text))
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
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                style_sheet = file.read()
            self.setStyleSheet(style_sheet)
        else:
            self.log_action(f"Style file '{file_name}' not found.")

    def update_language(self):
        self.button1.setText(self.translations[self.current_language][BUTTON1_TEXT])
        self.button2.setText(self.translations[self.current_language][BUTTON2_TEXT])
        self.send_text_button.setText(self.translations[self.current_language][SEND_TEXT_BUTTON])
        self.settings_button.setText(self.translations[self.current_language][SETTINGS_BUTTON_TEXT])
        self.label.setText(self.translations[self.current_language][LOG_TITLE])
        self.input_field.setPlaceholderText(self.translations[self.current_language][USER_INPUT_FIELD])

    def change_language(self, index):
        language_code = self.language_selector.itemData(index)
        if language_code in self.translations:
            self.current_language = language_code
            self.update_language()
        else:
            self.log_action(f"Language '{language_code}' not found.")

    def show_settings_dialog(self):
        if self.dialog.exec_() == QDialog.Accepted:
            settings = self.dialog.get_settings()
            self.log_field.append(f"Настройки: {settings}")
