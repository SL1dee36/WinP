import os
import zipfile
import zlib

def compress_file(filename, password=None):
  """
  Архивирует файл с максимальным сжатием и паролем (опционально).

  Args:
      filename: Путь к файлу для архивации.
      password: Пароль для архива (по умолчанию None).
  """

  filename_base, filename_ext = os.path.splitext(filename)
  archive_name = f"{filename_base}.zis"

  try:
    # Создаем папку .zis, если она не существует
    os.mkdir(archive_name)

    # Получаем список файлов для архивации (рекурсивно для папок)
    files_to_archive = []
    if os.path.isfile(filename):
      files_to_archive.append(filename)
    elif os.path.isdir(filename):
      for root, _, files in os.walk(filename):
        for file in files:
          files_to_archive.append(os.path.join(root, file))

    # Архивируем файлы
    with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED) as zipf:
      for file in files_to_archive:
        arcname = os.path.relpath(file, filename)  # Сохраняем структуру папок
        zipf.write(file, arcname, zipfile.ZIP_DEFLATED)
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
      zipf.extractall()
  except RuntimeError as e:
    print(f"Ошибка при разархивации: неверный пароль.")
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
    print(f"Файл/папка '{filename}' успешно архивирован в '{filename}.zis'")
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