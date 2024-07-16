import os
import shutil
import winreg

def clean_unused_files(folder_path):
    # Здесь можно указать путь к папке, например, рабочему столу или директории загрузок
    #folder_path = "C:\\Users\\Username\\Desktop"
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Проверяем, был ли файл использован за последние 6 месяцев (можно изменить количество месяцев по своему усмотрению)
            if os.stat(file_path).st_mtime < (os.path.now() - (6 * 30 * 86400)):
                os.remove(file_path)

def clean_registry():
    key = winreg.HKEY_CURRENT_USER
    subkey = r"Software\SomeSoftware"  # Здесь указывается путь к соответствующему подключу в реестре
    with winreg.OpenKey(key, subkey, 0, winreg.KEY_ALL_ACCESS) as registry_key:
        # Здесь можно добавить код для удаления ненужных записей из реестра
        pass

def clean_temp_folder():
    temp_folder = "C:\\Windows\\Temp"
    for root, dirs, files in os.walk(temp_folder):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

# Теперь, когда у нас есть функции для очистки, мы можем выполнить их при необходимости:
# Пользователь указал очистку давно не используемых файлов
clean_unused_files()

# Пользователь указал очистку реестра от мусора
clean_registry()

# Очистка папки TEMP
clean_temp_folder()