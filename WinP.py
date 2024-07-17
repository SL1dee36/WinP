# created by Nazaryan Artem
# Github @sl1de36 | Telegram @slide36

from customtkinter import *
import tkinter as tk
from CTkMessagebox import CTkMessagebox
# from func.cnv import get_file_path
# from func.tmp import clean_unused_files,clean_registry,clean_temp_folder
from func.arh import compress_file, decompress_file
from webbrowser import open
import os
import sys
import threading
import win32com.client
import winreg


class WinPWindow(CTk):
    def __init__(self):
        super().__init__()
        """
        Initialize the application.

        Instantiate the WinPWindow class, set the window size to 300x400,
        and make it non-resizable.
        Also, load the functions frame.
        """
        self.title("WinP: F17E7")
        self.geometry("300x400")
        self.resizable(False, False)
        self.load_functions_frame()

    def function(self, name):
        """
        Handle the click event of a button to execute a specific function.

        When a button is clicked, the name of the button is passed to this function.
        It hides the main functions frame, creates a new frame for the selected function,
        executes the function associated with the button name, and displays a 'Back' button
        to return to the previous frame.
        """
        self.lf_frame.forget()
        self.fn_frame = CTkFrame(self, width=300, height=400)
        self.fn_frame.pack(padx=5, pady=5)
        self.fn_frame.propagate(0)

        fncs = {
            'ARH': self.load_arh_frame,
            'CNV': lambda: print("CNV"),
            'TMP': lambda: print("TMP")
        }

        if name in fncs:
            fncs[name]()

        bck_button = CTkButton(self.fn_frame, text="Back", command=lambda: self.load_functions_frame())
        bck_button.pack(padx=5, pady=5, side=BOTTOM)

    def load_functions_frame(self):
        """
        Load the main functions frame.

        If any secondary function frame (like archive frame) exists, it is forgotten (hidden).
        Then, a new frame is created to hold the main function buttons (Archive, Converter, Optimizer).
        """
        try:
            self.fn_frame.forget()
            self.arh_frame.forget()
        except:
            pass

        self.lf_frame = CTkFrame(self, width=300, height=400)
        self.lf_frame.pack(padx=5, pady=5)
        self.lf_frame.propagate(0)

        arh_button = CTkButton(self.lf_frame, text="Archivate", command=lambda: self.function("ARH"))
        arh_button.pack(padx=5, pady=5)
        cnv_button = CTkButton(self.lf_frame, text="Converter", command=lambda: self.function("CNV"))
        cnv_button.pack(padx=5, pady=5)
        tmp_button = CTkButton(self.lf_frame, text="Optimizer", command=lambda: self.function("TMP"))
        tmp_button.pack(padx=5, pady=5)

        dev_button = CTkButton(self.lf_frame, text="GitHub", command=lambda: open("https://github.com/SL1dee36"))
        dev_button.pack(padx=5, pady=5, side=BOTTOM)

    def load_arh_frame(self):
        """
        Loads the frame with archiving options.

        This function creates a frame for archive operations, including selecting a file/folder, choosing between 
        file and folder compression, optional password setting, and buttons for archive and extract operations.
        """
        self.lf_frame.forget()
        self.fn_frame.forget()

        self.arh_frame = CTkFrame(self, width=300, height=400)
        self.arh_frame.pack(padx=5, pady=5)
        self.arh_frame.propagate(0)

        self.file_path = ""
        self.target_type = StringVar(value="file")  # Default to file

        def select_target():
            """Opens a dialog to select a file or folder."""
            if self.target_type.get() == "file":
                self.file_path = filedialog.askopenfilename(initialdir="/", title="Select File")
            else:
                self.file_path = filedialog.askdirectory(initialdir="/", title="Select Folder")
            file_path_label.configure(text=self.file_path)

        # Button for selecting file/folder
        select_target_button = CTkButton(self.arh_frame, text="Select", command=select_target)
        select_target_button.pack(padx=5, pady=5)

        # Label to display the selected path
        file_path_label = CTkLabel(self.arh_frame, text="File/Folder not selected")
        file_path_label.pack(pady=5)

        # Radiobutton to choose between file and folder
        file_radiobutton = CTkRadioButton(self.arh_frame, text="File", variable=self.target_type, value="file")
        file_radiobutton.pack(pady=5)
        folder_radiobutton = CTkRadioButton(self.arh_frame, text="Folder", variable=self.target_type, value="folder")
        folder_radiobutton.pack(pady=5)

        # Checkbox to enable password usage
        self.use_password = IntVar(value=0)
        password_checkbox = CTkCheckBox(self.arh_frame, text="Use Password?", variable=self.use_password,
                                      command=self.toggle_password_entry)
        password_checkbox.pack(pady=5)

        # Entry field for password (initially disabled)
        self.password_entry = CTkEntry(self.arh_frame, placeholder_text="Enter Password", show="*", state="disabled")
        self.password_entry.pack(pady=5)

        # Functions for archiving and extracting
        def archive():
            if self.file_path:
                password = self.password_entry.get() if self.use_password.get() else None
                try:
                    compress_file(self.file_path, password)
                    CTkMessagebox(title="Success", message=f"File/folder '{self.file_path}' successfully archived.", option_1="OK")
                except Exception as e:
                    CTkMessagebox(title="Error", message=f"Error during archiving: {e}")

        def extract():
            if self.file_path:
                password = self.password_entry.get() if self.use_password.get() else None
                try:
                    decompress_file(self.file_path, password)
                    CTkMessagebox(title="Success", message=f"File/folder '{self.file_path}' successfully extracted.", option_1="OK")
                except RuntimeError as e:
                    CTkMessagebox(title="Error", message=f"Error during extraction: {e}")
                except Exception as e:
                    CTkMessagebox(title="Error", message=f"Error during extraction: {e}")

        # Buttons for archiving and extracting
        archive_button = CTkButton(self.arh_frame, text="Archive", command=archive)
        archive_button.pack(pady=5)
        extract_button = CTkButton(self.arh_frame, text="Extract", command=extract)
        extract_button.pack(pady=5)

        # "Back" button
        bck_button = CTkButton(self.arh_frame, text="Back", command=lambda: self.load_functions_frame())
        bck_button.pack(padx=5, pady=5, side=BOTTOM)

    def toggle_password_entry(self):
        """Enables/disables password entry field."""
        if self.use_password.get():
            self.password_entry.configure(state="normal")
        else:
            self.password_entry.configure(state="disabled")

    def CNV():
        pass

    def TMP():
        pass


