# created by Nazaryan Artem
# Github @sl1de36 | Telegram @slide36

import os
from packages.func.arh import compress_file, decompress_file
import subprocess
import os
import sys
import winreg
import tkinter as tk
import threading
from tkinter import filedialog
from customtkinter import *
from CTkMessagebox import CTkMessagebox
import win32com.client


def archive_thread(items, password=None):
    """Function for performing archiving in a separate thread."""
    try:
        for item in items:
            compress_file(item, password)
            CTkMessagebox(title="Success", message=f"'{item}' successfully archived.")

            # Открываем папку с архивом
            folder_path = os.path.dirname(item)
        subprocess.Popen(f'explorer /select,"{folder_path}"')
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Error archiving: {e}")



def extract_thread(items, password=None):
    """Function to perform extraction in a separate thread."""
    try:
        for item in items:
            # Check if the file has a valid archive extension
            if not any(item.lower().endswith(ext) for ext in [".zis", ".zip", ".7zip"]):
                CTkMessagebox(title="Error", message=f"Unsupported file type: '{item}'")
                return  # Skip to the next file

            decompress_file(item, password)
            CTkMessagebox(title="Success", message=f"'{item}' successfully extracted.")
 
            # Открываем папку с распакованными файлами
            file_path = os.path.splitext(item)[0]
        subprocess.Popen(f'explorer /select,"{file_path}"')
    except RuntimeError as e:  # Catch potential password errors
        CTkMessagebox(title="Error", message=f"Error extracting '{item}': {e}")
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Error extracting '{item}': {e}")


def create_reg_key(type=None):
    """Creates a registry entry for the context menu."""
    try:
        python_path = sys.executable
        # Use sys.argv[0] to get the correct script path
        script_path = os.path.abspath(sys.argv[0])

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

        # --- Изменения в этой части ---
        for menu_text, key_path in key_paths.items():
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, menu_text)
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f"{script_path},0")

            command_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path + r"\command")
            # Передаем 'archive' как аргумент:
            winreg.SetValueEx(
                command_key,
                "",
                0,
                winreg.REG_SZ,
                f'"{python_path}" "{script_path}" "archive"  "%1"', 
            )
            winreg.CloseKey(command_key)
            winreg.CloseKey(key)

        for menu_text, key_path in extract_key_paths.items():
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, menu_text)
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f"{script_path},0")

            command_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path + r"\command")
            # Передаем 'extract' как аргумент:
            winreg.SetValueEx(
                command_key,
                "",
                0,
                winreg.REG_SZ,
                f'"{python_path}" "{script_path}" "extract" "%1"',
            )
            winreg.CloseKey(command_key)
            winreg.CloseKey(key)
        # --- Конец изменений ---

        return True
    except Exception as e:
        print(f"Error creating registry key: {e}")
        return False


def delete_reg_key(type=None):
    """Deletes existing registry entries."""
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