# created by Nazaryan Artem
# Github @sl1de36 | Telegram @slide36

import os
from arh import compress_file, decompress_file
from webbrowser import open
import subprocess
import os
import sys
import winreg


def create_reg_key(type=None):
    """Creates a registry entry for the context menu."""
    try:
        python_path = sys.executable
        script_path = os.path.abspath(__file__)

        key_paths = {
            "Archive File with WinP": r"Software\Classes\*\shell\ArchiveFile",
            "Archive Folder with WinP": r"Software\Classes\Folder\shell\ArchiveFolder",
        }

        # Use unique keys for each file type
        extract_key_paths = {
            "Extract with WinP (.zis)": r"Software\Classes\.zis\shell\ExtractFile",
            "Extract with WinP (.zip)": r"Software\Classes\.zip\shell\ExtractFile",
            "Extract with WinP (.7z)": r"Software\Classes\.7z\shell\ExtractFile",
        }

        for menu_text, key_path in key_paths.items():
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, menu_text)
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f"{script_path},0")

            command_key = winreg.CreateKey(
                winreg.HKEY_CURRENT_USER, key_path + r"\command"
            )
            winreg.SetValueEx(
                command_key,
                "",
                0,
                winreg.REG_SZ,
                f'"{python_path}" "{script_path}" "%1"',
            )
            winreg.CloseKey(command_key)
            winreg.CloseKey(key)

        for menu_text, key_path in extract_key_paths.items():
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, menu_text)
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f"{script_path},0")

            command_key = winreg.CreateKey(
                winreg.HKEY_CURRENT_USER, key_path + r"\command"
            )
            winreg.SetValueEx(
                command_key,
                "",
                0,
                winreg.REG_SZ,
                f'"{python_path}" "{script_path}" "extract" "%1"',
            )
            winreg.CloseKey(command_key)
            winreg.CloseKey(key)

        return True
    except Exception as e:
        print(f"Error creating registry key: {e}")
        return False


def delete_reg_key(type=None):
    """Deletes existing registry entries.

    This function now removes the incorrect entry that was associated with folders
    and adds the removal of the specific file type entries.
    """

    try:
        key_paths = [
            r"Software\Classes\*\shell\ArchiveFile",
            r"Software\Classes\Folder\shell\ArchiveFolder",
            r"Software\Classes\.zis\shell\ExtractFile",
            r"Software\Classes\.zip\shell\ExtractFile",
            r"Software\Classes\.7z\shell\ExtractFile",
        ]

        for key_path in key_paths:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path + r"\command")
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
        if type:
            print("Done")
        return True
    except FileNotFoundError:
        return True  # Key not found - this is normal
    except Exception as e:
        print(f"Error deleting registry key: {e}")
        return False