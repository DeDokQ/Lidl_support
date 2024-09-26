import os
import shutil
from glob import glob


def copy_latest_files(target_folder_name, is_folder, is_screenshot):
    try:
        user_folder = os.path.expanduser("~")

        config_folder = "C:\\SEGGER\\Flashingtool\\config"
        merged_hex_folder = "C:\\SEGGER\\Flashingtool\\mergedHex"

        log = ""

        desktop_path = os.path.join(user_folder, "Desktop")
        for root, dirs, files in os.walk(desktop_path):
            for folder in dirs:
                if target_folder_name in folder and target_folder_name == folder:
                    target_folder = os.path.join(root, folder)
                    break
            else:
                continue
            break
        else:
            log += (f"Папка с именем '{target_folder_name}' не найдена на рабочем столе.\n"
                    f"A folder named '{target_folder_name}' was not found on the desktop.\n\n")
            return log

        config_files = glob(os.path.join(config_folder, '*'))
        if len(config_files) == 0:
            log += ("Нет файлов для копирования в папке конфигураций.\n"
                    "There are no files to copy in the configurations folder.\n\n")
            return log

        latest_files = sorted(config_files, key=os.path.getmtime, reverse=True)[:2]
        if len(latest_files) < 2:
            log += ("Недостаточно файлов для копирования (меньше двух файлов в папке конфигураций).\n"
                    "There are not enough files to copy (less than two files in the configuration folder).\n\n")
            return log

        log += (f"Файлы для копирования из config: {latest_files}\n"
                f"Files to copy from config: {latest_files}\n\n")

        for file in latest_files:
            if target_folder_name in os.path.basename(file):
                shutil.copy(file, target_folder)
                log += (f"Скопирован файл из config: {file}\n"
                        f"A file was copied from config: {file}\n\n")
            else:
                log += ("Ошибка копирования из config.\n"
                        "Copy error from config.\n\n")
                return log

        merged_hex_files = glob(os.path.join(merged_hex_folder, '*'))
        if len(merged_hex_files) == 0:
            log += ("Нет файлов для копирования в папке mergedHex.\n"
                    "There are no files to copy in the mergedHex folder.\n\n")
            return log

        latest_merged_file = sorted(merged_hex_files, key=os.path.getmtime, reverse=True)[0]
        if target_folder_name in os.path.basename(latest_merged_file):
            shutil.copy(latest_merged_file, target_folder)
            log += (f"Скопирован файл из mergedHex: {latest_merged_file}\n"
                    f"A file was copied from mergedHex: {latest_merged_file}\n\n")
        else:
            log += ("Ошибка копирования из mergedHex.\n"
                    "Copy error from mergedHex.\n\n")
            return log

        def screenshot_creator():
            import time
            from pygetwindow import getWindowsWithTitle, getAllTitles
            import re
            from PIL import ImageGrab
            windows = getAllTitles()

            window = None
            for title in windows:
                if re.search(r'Hex Merge Tool', title):
                    window = getWindowsWithTitle(title)[0]
                    window.restore()

                    # Развернуть на весь экран
                    window.maximize()

                    # Активируем окно
                    window.activate()
                    break

            # Если окно не найдено
            if window is None:
                return "Окно 'Hex Merge Tool' не найдено"

            application_helper = getWindowsWithTitle("Hex Merge Helper")

            if application_helper:
                application_helper[0].minimize()

                time.sleep(0.5)

                screenshot = ImageGrab.grab()
                full_name = target_folder_name + ".png"
                screenshot.save(os.path.join(target_folder, full_name))

                if is_screenshot:
                    os.startfile(os.path.join(target_folder, full_name))

                application_helper[0].restore()

            else:
                return "Окно 'Hex Merge Helper' не найдено"

            window.minimize()

        screenshot_creator()

        # открываем папку с скопированными файлами
        log += ("Файлы успешно скопированы!\n"
                "The files have been successfully copied!\n\n")
        if is_folder:
            os.startfile(target_folder)

        return log

    except Exception as e:
        return f"Произошла ошибка: {e}"
