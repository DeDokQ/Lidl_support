import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QComboBox, QLabel, QLineEdit
from PyQt5.QtCore import Qt

BUTTON1_TEXT = 'button1'
BUTTON2_TEXT = 'button2'
SEND_TEXT_BUTTON = 'send_text_button'
USER_INPUT_FIELD = 'T-card ID'
LOG_TITLE = 'Software logs'
LOG_ACTION1_TEXT = 'log_action_1'
LOG_ACTION2_TEXT = 'log_action_2'


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Словарь с переводами
        self.translations = {
            'en': {
                BUTTON1_TEXT: 'Instruction',
                BUTTON2_TEXT: 'Create Folders',
                SEND_TEXT_BUTTON: 'Start',
                USER_INPUT_FIELD: 'T-card ID',
                LOG_TITLE: 'Software logs',
                LOG_ACTION1_TEXT: 'Button 1 pressed',
                LOG_ACTION2_TEXT: 'Button 2 pressed',
            },
            'ru': {
                BUTTON1_TEXT: 'Инструкция',
                BUTTON2_TEXT: 'Создать папки',
                SEND_TEXT_BUTTON: 'Начать',
                USER_INPUT_FIELD: 'Айди Т-карты',
                LOG_TITLE: 'Программные логи',
                LOG_ACTION1_TEXT: 'Нажата Кнопка 1',
                LOG_ACTION2_TEXT: 'Нажата Кнопка 2',
            }
        }

        self.current_language = 'ru'

        # Создание вертикального окна, кнопок, полей
        self.layout = QVBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setFixedWidth(self.width() * 0.25)  # Установка высоты поля ввода


        self.log_field = QTextEdit()
        self.log_field.setReadOnly(True)  # Запретить редактирование пользователем
        self.label = QLabel()

        self.button1 = QPushButton()
        self.button2 = QPushButton()
        self.send_text_button = QPushButton()

        # Привязка кнопок к функциям обработки событий
        self.button1.clicked.connect(self.handle_button1_click)
        self.button2.clicked.connect(self.handle_button2_click)
        self.send_text_button.clicked.connect(self.handle_send_text_click)


        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.log_field)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.send_text_button)

        # Список с языками
        self.language_selector = QComboBox()
        self.language_selector.addItem('Русский', 'ru')
        self.language_selector.addItem('English', 'en')
        self.language_selector.currentIndexChanged.connect(self.change_language)
        self.layout.addWidget(self.language_selector)
        self.setLayout(self.layout)

        self.resize(960, 540)

        # Подключение стилей
        self.apply_styles_from_file('static/styles/styles.qss')

        # Язык по умолчанию
        self.update_language()

    def handle_button1_click(self):
        self.log_action(self.translations[self.current_language][LOG_ACTION1_TEXT])

    def handle_button2_click(self):
        self.log_action(self.translations[self.current_language][LOG_ACTION2_TEXT])

    def handle_send_text_click(self):
        text = self.input_field.text()
        self.log_action(f"User input / Пользовательский ввод: {text}")
        self.input_field.clear()

    def log_action(self, message):
        self.log_field.append(message)

    # Функция подключения стилей
    def apply_styles_from_file(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                style_sheet = file.read()
            self.setStyleSheet(style_sheet)
        else:
            print(f"Style file '{file_name}' not found.")

    def update_language(self):
        """Обновляет текст на виджетах в зависимости от выбранного языка."""
        self.button1.setText(self.translations[self.current_language][BUTTON1_TEXT])
        self.button2.setText(self.translations[self.current_language][BUTTON2_TEXT])
        self.send_text_button.setText(self.translations[self.current_language][SEND_TEXT_BUTTON])
        self.label.setText(self.translations[self.current_language][LOG_TITLE])
        self.input_field.setPlaceholderText(self.translations[self.current_language][USER_INPUT_FIELD])

    def change_language(self, index):
        """Изменяет текущий язык и обновляет интерфейс."""
        language_code = self.language_selector.itemData(index)
        if language_code in self.translations:
            self.current_language = language_code
            self.update_language()
        else:
            print(f"Language '{language_code}' not found.")
