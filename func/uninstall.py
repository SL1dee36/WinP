import winreg

def delete_reg_key():
    """Удаляет записи WinP из реестра."""
    try:
        key_paths = [
            r"Software\Classes\*\shell\ArchiveFile",
            r"Software\Classes\Folder\shell\ArchiveFolder",
            r"Software\Classes\.zis\shell\ExtractFile",
            r"Software\Classes\.zip\shell\ExtractFile",
            r"Software\Classes\.7z\shell\ExtractFile"
        ]

        for key_path in key_paths:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path + r"\command")
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
        print("Записи WinP успешно удалены из реестра.")
        return True
    except FileNotFoundError:
        print("Записи WinP не найдены в реестре.")
        return True  # Ключ не найден - это нормально
    except Exception as e:
        print(f"Ошибка при удалении ключей реестра: {e}")
        return False

if __name__ == "__main__":
    delete_reg_key()