def compress_selected():
    """Archives selected files or folders in a separate thread.

    This function is intended to be called from the context menu integration. 
    It retrieves the selected files/folders from the command line arguments and 
    archives each of them. Error messages are displayed using CTkMessagebox.
    """
    def archive_thread(items):
        """Function for performing archiving in a separate thread."""
        if not items:
            root = tk.Tk()
            root.withdraw()
            CTkMessagebox(title="Error", message="No file or folder selected.")
            root.mainloop()
            return

        for item in items:
            try:
                compress_file(item)
                root = tk.Tk()
                root.withdraw()
                CTkMessagebox(title="Success", message=f"'{item}' successfully archived.")
                root.mainloop()
            except Exception as e:
                root = tk.Tk()
                root.withdraw()
                CTkMessagebox(title="Error", message=f"Error archiving '{item}': {e}")
                root.mainloop()

    # Create and start a separate thread for archiving
    thread = threading.Thread(target=archive_thread, args=(sys.argv[1:],))
    thread.start()
    thread.join()  # Wait for the thread to complete


def extract_selected():
    """Extracts selected archive files in a separate thread.

    Similar to `compress_selected`, this function handles the context menu action
    for extraction. It iterates through the provided file paths, attempting to
    decompress each one. Any errors encountered during extraction are displayed
    using CTkMessagebox. 
    
    This version also filters the provided file paths to only process files with
    the extensions .zis, .zip, or .7zip.
    """
    def extract_thread(items):
        """Function to perform extraction in a separate thread."""
        if not items:
            root = tk.Tk()
            root.withdraw()
            CTkMessagebox(title="Error", message="No file or folder selected.")
            root.mainloop()
            return

        for item in items:
            print(item)
            # Check if the file has a valid archive extension
            if not any(item.lower().endswith(ext) for ext in ['.zis', '.zip', '.7zip']):
                root = tk.Tk()
                root.withdraw()
                CTkMessagebox(title="Error", message=f"Unsupported file type: '{item}'")
                root.mainloop()
                continue  # Skip to the next file

            try:
                decompress_file(item)
                root = tk.Tk()
                root.withdraw()
                CTkMessagebox(title="Success", message=f"'{item}' successfully extracted.")
                root.mainloop()
            except RuntimeError as e:  # Catch potential password errors
                root = tk.Tk()
                root.withdraw()
                CTkMessagebox(title="Error", message=f"Error extracting '{item}': {e}")
                root.mainloop()
            except Exception as e:
                root = tk.Tk()
                root.withdraw()
                CTkMessagebox(title="Error", message=f"Error extracting '{item}': {e}")
                root.mainloop()
    #  Исправление: начинаем с индекса 2, чтобы получить пути к файлам
    file_paths = sys.argv[2:]  

    # Create and start a separate thread for extraction
    thread = threading.Thread(target=extract_thread, args=(file_paths,))
    thread.start()
    thread.join()  # Wait for the thread to complete

