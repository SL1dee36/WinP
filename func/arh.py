import os
import zipfile
import zlib

def compress_file(filename, password=None):
  """
  Архивирует файл или папку с максимальным сжатием и паролем (опционально).

  Args:
      filename: Путь к файлу или папке для архивации.
      password: Пароль для архива (по умолчанию None).
  """

  filename_base, filename_ext = os.path.splitext(filename)
  archive_name = f"{filename_base}.zis"
  print(f"Пытаюсь создать архив: {archive_name}") 
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
  except Exception as e:
      print(f"Ошибка при архивации: {e}")

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

    except RuntimeError as e:
        print(f"Ошибка при разархивации: {e}")
    except Exception as e:
        print(f"Ошибка при разархивации: {e}")

if __name__ == "__main__":
  action = input("Выберите действие (1 - архивировать, 2 - разархивировать): ")
  filename = input("Введите путь к файлу/папке: ")

  if action == "1":
    use_password = input("Использовать пароль? (да/нет): ")
    if use_password.lower() == "да":
      password = input("Введите пароль: ")
    else:
      password = "default"
    compress_file(filename, password)
    print(f"Файл/папка '{filename}' успешно архивирован в '{filename}.zip'")
  elif action == "2":
    use_password = input("Архив защищен паролем? (да/нет): ")
    if use_password.lower() == "да":
      password = input("Введите пароль: ")
    else:
      password = None
    decompress_file(filename, password)
    print(f"Файл/папка '{filename}' успешно разархивирован.")
  else:
    print("Неверный выбор действия.")