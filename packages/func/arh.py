import os
import zipfile
import zlib
from CTkMessagebox import CTkMessagebox
import winreg
import subprocess
import time

def compress_file(filename, password=None):
  """
  Архивирует файл или папку с максимальным сжатием и паролем (опционально).

  Args:
      filename: Путь к файлу или папке для архивации.
      password: Пароль для архива (по умолчанию None).
  """

  filename_base, filename_ext = os.path.splitext(filename)
  archive_name = f"{filename_base}.zis" 
  try:
    with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        if os.path.isdir(filename):  # Если это папка
            for root, _, files in os.walk(filename):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, filename)
                    zipf.write(full_path, arcname, zipfile.ZIP_DEFLATED)
        else:  # Если это файл
            zipf.write(filename, os.path.basename(filename), zipfile.ZIP_DEFLATED)

        if password:
            zipf.setpassword(password.encode())
    CTkMessagebox(title="Success", message=f"'{filename}' successfully archived.")
  except Exception as e:
      CTkMessagebox(title="Error", message=f"Error archiving: {e}")

def decompress_file(filename, password=None):
    """
    Разархивирует файл .zis.

    Args:
        filename: Путь к файлу .zis для разархивации.
        password: Пароль для архива (по умолчанию None).
    """

    try:
        with zipfile.ZipFile(filename, "r") as zipf:
            if password:
                zipf.setpassword(password.encode())

            # Получаем имя папки из имени архива
            output_dir = os.path.splitext(filename)[0]

            # Создаем папку, если она не существует
            os.makedirs(output_dir, exist_ok=True) 

            # Извлекаем все файлы в папку
            zipf.extractall(path=output_dir) 
        CTkMessagebox(title="Success", message=f"'{filename}' successfully extracted.")
    except RuntimeError as e:
        CTkMessagebox(title="Error", message=f"Error extracting '{filename}': {e}")
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Error extracting '{filename}': {e}")

def restart_explorer():
    """Перезапускает процесс explorer.exe."""
    try:
        # Завершаем процесс explorer.exe
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], check=True)

        # Небольшая задержка, чтобы процесс успел завершиться
        time.sleep(2)

        # Запускаем explorer.exe заново
        subprocess.Popen(["explorer.exe"])

        print("Процесс explorer.exe перезапущен.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при перезапуске explorer.exe: {e}")

def set_icon_for_extension(extension, icon_path):
    """
    Устанавливает иконку для указанного расширения файла в реестре Windows.

    Args:
        extension: Расширение файла (например, ".txt", ".zis").
        icon_path: Полный путь к файлу иконки (например, "C:\\MyIcons\\icon.ico").
    """

    try:

        # Открываем ключ расширения файла в реестре
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, extension)
        winreg.CloseKey(key)  # Закрываем ключ, чтобы изменения вступили в силу

        # Открываем ключ DefaultIcon
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{extension}\\DefaultIcon")
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, icon_path)  # Устанавливаем путь к иконке
        winreg.CloseKey(key)

        print(f"Иконка для расширения {extension} успешно установлена.")

        restart_explorer()

    except WindowsError as e:
        print(f"Ошибка при установке иконки: {e}")