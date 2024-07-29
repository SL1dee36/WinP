import os
import zipfile
import zlib
from CTkMessagebox import CTkMessagebox

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