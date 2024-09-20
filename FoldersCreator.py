import os
from datetime import datetime

RESPONSE_EN = "Folder creation completed successfully!"
RESPONSE_RU = "Создание папок успешно завершено!"

def create_folders(path, language, column_date, row_date_start, row_date_end, column_eqp, column_cards_id):
    try:
        import openpyxl
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        iot_france_folder = os.path.join(desktop_path, "IOT")

        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active

        # Получаем индексы столбцов
        date_col_index = openpyxl.utils.cell.column_index_from_string(column_date) - 1
        name_col_index = openpyxl.utils.cell.column_index_from_string(column_eqp) - 1
        cards_id_index = openpyxl.utils.cell.column_index_from_string(column_cards_id) - 1

        current_date = None
        current_date_folder = None

        for row in sheet.iter_rows(min_row=int(row_date_start), max_row=int(row_date_end),
                                   values_only=True):  # Читаем строки
            date_cell = row[date_col_index]  # Получаем значение из столбца с датами
            name_cell = row[name_col_index]  # Получаем значение из столбца с именами
            card_id_cell = row[cards_id_index].split(", ")  # Получаем значение из столбца с айди

            if isinstance(date_cell, datetime):
                folder_name = date_cell.strftime('%d.%m.%Y')
                current_date_folder = os.path.join(iot_france_folder, folder_name)

                if not os.path.exists(current_date_folder):
                    os.makedirs(current_date_folder)

                current_date = folder_name  # Обновляем текущую дату

            subfolder_path = ""

            if current_date and name_cell:
                subfolder_path = os.path.join(current_date_folder, str(name_cell))

                if not os.path.exists(subfolder_path):
                    os.makedirs(subfolder_path)

            if card_id_cell:
                for item in card_id_cell:
                    folder_cards_path = os.path.join(subfolder_path, str(item))

                    if not os.path.exists(folder_cards_path):
                        os.makedirs(folder_cards_path)

        workbook.close()
        return RESPONSE_EN if language == "en" else RESPONSE_RU

    except Exception as inst:
        return str(inst)