def create_reg_key():
    """Creates a registry entry for the context menu."""
    try:
        python_path = sys.executable
        script_path = os.path.abspath(__file__)

        key_paths = {
            "Archive File with WinP": r"Software\Classes\*\shell\ArchiveFile",
            "Archive Folder with WinP": r"Software\Classes\Folder\shell\ArchiveFolder"
        }

        # Use unique keys for each file type
        extract_key_paths = {
            "Extract with WinP (.zis)": r"Software\Classes\.zis\shell\ExtractFile",
            "Extract with WinP (.zip)": r"Software\Classes\.zip\shell\ExtractFile",
            "Extract with WinP (.7z)": r"Software\Classes\.7z\shell\ExtractFile"
        }

        for menu_text, key_path in key_paths.items():
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, menu_text)
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f"{script_path},0")

            command_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path + r"\command")
            winreg.SetValueEx(command_key, "", 0, winreg.REG_SZ,
                             f"\"{python_path}\" \"{script_path}\" \"%1\"")
            winreg.CloseKey(command_key)
            winreg.CloseKey(key)

        for menu_text, key_path in extract_key_paths.items():
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, menu_text)
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f"{script_path},0")

            command_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path + r"\command")
            winreg.SetValueEx(command_key, "", 0, winreg.REG_SZ,
                             f"\"{python_path}\" \"{script_path}\" \"extract\" \"%1\"")
            winreg.CloseKey(command_key)
            winreg.CloseKey(key)

        return True
    except Exception as e:
        print(f"Error creating registry key: {e}")
        return False


def delete_reg_key():
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
            r"Software\Classes\.7z\shell\ExtractFile"
        ]

        for key_path in key_paths:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path + r"\command")
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
        return True
    except FileNotFoundError:
        return True  # Key not found - this is normal
    except Exception as e:
        print(f"Error deleting registry key: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "extract":  # Check for "extract" 
        extract_selected()
    elif len(sys.argv) > 1: # If there are arguments, assume it's for archiving
        compress_selected()
    else:
        if delete_reg_key() and create_reg_key():
            print("Registry entry successfully updated.")
        else:
            print("Error updating registry entry.")

        app = WinPWindow()
        app.mainloop()