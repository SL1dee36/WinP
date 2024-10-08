# created by Nazaryan Artem
# Github @sl1de36 | Telegram @slide36

import os
import tkinter as tk
from tkinter import filedialog
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from packages.func.arh import compress_file, decompress_file
from packages.func.tmp import *
from packages.func.ctmenu import *
import webbrowser
import subprocess
import os
import sys
import win32com.client
import win32con
import win32api
import winreg
import tempfile
from pathlib import Path
from PIL import Image
import moviepy.editor as mp
from pydub import AudioSegment
import threading
import time
import pystray
from PIL import Image
import json
import datetime
import shutil
import gc
import shutil
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import pywinstyles

from packages.data.lang import translations

class WinPWindow(CTk):
    def __init__(self):
        super().__init__()

        self.current_language = "en"  # Default language
        self.title("WinP: F24e7")

        try: self.iconbitmap("assets/winp.ico") 
        except: 
            try: self.iconbitmap("_internal/winp.ico")  
            except: pass

        self.geometry("300x400")
        self.resizable(False, False)

        self.lf_frame    = None
        self.fn_frame    = None
        self.arh_frame   = None
        self.cnv_frame_l = None
        self.cnv_frame_m = None
        self.cnv_frame_r = None
        self.stg_frame   = None
        self.tmp_frame   = None
        self.tmp_frame_r = None

        self.Extended_menu = False

        self.load_settings()
        self.load_functions_frame()
        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )  # Вызов on_closing при закрытии

    def load_settings(self):
        """Loads settings from settings.json."""
        settings_path = "packages/data/settings.json"
        try:
            with open(settings_path, "r") as f:
                settings = json.load(f)
                self.current_language = settings.get("language", "en")
                self.run_on_startup = settings.get("run_on_startup", False)
        except FileNotFoundError:
            # If settings file not found, use default settings and create the file
            self.current_language = "en"
            self.run_on_startup = False
            self.save_settings()

    def save_settings(self):
        """Saves settings to settings.json."""
        settings_path = "packages/data/settings.json"
        settings = {
            "language": self.current_language,
            "run_on_startup": self.run_on_startup,
        }
        with open(settings_path, "w") as f:
            json.dump(settings, f, indent=4) # Добавляем indent для читаемости

    def change_language(self, new_language):
        self.current_language = new_language
        self.update_language()
        self.save_settings()  # Сохраняем настройки после смены языка

    def update_language(self):
        self.update_widget_language(self)

        for frame in [
            self.lf_frame,
            self.fn_frame,
            self.arh_frame,
            self.cnv_frame_l,
            self.cnv_frame_m,
            self.cnv_frame_r,
            self.stg_frame,
            self.tmp_frame,
        ]:
            try:
                self.update_widget_language(frame)
            except AttributeError:
                pass

    def update_widget_language(self, widget):
        if hasattr(widget, "configure") and "text" in widget.keys():
            original_text = widget.cget("text")
            translated_text = translations[self.current_language].get(
                original_text, original_text
            )
            widget.configure(text=translated_text)
        for child in widget.winfo_children():
            self.update_widget_language(child)
    
    def create_system_tray_icon(self):
        """Создает иконку в системном трее."""

        def on_quit():
            self.icon.stop()  # Останавливаем иконку перед выходом
            self.destroy()
            os._exit(0)

        def on_show_window():
            self.deiconify()  # Показываем окно
            self.icon.stop()  # Убираем из трея

        # Загружаем иконку (замените на путь к вашей иконке)
        try: icon_image = Image.open(r"assets\winp.ico")
        except:
            try: icon_image = Image.open(r"_internal\winp.ico")
            except: on_show_window()
            
        # Создаем меню для иконки
        menu = pystray.Menu(
            pystray.MenuItem(translations[self.current_language]["Show"], on_show_window),
            pystray.MenuItem(translations[self.current_language]["Exit"], on_quit),
        )

        # Создаем иконку, используя только Image
        self.icon = pystray.Icon("WinP", icon_image, "WinP", menu)
        self.icon.run()
    
    def on_closing(self):
        """Функция, вызываемая при закрытии окна."""
        result = CTkMessagebox(
            title=translations[self.current_language]["Confirmation"],
            message=translations[self.current_language][
                "Are you sure you want to close the app?"
            ],
            icon="question",
            option_1=translations[self.current_language]["Exit"],
            option_2=translations[self.current_language]["Minimize to tray"],
            option_3=translations[self.current_language]["Cancel"],
        ).get()

        if result == translations[self.current_language]["Exit"]:
            self.destroy()
            os._exit(0)
        elif result == translations[self.current_language]["Minimize to tray"]:
            self.withdraw()  # Скрываем окно
            self.create_system_tray_icon()

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
            "ARH": self.load_arh_frame,
            "CNV": self.load_cnv_frame,
            "TMP": self.load_tmp_frame,
            "STG": self.load_stg_frame,
        }

        if name in fncs:
            fncs[name]()

        bck_button = CTkButton(
            self.fn_frame, text=translations[self.current_language]["Back"], command=lambda: self.load_functions_frame()
        )
        bck_button.pack(padx=5, pady=5, side=BOTTOM)

    def clear_frame(self):
        
        for frame in [self.stg_frame, self.fn_frame, self.arh_frame, 
                      self.cnv_frame_l, self.cnv_frame_m, self.cnv_frame_r, 
                      self.lf_frame, self.tmp_frame, self.tmp_frame_r]:
            try:
                frame.forget()
            except AttributeError:
                pass
        
        self.Extended_menu = False
        self.geometry("300x400")

    def load_functions_frame(self):
        """
        Load the main functions frame.

        If any secondary function frame (like archive frame) exists, it is forgotten (hidden).
        Then, a new frame is created to hold the main function buttons (Archive, Converter, Optimizer).
        """
        self.clear_frame()
        self.lf_frame = CTkFrame(self, width=300, height=400)
        self.lf_frame.pack(padx=5, pady=5)
        self.lf_frame.propagate(0)

        arh_button = CTkButton(
            self.lf_frame, text=translations[self.current_language]["Archivate"], command=lambda: self.function("ARH")
        )
        arh_button.pack(padx=5, pady=5)
        cnv_button = CTkButton(
            self.lf_frame, text=translations[self.current_language]["Converter"], command=lambda: self.function("CNV")
        )
        cnv_button.pack(padx=5, pady=5)
        tmp_button = CTkButton(
            self.lf_frame, text=translations[self.current_language]["Optimizer"], command=lambda: self.function("TMP")
        )
        tmp_button.pack(padx=5, pady=5)
        stg_button = CTkButton(
            self.lf_frame, text=translations[self.current_language]["Settings"], command=lambda: self.function("STG")
        )
        stg_button.pack(padx=5, pady=5)

        dev_button = CTkButton(self.lf_frame,text=translations[self.current_language]["GitHub"],command=lambda: webbrowser.open("https://github.com/SL1dee36"))
        dev_button.pack(padx=5, pady=5, side=BOTTOM)

        # Translate initial text
        self.update_language() 

    def load_tmp_frame(self):
        """Loads the frame with optimization options."""
        self.clear_frame()
        self.geometry("900x400")

        self.tmp_frame = CTkFrame(self, width=300, height=400)
        self.tmp_frame.pack(padx=5, pady=5,side=LEFT)
        self.tmp_frame.propagate(0)

        self.tmp_frame_r = CTkFrame(self, width=600, height=400, corner_radius=0)
        self.tmp_frame_r.pack(side=LEFT)
        self.tmp_frame_r.propagate(0)

        # Buttons for each optimization action
        clear_temp_button = CTkButton(
            self.tmp_frame,
            text=translations[self.current_language]["Clear Temp Folder"],
            command=lambda: self.handle_clear_temp_folder(),
        )
        clear_temp_button.pack(pady=10)

        check_registry_button = CTkButton(
            self.tmp_frame,
            text=translations[self.current_language]["Check Registry"],
            command=lambda: self.handle_check_registry(),
        )
        check_registry_button.pack(pady=10)

        free_ram_button = CTkButton(
            self.tmp_frame,
            text=translations[self.current_language]["Free Up RAM"],
            command=lambda: self.handle_free_ram(),
        )
        free_ram_button.pack(pady=10)

        # "Back" button
        bck_button = CTkButton(
            self.tmp_frame,
            text=translations[self.current_language]["Back"],
            command=lambda: self.load_functions_frame(),
        )
        bck_button.pack(padx=5, pady=5, side=BOTTOM)

# График использования RAM
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tmp_frame_r)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.ani = animation.FuncAnimation(self.fig, self.update_graph, interval=1000)
        self.show_used_processes()
        
    def show_used_processes(self):
        self.tmp_scrlb_frame = CTkScrollableFrame(self.tmp_frame_r,width=600)
        self.tmp_scrlb_frame.pack(padx=5,pady=5,side=BOTTOM)
        #self.tmp_scrlb_frame.propagate(0)
        for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent']):
            try:
                process = proc.info
                label = CTkLabel(master=self.tmp_scrlb_frame, text=f"PID: {process['pid']}, Name: {process['name']}, User: {process['username']}, RAM: {process['memory_percent']:.1f}%")
                label.pack(anchor="w")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def update_graph(self, i):
        """Обновляет данные графика использования RAM."""
        self.ax.clear()
        ram = psutil.virtual_memory()
        self.ax.bar(["Used", "Free"], [ram.percent, 100 - ram.percent])
        self.ax.set_ylim(0, 100)
        self.ax.set_ylabel("RAM Usage (%)")
        self.ax.set_title("Real-Time RAM Usage")

    def handle_clear_temp_folder(self):
        deleted_files, errors = clear_temp_folder()
        if deleted_files:
            deleted_message = "\n".join(
                [f"{filename} - {translations[self.current_language]['deleted']}" for filename in deleted_files]
            )
            self.show_success(deleted_message)
        if errors:
            error_message = "\n".join(
                [f"{translations[self.current_language]['Failed to delete']} {filename}. {e}" for filename, e in errors]
            )
            self.show_error(error_message)

    def handle_check_registry(self):
        success, result = check_registry()
        if success:
            if result:
                issues_str = "\n".join(result)
                self.show_error(
                    f"{translations[self.current_language]['Registry issues found:']}\n{issues_str}"
                )
            else:
                self.show_success(translations[self.current_language]["No registry issues found."])
        else:
            self.show_error(f"{translations[self.current_language]['Failed to check registry']}. {result}") 

    def handle_free_ram(self):
        result = free_ram()
        if result:
            self.show_info(
                translations[self.current_language]["RAM cleaning attempt completed."]
            )
        else:
            self.show_error(translations[self.current_language]["Failed to free RAM"])

    def show_error(self, message):
        """Shows an error message box."""
        CTkMessagebox(
            title=translations[self.current_language]["Error"],
            message=message,
            icon="cancel",
        )

    def show_success(self, message):
        """Shows a success message box."""
        CTkMessagebox(
            title=translations[self.current_language]["Success"],
            message=message,
            icon="check",
        )

    def show_info(self, message):
        """Shows an information message box."""
        CTkMessagebox(
            title=translations[self.current_language]["Information"],
            message=message,
            icon="info",
        )





    def load_cnv_frame(self):
        """Loads the frame for file conversion with input and output options."""
        self.clear_frame()
        self.geometry("710x400")

        self.cnv_frame_l = CTkFrame(self, width=300, height=400)
        self.cnv_frame_l.pack(padx=5, pady=5, side=LEFT)
        self.cnv_frame_l.propagate(0)

        self.cnv_frame_m = CTkFrame(self, width=400, height=400, corner_radius=0)
        self.cnv_frame_m.pack(side=LEFT)
        self.cnv_frame_m.propagate(0)

        self.cnv_frame_r = CTkFrame(self, width=400, height=400)
        self.cnv_frame_r.pack(padx=5, pady=5, side=LEFT)
        self.cnv_frame_r.propagate(0)

        # --- Left Frame (File Input) ---

        def select_file():
            """Opens a dialog to select a file and updates the file path label."""
            self.file_path = filedialog.askopenfilename(
                initialdir="/",
                title=translations[self.current_language]["Select File"],
            )
            if self.file_path:
                display_file_info()
            # Update conversion options based on selected file type
            update_conversion_options()

        def display_file_info():
            """Displays file information in the file_info_label."""
            if not self.file_path:  # Check if a file is selected
                return

            file_name = os.path.basename(self.file_path)
            file_size = os.path.getsize(self.file_path)
            file_type = os.path.splitext(self.file_path)[1].lower()

            # Get creation, modification, and last open times
            file_create_timestamp = os.path.getctime(self.file_path)
            file_modify_timestamp = os.path.getmtime(self.file_path)
            file_access_timestamp = os.path.getatime(self.file_path)

            # Convert timestamps to readable format
            file_create_data = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(file_create_timestamp)
            )
            file_update_data = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(file_modify_timestamp)
            )
            file_last_open_data = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(file_access_timestamp)
            )

            # Get file attributes
            file_modify = oct(os.stat(self.file_path).st_mode)[-3:]
            if file_modify == "666":
                file_modify = "None"

            file_info_text = (
                f"{translations[self.current_language]['File']} : {file_name}\n"
                f"{translations[self.current_language]['Type']} : {file_type}\n"
                f"{translations[self.current_language]['Size']} : {file_size} байт\n"
                f"{translations[self.current_language]['On disk']} : {file_size} байт\n"
                f"---------------------------\n"
                f"{translations[self.current_language]['Created']} : {file_create_data}\n"
                f"{translations[self.current_language]['Modified']} : {file_update_data}\n"
                f"{translations[self.current_language]['Opened']} : {file_last_open_data}\n"
                f"---------------------------\n"
                f"{translations[self.current_language]['Attributes']} : {file_modify}\n"
            )
            self.file_info_label.configure(text=file_info_text, justify=LEFT)

        # Button to select a file
        select_file_button = CTkButton(
            self.cnv_frame_l,
            text=translations[self.current_language]["Select File"],
            command=select_file,
        )
        select_file_button.pack(padx=5, pady=10)

        self.file_path = ""
        self.file_info_label = CTkLabel(
            self.cnv_frame_l, text=""
        )  # New label for file information
        self.file_info_label.pack(pady=5)

        # --- Right Frame (Conversion Options) ---
        def segmented_button_callback(value):
            # This function will be called every time the segment button changes
            print("segmented button clicked:", value)
            update_conversion_options()

        self.segment_var = tk.StringVar(value="Image")
        segmented_button = CTkSegmentedButton(
            self.cnv_frame_m,
            values=[
                translations[self.current_language]["Image"],
                translations[self.current_language]["Video"],
                translations[self.current_language]["Audio"],
                translations[self.current_language]["Document"],
            ],
            command=segmented_button_callback,
            variable=self.segment_var,
        )
        segmented_button.pack(pady=10)

        # Conversion Options (Dynamically updated)
        self.conversion_options_label = CTkLabel(
            self.cnv_frame_m,
            text=translations[self.current_language][
                "Select a file to see conversion options."
            ],
        )
        self.conversion_options_label.pack(pady=5)

        self.option_menu = CTkOptionMenu(self.cnv_frame_m, variable=None, values=[])
        self.option_menu.pack(pady=10)

        # --- Conversion Progress Label ---
        self.conversion_progress = CTkLabel(
            self.cnv_frame_m, text="", font=("Arial", 10)
        )
        self.conversion_progress.pack()

        # --- Function to Open Converted File Location ---
        def open_file_location():
            """Opens the file explorer to the location of the converted file."""
            if hasattr(self, "converted_file_path"):
                folder_path = os.path.dirname(self.converted_file_path)
                subprocess.Popen(f'explorer /select,"{folder_path}"')
            else:
                CTkMessagebox(
                    title=translations[self.current_language]["Error"],
                    message=translations[self.current_language][
                        "File not yet converted or not found."
                    ],
                )

        # --- Bottom Frame (Conversion Button and Open Location Button) ---
        def convert_file():
            """Handles the file conversion process."""
            if self.file_path:
                # Update progress label
                self.conversion_progress.configure(
                    text=translations[self.current_language]["Converting..."]
                )
                self.cnv_frame_m.update()  # Update the frame to show the label

                try:
                    output_format = self.option_menu.get().lower()
                    self.converted_file_path = self.convert_to(
                        self.file_path, output_format
                    )

                    # Enable or create the "Open File Location" button
                    if hasattr(self, "open_location_button"):
                        self.open_location_button.configure(state="normal")
                    else:
                        self.open_location_button = CTkButton(
                            self.cnv_frame_m,
                            text=translations[self.current_language][
                                "Open File Location"
                            ],
                            command=open_file_location,
                        )
                        self.open_location_button.pack(pady=10)

                except Exception as e:
                    self.conversion_progress.configure(
                        text=f"{translations[self.current_language]['Conversion failed:']} {str(e)}"
                    )
            else:
                CTkMessagebox(
                    title=translations[self.current_language]["Error"],
                    message=translations[self.current_language][
                        "No file selected for conversion!"
                    ],
                )

        self.download_button = CTkButton(
            self.cnv_frame_m,
            text=translations[self.current_language]["Convert"],
            command=convert_file,
        )
        self.download_button.pack(pady=10)

        # --- Right Frame (File Editor) ---

        # Name
        self.name_label = CTkLabel(self.cnv_frame_r, text="Name:")
        self.name_label.pack(pady=(10, 0))
        self.name_entry = CTkEntry(self.cnv_frame_r, width=300)
        self.name_entry.pack(pady=(0, 10))

        # Description (Not implemented yet)
        self.description_label = CTkLabel(self.cnv_frame_r, text="Description:")
        self.description_label.pack(pady=(10, 0))
        self.description_entry = CTkEntry(self.cnv_frame_r, width=300)
        self.description_entry.pack(pady=(0, 10))

        # Creation Date
        self.creation_date_label = CTkLabel(
            self.cnv_frame_r, text="Creation Date (YYYY-MM-DD HH:MM:SS):"
        )
        self.creation_date_label.pack(pady=(10, 0))
        self.creation_date_entry = CTkEntry(self.cnv_frame_r, width=300)
        self.creation_date_entry.pack(pady=(0, 10))

        # Modification Date
        self.modification_date_label = CTkLabel(
            self.cnv_frame_r, text="Modification Date (YYYY-MM-DD HH:MM:SS):"
        )
        self.modification_date_label.pack(pady=(10, 0))
        self.modification_date_entry = CTkEntry(self.cnv_frame_r, width=300)
        self.modification_date_entry.pack(pady=(0, 10))

        # Permissions (Read-only checkbox)
        def toggle_read_only():
            """Toggles the read-only attribute of the file."""
            if self.file_path:
                attrs = win32api.GetFileAttributes(self.file_path)
                if attrs & win32con.FILE_ATTRIBUTE_READONLY:
                    win32api.SetFileAttributes(
                        self.file_path,
                        attrs & ~win32con.FILE_ATTRIBUTE_READONLY,
                    )
                    self.read_only_checkbox.deselect()
                else:
                    win32api.SetFileAttributes(
                        self.file_path,
                        attrs | win32con.FILE_ATTRIBUTE_READONLY,
                    )
                    self.read_only_checkbox.select()

        self.read_only_checkbox = CTkCheckBox(
            self.cnv_frame_r,
            text="Read-only",
            command=toggle_read_only,
            onvalue="on",
            offvalue="off",
        )
        self.read_only_checkbox.pack(pady=(10, 0))

        # Save Button
        def save_changes():
            """Saves the changes to the file."""
            if self.file_path:
                try:
                    # Update file name
                    new_file_name = self.name_entry.get()
                    if new_file_name != os.path.basename(self.file_path):
                        new_file_path = os.path.join(
                            os.path.dirname(self.file_path), new_file_name
                        )
                        os.rename(self.file_path, new_file_path)
                        self.file_path = new_file_path

                    # Update description (Not implemented yet)
                    # ...

                    # Update creation and modification dates
                    creation_datetime = datetime.strptime(
                        self.creation_date_entry.get(), "%Y-%m-%d %H:%M:%S"
                    )
                    modification_datetime = datetime.strptime(
                        self.modification_date_entry.get(), "%Y-%m-%d %H:%M:%S"
                    )
                    win32api.SetFileTime(
                        self.file_path,
                        creation_datetime,
                        modification_datetime,
                        modification_datetime,
                    )

                    # Display success message
                    CTkMessagebox(
                        title=translations[self.current_language]["Success"],
                        message="File attributes updated successfully.",
                    )

                    # Update file info label
                    display_file_info()
                except Exception as e:
                    CTkMessagebox(
                        title=translations[self.current_language]["Error"],
                        message=f"Error updating file attributes: {e}",
                    )

        self.save_button = CTkButton(
            self.cnv_frame_r, text="Save Changes", command=save_changes
        )
        self.save_button.pack(pady=5,side=BOTTOM)

        # "Back" button
        bck_button = CTkButton(
            self.cnv_frame_l,
            text=translations[self.current_language]["Back"],
            command=lambda: self.load_functions_frame(),
        )
        bck_button.pack(padx=5, pady=5, side=BOTTOM)

        def toggle_extended_menu():
            """Toggles the extended menu and resizes the window."""
            self.Extended_menu = not self.Extended_menu  # Toggle the menu state
            if self.Extended_menu:
                self.geometry("1100x400")  # Expand the window
            else:
                self.geometry("710x400")  # Collapse the window

        ext_button = CTkButton(
            self.cnv_frame_m,
            text=translations[self.current_language]["Extended"],
            command=toggle_extended_menu  # Assign the function to the button
        )
        ext_button.pack(padx=5, pady=5, side=BOTTOM)

        def update_conversion_options():
            """Updates the conversion options based on the selected file type and category."""
            if self.file_path:
                file_ext = os.path.splitext(self.file_path)[1].lower()
                selected_category = self.segment_var.get()

                if selected_category == translations[self.current_language]["Image"]:
                    supported_formats = ["PNG", "JPG", "JPEG", "GIF"]
                elif selected_category == translations[self.current_language]["Video"]:
                    supported_formats = ["MP4", "AVI", "MOV"]
                elif selected_category == translations[self.current_language]["Audio"]:
                    supported_formats = ["MP3", "WAV", "OGG"]
                elif selected_category == translations[self.current_language]["Document"]:
                    supported_formats = ["TXT", "PDF", "DOC", "DOCX"]
                else:
                    supported_formats = []

                self.conversion_options_label.configure(
                    text=f"{translations[self.current_language]['Convert to:']} ({selected_category})"
                )
                self.option_menu.configure(values=supported_formats)
                if supported_formats:
                    self.option_menu.set(
                        supported_formats[0]
                    )  # Set a default option

        def update_editor_fields():
            """Updates the editor fields with current file information."""
            if self.file_path:
                file_name = os.path.basename(self.file_path)
                self.name_entry.delete(0, END)
                self.name_entry.insert(0, file_name)

                # Update creation and modification dates
                creation_timestamp = os.path.getctime(self.file_path)
                modification_timestamp = os.path.getmtime(self.file_path)

                # Update creation and modification dates
                creation_timestamp = os.path.getctime(self.file_path)
                modification_timestamp = os.path.getmtime(self.file_path)

                creation_datetime = datetime.datetime.fromtimestamp(creation_timestamp).strftime("%Y-%m-%d %H:%M:%S")
                modification_datetime = datetime.datetime.fromtimestamp(modification_timestamp).strftime("%Y-%m-%d %H:%M:%S")

                # Update entry widgets only if they are empty
                if not self.creation_date_entry.get():
                    self.creation_date_entry.insert(0, creation_datetime)

                if not self.modification_date_entry.get():
                    self.modification_date_entry.insert(0, modification_datetime)

                # Set read-only checkbox
                attrs = win32api.GetFileAttributes(self.file_path)
                if attrs & win32con.FILE_ATTRIBUTE_READONLY:
                    self.read_only_checkbox.select()
                else:
                    self.read_only_checkbox.deselect()

        # Call update_editor_fields when a file is selected
        select_file_button.configure(command=lambda: [select_file(), update_editor_fields()])

    def load_stg_frame(self):
        self.lf_frame.forget()
        self.fn_frame.forget()

        self.stg_frame = CTkFrame(self, width=300, height=400)
        self.stg_frame.pack(padx=5, pady=5)
        self.stg_frame.propagate(0)

        # "Create WinP Reg Key" button
        crg_button = CTkButton(
            self.stg_frame,
            text=translations[self.current_language]["Activate WinP Context Menu"],
            width=200,
            command=lambda: create_reg_key(True),
        )
        crg_button.pack(padx=5, pady=5)

        # "Delete WinP Reg Key" button
        drg_button = CTkButton(
            self.stg_frame,
            text=translations[self.current_language]["Disable WinP Context Menu"],
            width=200,
            command=lambda: delete_reg_key(True),
        )
        drg_button.pack(padx=5, pady=5)

        # Language Selection
        self.language_label = CTkLabel(self.stg_frame, text=translations[self.current_language]["Select Language"])
        self.language_label.pack(padx=5, pady=5)

        # Получаем список доступных языков из словаря переводов
        available_languages = list(translations.keys())
        # Сопоставляем отображаемые имена языков с их кодами
        language_names = {
            "en": "English",
            "ru": "Русский",
            "de": "Deutsch",
            "fr": "Français",
            "hy": "Հայոց լեզու"
            # Добавьте другие языки по аналогии
        }
        display_languages = [language_names.get(lang, lang) for lang in available_languages]

        self.language_menu = CTkOptionMenu(
            self.stg_frame,
            values=display_languages, # Используем отображаемые имена
            command=lambda lang: self.change_language(
                available_languages[display_languages.index(lang)] # Получаем код языка
            ),
        )
        self.language_menu.pack(padx=5, pady=5)

        # Run on Windows Startup Switch
        def toggle_run_on_startup():
            self.run_on_startup = self.startup_switch.get() == "on"
            self.update_startup_registry()
            self.save_settings()

        self.startup_switch = CTkSwitch(
            self.stg_frame,
            text=translations[self.current_language]["Run on Windows startup"],
            command=toggle_run_on_startup,
            variable=StringVar(value="on" if self.run_on_startup else "off"),
            onvalue="on",
            offvalue="off",
        )
        self.startup_switch.pack(padx=5, pady=5)

        # "Back" button
        bck_button = CTkButton(
            self.stg_frame, text=translations[self.current_language]["Back"], command=lambda: self.load_functions_frame()
        )
        bck_button.pack(padx=5, pady=5, side=BOTTOM)

        self.update_language()  # Update text after adding language settings

    def update_startup_registry(self):
        """Updates the Windows registry to run the app on startup."""
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS
        )
        app_path = os.path.abspath(sys.argv[0])

        if self.run_on_startup:
            try:
                winreg.SetValueEx(key, "WinP", 0, winreg.REG_SZ, app_path)
            except Exception as e:
                print(f"Error setting registry value: {e}")
        else:
            try:
                winreg.DeleteValue(key, "WinP")
            except FileNotFoundError:
                pass  # Value doesn't exist
            except Exception as e:
                print(f"Error deleting registry value: {e}")

        winreg.CloseKey(key)

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
                self.file_path = filedialog.askopenfilename(
                    initialdir="/", title=translations[self.current_language]["Select File"]
                )
            else:
                self.file_path = filedialog.askdirectory(
                    initialdir="/", title="Select Folder"
                )
            self.file_path_label.configure(text=self.file_path)

        def drop_func( files):
            for file in files:
                print(file)

                self.file_path = f"{file}"
                self.file_path_label.configure(text=f'{os.path.basename(self.file_path)}')
        # Button for selecting file/folder\

        self.dragndrop_place = CTkFrame(self.arh_frame,width=250,height=120)
        self.dragndrop_place.pack(pady=5,padx=15)
        self.dragndrop_place.propagate(0)
        self.dragndrop_label = CTkLabel(self.dragndrop_place,text='\nDrag & Drop\nor',width=250,height=60)#translations[self.current_language]["File/Folder not selected"])
        self.dragndrop_label.pack(padx=5)

        pywinstyles.apply_dnd(self.dragndrop_label, drop_func)

        self.select_target_button = CTkButton(
            self.dragndrop_place, text=translations[self.current_language]["Select"], command=select_target,width=250
        )
        self.select_target_button.pack(padx=5, pady=5,side=BOTTOM)

        # Label to display the selected path
        self.file_path_label = CTkLabel(self.arh_frame, text=translations[self.current_language]["File/Folder not selected"])
        self.file_path_label.pack(pady=5)


        self.file_radiobutton_frame = CTkFrame(self.arh_frame,width=250,height=50)
        self.file_radiobutton_frame.pack(padx=5)
        self.file_radiobutton_frame.propagate(0)

        # Radiobutton to choose between file and folder
        self.file_radiobutton = CTkRadioButton(
            self.file_radiobutton_frame, text="File", variable=self.target_type, value="file"
        )
        self.file_radiobutton.pack(padx=5,pady=5,side=LEFT)
        self.folder_radiobutton = CTkRadioButton(
            self.file_radiobutton_frame, text="Folder", variable=self.target_type, value="folder"
        )
        self.folder_radiobutton.pack(padx=5,pady=5,side=LEFT)

        self.use_password_frame = CTkFrame(self.arh_frame,width=250,height=50)
        self.use_password_frame.pack(padx=5,pady=5)
        self.use_password_frame.propagate(0)

        # Checkbox to enable password usage
        self.use_password = IntVar(value=0)
        self.password_checkbox = CTkCheckBox(
            self.use_password_frame,
            text=f'{translations[self.current_language]["Use Password?"]} ',
            variable=self.use_password,
            command=self.toggle_password_entry,
        )
        self.password_checkbox.pack(padx=5,pady=5,side=LEFT)

        # Entry field for password (initially disabled)
        self.password_entry = CTkEntry(
            self.use_password_frame,
            placeholder_text=translations[self.current_language]["Enter Password"],
            show="*",
            state="disabled",
        )
        self.password_entry.pack(padx=5,pady=5,side=LEFT)

        # Functions for archiving and extracting
        def archive():
            if self.file_path:
                password = (
                    self.password_entry.get() if self.use_password.get() else None
                )
                try:
                    compress_file(self.file_path, password)
                    CTkMessagebox(
                        title=translations[self.current_language]["Success"],
                        message=f"File/folder '{self.file_path}' successfully archived.",
                        option_1="OK",
                    )
                except Exception as e:
                    CTkMessagebox(title=translations[self.current_language]["Error"], message=f"Error during archiving: {e}")

        def extract():
            if self.file_path:
                password = (
                    self.password_entry.get() if self.use_password.get() else None
                )
                try:
                    decompress_file(self.file_path, password)
                    CTkMessagebox(
                        title=translations[self.current_language]["Success"],
                        message=f"File/folder '{self.file_path}' successfully extracted.",
                        option_1="OK",
                    )
                except RuntimeError as e:
                    CTkMessagebox(
                        title=translations[self.current_language]["Error"], message=f"Error during extraction: {e}"
                    )
                except Exception as e:
                    CTkMessagebox(
                        title=translations[self.current_language]["Error"], message=f"Error during extraction: {e}"
                    )

        self.arhh_frame = CTkFrame(self.arh_frame,width=250,height=50)
        self.arhh_frame.pack(padx=5,pady=5)
        self.arhh_frame.propagate(0)

        # Buttons for archiving and extracting
        self.archive_button = CTkButton(self.arhh_frame, text=translations[self.current_language]["Archive"], command=archive,width=115)
        self.archive_button.pack(pady=5,padx=5,side=LEFT)
        self.extract_button = CTkButton(self.arhh_frame, text=translations[self.current_language]["Extract"], command=extract,width=115)
        self.extract_button.pack(pady=5,padx=5,side=RIGHT)

        # "Back" button
        bck_button = CTkButton(
            self.arh_frame, text=translations[self.current_language]["Back"], command=lambda: self.load_functions_frame(),width=250
        )
        bck_button.pack(padx=5, pady=5, side=BOTTOM)

    def toggle_password_entry(self):
        """Enables/disables password entry field."""
        if self.use_password.get():
            self.password_entry.configure(state="normal")
        else:
            self.password_entry.configure(state="disabled")

    def convert_to(self, file_path, output_format):
        """
        Converts the given file to the specified output format and saves it to the Downloads folder.
        """
        def conversion_thread():
            """Функция для выполнения конвертации в отдельном потоке."""
            nonlocal output_file_path
            global open_file_location
            try:
                if output_format == "txt":
                    with open(output_file_path, "w") as f:
                        pass  # Просто создаем пустой текстовый файл
                elif output_format == "jpg":
                    img = Image.open(file_path).convert("RGB")
                    img.save(output_file_path, "JPEG")
                elif output_format == "png":
                    img = Image.open(file_path)
                    img.save(output_file_path, "PNG")
                elif output_format == "gif":
                    img = Image.open(file_path)
                    img.save(output_file_path, "GIF")
                elif output_format == "mp4":
                    clip = mp.VideoFileClip(file_path)
                    clip.write_videofile(output_file_path)
                elif output_format == "avi":
                    clip = mp.VideoFileClip(file_path)
                    clip.write_videofile(output_file_path, codec="png")
                elif output_format == "mov":
                    clip = mp.VideoFileClip(file_path)
                    clip.write_videofile(output_file_path, codec="libx264")  # H.264 codec
                elif output_format == "mp3":
                    audio = AudioSegment.from_file(file_path)
                    audio.export(output_file_path, format="mp3")
                elif output_format == "wav":
                    audio = AudioSegment.from_file(file_path)
                    audio.export(output_file_path, format="wav")
                elif output_format == "ogg":
                    audio = AudioSegment.from_file(file_path)
                    audio.export(output_file_path, format="ogg")
                # Добавьте аналогичные блоки elif для других форматов документов (PDF, DOC, DOCX и т. д.)
                else:
                    raise ValueError(
                        f"Конвертация в {output_format} пока не реализована!"
                    )

                # Обновляем UI после успешной конвертации
                self.conversion_progress.configure(text=translations[self.current_language]["Conversion complete!"])
                if hasattr(self, "open_location_button"):
                    self.open_location_button.configure(state="normal")
                else:
                    self.open_location_button = CTkButton(
                        self.cnv_frame_m,
                        text=translations[self.current_language]["Open File Location"],
                        command=open_file_location,
                    )
                    self.open_location_button.pack(pady=10)
            except Exception as e:
                # Обновляем UI при ошибке
                self.conversion_progress.configure(
                    text=f"{translations[self.current_language]['Conversion failed:']} {str(e)}"
                )

        print(f"Конвертирую {file_path} в {output_format}")
        file_name, _ = os.path.splitext(os.path.basename(file_path))
        downloads_path = str(Path.home() / "Downloads")
        output_file_path = os.path.join(
            downloads_path, f"{file_name}.{output_format.lower()}"
        )
        print(f"Путь вывода: {output_file_path}")

        self.conversion_progress.configure(text=translations[self.current_language]["Converting..."])
        self.cnv_frame_m.update()  # Обновляем фрейм, чтобы отобразить метку

        # Создаем и запускаем поток для конвертации
        thread = threading.Thread(target=conversion_thread)
        thread.start()

        return output_file_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "extract":
            # Получаем пути к файлам/папкам из аргументов командной строки:
            items_to_extract = sys.argv[2:] 
            extract_thread(items_to_extract)
        elif sys.argv[1] == "archive":
            items_to_archive = sys.argv[2:]
            archive_thread(items_to_archive)
    else:
        app = WinPWindow()
        app.mainloop()

#
#ef load_cnv_frame(self):
#       """Loads the frame for file conversion with input and output options."""
#       self.clear_frame()
#       self.geometry("700x400")
#
#       self.cnv_frame_l = CTkFrame(self, width=300, height=400)
#       self.cnv_frame_l.pack(padx=5, pady=5, side=LEFT)
#       self.cnv_frame_l.propagate(0)
#
#       self.cnv_frame_r = CTkFrame(self, width=400, height=400, corner_radius=0)
#       self.cnv_frame_r.pack(side=LEFT)
#       self.cnv_frame_r.propagate(0)
#
#       # --- Left Frame (File Input) ---
#
#       def select_file():
#           """Opens a dialog to select a file and updates the file path label."""
#           self.file_path = filedialog.askopenfilename(
#               initialdir="/", title=translations[self.current_language]["Select File"]
#           )
#           if self.file_path:
#               display_file_info()
#           # Update conversion options based on selected file type
#           update_conversion_options()
#
#       def display_file_info():
#           """Displays file information in the file_info_label."""
#           if not self.file_path:  # Проверка, выбран ли файл
#               return
#
#           file_name = os.path.basename(self.file_path)
#           file_size = os.path.getsize(self.file_path)
#           file_type = os.path.splitext(self.file_path)[1].lower()
#           
#           # Получаем время создания, изменения и последнего открытия
#           file_create_timestamp = os.path.getctime(self.file_path)
#           file_modify_timestamp = os.path.getmtime(self.file_path)
#           file_access_timestamp = os.path.getatime(self.file_path)
#
#           # Преобразуем временные метки в читаемый формат
#           file_create_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_create_timestamp))
#           file_update_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_modify_timestamp))
#           file_last_open_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_access_timestamp))
#
#           # Получаем атрибуты файла
#           file_modify = oct(os.stat(self.file_path).st_mode)[-3:]
#           if file_modify == "666":
#               file_modify = "None"
#
#           file_info_text = (
#               f"{translations[self.current_language]['File']} : {file_name}\n"
#               f"{translations[self.current_language]['Type']} : {file_type}\n"
#               f"{translations[self.current_language]['Size']} : {file_size} байт\n"
#               f"{translations[self.current_language]['On disk']} : {file_size} байт\n"
#               f"---------------------------\n"
#               f"{translations[self.current_language]['Created']} : {file_create_data}\n"
#               f"{translations[self.current_language]['Modified']} : {file_update_data}\n"
#               f"{translations[self.current_language]['Opened']} : {file_last_open_data}\n"
#               f"---------------------------\n"
#               f"{translations[self.current_language]['Attributes']} : {file_modify}\n"
#           )
#           self.file_info_label.configure(text=file_info_text,justify=LEFT)
#
#       # Button to select a file
#       select_file_button = CTkButton(
#           self.cnv_frame_l, text=translations[self.current_language]["Select File"], command=select_file
#       )
#       select_file_button.pack(padx=5, pady=10)
#
#       self.file_path = ""
#       self.file_info_label = CTkLabel(self.cnv_frame_l, text="")  # Новая метка для информации о файле
#       self.file_info_label.pack(pady=5)
#
#       # --- Right Frame (Conversion Options) ---
#       def segmented_button_callback(value):
#           # This function will be called every time the segment button changes
#           print("segmented button clicked:", value)
#           update_conversion_options()
#
#       self.segment_var = tk.StringVar(value="Image")
#       segmented_button = CTkSegmentedButton(
#           self.cnv_frame_r,
#           values=[translations[self.current_language]["Image"], translations[self.current_language]["Video"], translations[self.current_language]["Audio"], translations[self.current_language]["Document"]],
#           command=segmented_button_callback,
#           variable=self.segment_var,
#       )
#       segmented_button.pack(pady=10)
#
#       # Conversion Options (Dynamically updated)
#       self.conversion_options_label = CTkLabel(
#           self.cnv_frame_r, text=translations[self.current_language]["Select a file to see conversion options."]
#       )
#       self.conversion_options_label.pack(pady=5)
#
#       self.option_menu = CTkOptionMenu(
#           self.cnv_frame_r, variable=None, values=[]
#       )
#       self.option_menu.pack(pady=10)
#
#       # --- Conversion Progress Label ---
#       self.conversion_progress = CTkLabel(
#           self.cnv_frame_r, text="", font=("Arial", 10)
#       )
#       self.conversion_progress.pack()
#
#       # --- Function to Open Converted File Location ---
#       def open_file_location():
#           """Opens the file explorer to the location of the converted file."""
#           if hasattr(self, "converted_file_path"):
#               folder_path = os.path.dirname(self.converted_file_path)
#               subprocess.Popen(f'explorer /select,"{folder_path}"')
#           else:
#               CTkMessagebox(
#                   title=translations[self.current_language]["Error"], message=translations[self.current_language]["File not yet converted or not found."]
#               )
#
#       # --- Bottom Frame (Conversion Button and Open Location Button) ---
#       def convert_file():
#           """Handles the file conversion process."""
#           if self.file_path:
#               # Update progress label
#               self.conversion_progress.configure(text=translations[self.current_language]["Converting..."])
#               self.cnv_frame_r.update()  # Update the frame to show the label
#
#               try:
#                   output_format = self.option_menu.get().lower()
#                   self.converted_file_path = self.convert_to(
#                       self.file_path, output_format
#                   )
#                   self.conversion_progress.configure(text=translations[self.current_language]["Conversion complete!"])
#
#                   # Enable or create the "Open File Location" button
#                   if hasattr(self, "open_location_button"):
#                       self.open_location_button.configure(state="normal")
#                   else:
#                       self.open_location_button = CTkButton(
#                           self.cnv_frame_r,
#                           text=translations[self.current_language]["Open File Location"],
#                           command=open_file_location,
#                       )
#                       self.open_location_button.pack(pady=10)
#
#               except Exception as e:
#                   self.conversion_progress.configure(
#                       text=f"{translations[self.current_language]['Conversion failed:']} {str(e)}"
#                   )
#           else:
#               CTkMessagebox(title=translations[self.current_language]["Error"], message=translations[self.current_language]["No file selected for conversion!"])
#
#       self.download_button = CTkButton(
#           self.cnv_frame_r, text=translations[self.current_language]["Convert"], command=convert_file
#       )
#       self.download_button.pack(pady=10)
#
#       # --- Right Frame (File Editor) ---
#
#       # Name
#       self.name_label = CTkLabel(self.cnv_frame_r, text="Name:")
#       self.name_label.pack(pady=(10, 0))
#       self.name_entry = CTkEntry(self.cnv_frame_r, width=300)
#       self.name_entry.pack(pady=(0, 10))
#
#       # Description (Not implemented yet)
#       self.description_label = CTkLabel(self.cnv_frame_r, text="Description:")
#       self.description_label.pack(pady=(10, 0))
#       self.description_entry = CTkEntry(self.cnv_frame_r, width=300)
#       self.description_entry.pack(pady=(0, 10))
#
#       # Creation Date
#       self.creation_date_label = CTkLabel(
#           self.cnv_frame_r, text="Creation Date (YYYY-MM-DD HH:MM:SS):"
#       )
#       self.creation_date_label.pack(pady=(10, 0))
#       self.creation_date_entry = CTkEntry(self.cnv_frame_r, width=300)
#       self.creation_date_entry.pack(pady=(0, 10))
#
#       # Modification Date
#       self.modification_date_label = CTkLabel(
#           self.cnv_frame_r, text="Modification Date (YYYY-MM-DD HH:MM:SS):"
#       )
#       self.modification_date_label.pack(pady=(10, 0))
#       self.modification_date_entry = CTkEntry(self.cnv_frame_r, width=300)
#       self.modification_date_entry.pack(pady=(0, 10))
#
#       # Permissions (Read-only checkbox)
#       def toggle_read_only():
#           """Toggles the read-only attribute of the file."""
#           if self.file_path:
#               attrs = win32api.GetFileAttributes(self.file_path)
#               if attrs & win32con.FILE_ATTRIBUTE_READONLY:
#                   win32api.SetFileAttributes(
#                       self.file_path, attrs & ~win32con.FILE_ATTRIBUTE_READONLY
#                   )
#                   self.read_only_checkbox.deselect()
#               else:
#                   win32api.SetFileAttributes(
#                       self.file_path, attrs | win32con.FILE_ATTRIBUTE_READONLY
#                   )
#                   self.read_only_checkbox.select()
#
#       self.read_only_checkbox = CTkCheckBox(
#           self.cnv_frame_r,
#           text="Read-only",
#           command=toggle_read_only,
#           onvalue="on",
#           offvalue="off",
#       )
#       self.read_only_checkbox.pack(pady=(10, 0))
#
#       # Save Button
#       def save_changes():
#           """Saves the changes to the file."""
#           if self.file_path:
#               try:
#                   # Update file name
#                   new_file_name = self.name_entry.get()
#                   if new_file_name != os.path.basename(self.file_path):
#                       new_file_path = os.path.join(
#                           os.path.dirname(self.file_path), new_file_name
#                       )
#                       os.rename(self.file_path, new_file_path)
#                       self.file_path = new_file_path
#
#                   # Update description (Not implemented yet)
#                   # ...
#
#                   # Update creation and modification dates
#                   creation_datetime = datetime.datetime.strptime(
#                       self.creation_date_entry.get(), "%Y-%m-%d %H:%M:%S"
#                   )
#                   modification_datetime = datetime.datetime.strptime(
#                       self.modification_date_entry.get(), "%Y-%m-%d %H:%M:%S"
#                   )
#                   win32api.SetFileTime(
#                       self.file_path,
#                       creation_datetime,
#                       modification_datetime,
#                       modification_datetime,
#                   )
#
#                   # Display success message
#                   CTkMessagebox(
#                       title=translations[self.current_language]["Success"],
#                       message="File attributes updated successfully.",
#                   )
#
#                   # Update file info label
#                   display_file_info()
#               except Exception as e:
#                   CTkMessagebox(
#                       title=translations[self.current_language]["Error"],
#                       message=f"Error updating file attributes: {e}",
#                   )
#
#       self.save_button = CTkButton(
#           self.cnv_frame_r, text="Save Changes", command=save_changes
#       )
#       self.save_button.pack(pady=10)
#
#       # "Back" button
#       bck_button = CTkButton(
#           self.cnv_frame_l,
#           text=translations[self.current_language]["Back"],
#           command=lambda: self.load_functions_frame(),
#       )
#       bck_button.pack(padx=5, pady=5, side=BOTTOM)
#
#       def update_editor_fields():
#           """Updates the editor fields with current file information."""
#           if self.file_path:
#               file_name = os.path.basename(self.file_path)
#               self.name_entry.delete(0, END)
#               self.name_entry.insert(0, file_name)
#
#               if self.file_path: # Проверяем, выбран ли файл
#                   file_ext = os.path.splitext(self.file_path)[1].lower()
#                   selected_category = self.segment_var.get()  # Get selected category
#
#                   if selected_category == translations[self.current_language]["Image"]:
#                       supported_formats = ["PNG", "JPG", "JPEG", "GIF"]  # Example
#                   elif selected_category == translations[self.current_language]["Video"]:
#                       supported_formats = ["MP4", "AVI", "MOV"]  # Example
#                   elif selected_category == translations[self.current_language]["Audio"]:
#                       supported_formats = ["MP3", "WAV", "OGG"]  # Example
#                   elif selected_category == translations[self.current_language]["Document"]:
#                       supported_formats = ["TXT", "PDF", "DOC", "DOCX"]  # Example
#                   else:
#                       supported_formats = []
#
#                   self.conversion_options_label.configure(
#                       text=f"{translations[self.current_language]['Convert to:']} ({selected_category})"
#                   )
#                   self.option_menu.configure(values=supported_formats)
#                   if supported_formats:
#                       self.option_menu.set(
#                           supported_formats[0]
#                       )  # Set a default option
#
#               # Update creation and modification dates
#               creation_timestamp = os.path.getctime(self.file_path)
#               modification_timestamp = os.path.getmtime(self.file_path)
#
#               creation_datetime = datetime.datetime.fromtimestamp(
#                   creation_timestamp
#               ).strftime("%Y-%m-%d %H:%M:%S")
#               modification_datetime = datetime.datetime.fromtimestamp(
#                   modification_timestamp
#               ).strftime("%Y-%m-%d %H:%M:%S")
#
#               self.creation_date_entry.delete(0, END)
#               self.creation_date_entry.insert(0, creation_datetime)
#
#               self.modification_date_entry.delete(0, END)
#               self.modification_date_entry.insert(0, modification_datetime)
#
#               # Set read-only checkbox
#               attrs = win32api.GetFileAttributes(self.file_path)
#               if attrs & win32con.FILE_ATTRIBUTE_READONLY:
#                   self.read_only_checkbox.select()
#               else:
#                   self.read_only_checkbox.deselect()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# created by Nazaryan Artem
# Github @sl1de36 | Telegram @slide36
#
#mport os
#mport tkinter as tk
#rom tkinter import filedialog
#rom customtkinter import *
#rom CTkMessagebox import CTkMessagebox
#rom func.arh import compress_file, decompress_file
#rom webbrowser import open
#mport subprocess
#mport os
#mport sys
#mport win32com.client
#mport winreg
#rom pathlib import Path
#rom PIL import Image
#mport moviepy.editor as mp
#rom pydub import AudioSegment
#mport threading
#mport time
#
#
# Словари для перевода интерфейса
#ranslations = {
#   "en": {
#       "Archivate": "Archivate",
#       "Converter": "Converter",
#       "Optimizer": "Optimizer",
#       "Settings": "Settings",
#       "GitHub": "GitHub",
#       "Activate WinP Context Menu": "Activate WinP Context Menu",
#       "Disable WinP Context Menu": "Disable WinP Context Menu",
#       "Back": "Back",
#       "Select File": "Select File",
#       "No file selected": "No file selected",
#       "Image": "Image",
#       "Video": "Video",
#       "Audio": "Audio",
#       "Document": "Document",
#       "Select a file to see conversion options.": "Select a file to see conversion options.",
#       "Convert to:": "Convert to:",
#       "Converting...": "Converting...",
#       "Conversion complete!": "Conversion complete!",
#       "Open File Location": "Open File Location",
#       "Conversion failed:": "Conversion failed:",
#       "No file selected for conversion!": "No file selected for conversion!",
#       "File": "File",
#       "Type": "Type",
#       "Size": "Size",
#       "On disk": "On disk",
#       "Created": "Created",
#       "Modified": "Modified",
#       "Opened": "Opened",
#       "Attributes": "Attributes",
#       "Select": "Select",
#       "File/Folder not selected": "File/Folder not selected",
#       "Use Password?": "Use Password?",
#       "Enter Password": "Enter Password",
#       "Archive": "Archive",
#       "Extract": "Extract",
#       "Error": "Error",
#       "No file or folder selected.": "No file or folder selected.",
#       "Unsupported file type:": "Unsupported file type:",
#       "Error archiving": "Error archiving",
#       "Error extracting": "Error extracting",
#       "Done": "Done",
#       "Convert": "Convert",
#       "Registry entry successfully updated.": "Registry entry successfully updated.",
#       "Error updating registry entry.": "Error updating registry entry.",
#       "Confirmation": "Confirmation",
#       "Are you sure you want to exit?": "Are you sure you want to exit?",
#       "Yes": "Yes",
#       "No": "No",
#       "Language": "Language",
#       "Select Language": "Select Language",
#   },
#   "ru": {
#       "Archivate": "Архивация",
#       "Converter": "Конвертер",
#       "Optimizer": "Оптимизатор",
#       "Settings": "Настройки",
#       "GitHub": "GitHub",
#       "Activate WinP Context Menu": "Активировать контекстное меню WinP",
#       "Disable WinP Context Menu": "Отключить контекстное меню WinP",
#       "Back": "Назад",
#       "Select File": "Выбрать файл",
#       "No file selected": "Файл не выбран",
#       "Image": "Изображение",
#       "Video": "Видео",
#       "Audio": "Аудио",
#       "Document": "Документ",
#       "Select a file to see conversion options.": "Выберите файл, чтобы увидеть варианты конвертации.",
#       "Convert to:": "Конвертировать в:",
#       "Converting...": "Конвертирую...",
#       "Conversion complete!": "Конвертация завершена!",
#       "Open File Location": "Открыть расположение файла",
#       "Conversion failed:": "Ошибка конвертации:",
#       "No file selected for conversion!": "Не выбран файл для конвертации!",
#       "File": "Файл",
#       "Type": "Тип",
#       "Size": "Размер",
#       "On disk": "На диске",
#       "Created": "Создан",
#       "Modified": "Изменен",
#       "Convert": "Конвертировать",
#       "Opened": "Открыт",
#       "Attributes": "Атрибуты",
#       "Select": "Выбрать",
#       "File/Folder not selected": "Файл/Папка не выбраны",
#       "Use Password?": "Использовать пароль?",
#       "Enter Password": "Введите пароль",
#       "Archive": "Архивировать",
#       "Extract": "Извлечь",
#       "Error": "Ошибка",
#       "No file or folder selected.": "Не выбран файл или папка.",
#       "Unsupported file type:": "Неподдерживаемый тип файла:",
#       "Error archiving": "Ошибка архивации",
#       "Error extracting": "Ошибка извлечения",
#       "Done": "Готово",
#       "Registry entry successfully updated.": "Запись реестра успешно обновлена.",
#       "Error updating registry entry.": "Ошибка обновления записи реестра.",
#       "Confirmation": "Подтверждение",
#       "Are you sure you want to exit?": "Вы уверены, что хотите выйти?",
#       "Yes": "Да",
#       "No": "Нет",
#       "Language": "Язык",
#       "Select Language": "Выбрать язык",
#   },
#
#
#
#lass WinPWindow(CTk):
#   def __init__(self):
#       super().__init__()
#
#       self.current_language = "en"  # Начальный язык - английский
#       """
#       Initialize the application.
#
#       Instantiate the WinPWindow class, set the window size to 300x400,
#       and make it non-resizable.
#       Also, load the functions frame.
#       """
#       # self.iconbitmap("assets/winp.ico")
#       self.title("WinP: F17E7")
#       self.geometry("300x400")
#       self.resizable(False, False)
#       # Инициализируем фреймы как None
#       self.lf_frame = None
#       self.fn_frame = None
#       self.arh_frame = None
#       self.cnv_frame_l = None
#       self.cnv_frame_r = None
#       self.stg_frame = None
#
#       self.load_functions_frame()
#
#       self.protocol(
#           "WM_DELETE_WINDOW", self.on_closing
#       )  # Вызов on_closing при закрытии
#
#   def change_language(self, new_language):
#       """Меняет язык интерфейса."""
#       self.current_language = new_language
#       self.update_language()  # Обновляем текст элементов интерфейса
#
#   def update_language(self):
#       """Обновляет текст элементов интерфейса в соответствии с выбранным языком."""
#       self.update_widget_language(self)
#
#       # Обновляем дочерние элементы во фреймах
#       for frame in [self.lf_frame, self.fn_frame, self.arh_frame, 
#                     self.cnv_frame_l, self.cnv_frame_r, self.stg_frame]:
#           try:
#               self.update_widget_language(frame)
#           except AttributeError:
#               pass
#
#   def update_widget_language(self, widget):
#       """Рекурсивно обновляет текст виджета и его потомков."""
#       if hasattr(widget, "configure") and "text" in widget.keys():
#           original_text = widget.cget("text")
#           translated_text = translations[self.current_language].get(
#               original_text, original_text
#           )
#           widget.configure(text=translated_text)
#       for child in widget.winfo_children():
#           self.update_widget_language(child)
#
#   def on_closing(self):
#       """Функция, которая вызывается при закрытии окна."""
#       if CTkMessagebox(
#           title=translations[self.current_language]["Confirmation"],
#           message=translations[self.current_language]["Are you sure you want to exit?"],
#           icon="question",
#           option_1=translations[self.current_language]["Yes"],
#           option_2=translations[self.current_language]["No"],
#       ).get() == translations[self.current_language]["Yes"]:
#           self.destroy()  # Закрываем окно
#           os._exit(0)  # Завершаем процесс Python
#
#   def function(self, name):
#       """
#       Handle the click event of a button to execute a specific function.
#
#       When a button is clicked, the name of the button is passed to this function.
#       It hides the main functions frame, creates a new frame for the selected function,
#       executes the function associated with the button name, and displays a 'Back' button
#       to return to the previous frame.
#       """
#       self.lf_frame.forget()
#       self.fn_frame = CTkFrame(self, width=300, height=400)
#       self.fn_frame.pack(padx=5, pady=5)
#       self.fn_frame.propagate(0)
#
#       fncs = {
#           "ARH": self.load_arh_frame,
#           "CNV": self.load_cnv_frame,
#           "TMP": lambda: print("TMP"),
#           "STG": self.load_stg_frame,
#       }
#
#       if name in fncs:
#           fncs[name]()
#
#       bck_button = CTkButton(
#           self.fn_frame, text=translations[self.current_language]["Back"], command=lambda: self.load_functions_frame()
#       )
#       bck_button.pack(padx=5, pady=5, side=BOTTOM)
#
#   def clear_frame(self):
#       
#       for frame in [self.stg_frame, self.fn_frame, self.arh_frame, 
#                     self.cnv_frame_l, self.cnv_frame_r, self.lf_frame]:
#           try:
#               frame.forget()
#           except AttributeError:
#               pass
#       
#       self.geometry("300x400")
#
#   def load_functions_frame(self):
#       """
#       Load the main functions frame.
#
#       If any secondary function frame (like archive frame) exists, it is forgotten (hidden).
#       Then, a new frame is created to hold the main function buttons (Archive, Converter, Optimizer).
#       """
#       self.clear_frame()
#       self.lf_frame = CTkFrame(self, width=300, height=400)
#       self.lf_frame.pack(padx=5, pady=5)
#       self.lf_frame.propagate(0)
#
#       arh_button = CTkButton(
#           self.lf_frame, text=translations[self.current_language]["Archivate"], command=lambda: self.function("ARH")
#       )
#       arh_button.pack(padx=5, pady=5)
#       cnv_button = CTkButton(
#           self.lf_frame, text=translations[self.current_language]["Converter"], command=lambda: self.function("CNV")
#       )
#       cnv_button.pack(padx=5, pady=5)
#       tmp_button = CTkButton(
#           self.lf_frame, text=translations[self.current_language]["Optimizer"], command=lambda: self.function("TMP")
#       )
#       tmp_button.pack(padx=5, pady=5)
#       stg_button = CTkButton(
#           self.lf_frame, text=translations[self.current_language]["Settings"], command=lambda: self.function("STG")
#       )
#       stg_button.pack(padx=5, pady=5)
#
#       dev_button = CTkButton(self.lf_frame,text=translations[self.current_language]["GitHub"],command=lambda: open("https://github.com/SL1dee36"))
#       dev_button.pack(padx=5, pady=5, side=BOTTOM)
#
#       # Translate initial text
#       self.update_language() 
#
#   def load_cnv_frame(self):
#       """Loads the frame for file conversion with input and output options."""
#       self.clear_frame()
#       self.geometry("700x400")
#
#       self.cnv_frame_l = CTkFrame(self, width=300, height=400)
#       self.cnv_frame_l.pack(padx=5, pady=5, side=LEFT)
#       self.cnv_frame_l.propagate(0)
#
#       self.cnv_frame_r = CTkFrame(self, width=400, height=400, corner_radius=0)
#       self.cnv_frame_r.pack(side=LEFT)
#       self.cnv_frame_r.propagate(0)
#
#       # --- Left Frame (File Input) ---
#
#       def select_file():
#           """Opens a dialog to select a file and updates the file path label."""
#           self.file_path = filedialog.askopenfilename(
#               initialdir="/", title=translations[self.current_language]["Select File"]
#           )
#           if self.file_path:
#               display_file_info()
#           # Update conversion options based on selected file type
#           update_conversion_options()
#
#       def display_file_info():
#           """Displays file information in the file_info_label."""
#           if not self.file_path:  # Проверка, выбран ли файл
#               return
#
#           file_name = os.path.basename(self.file_path)
#           file_size = os.path.getsize(self.file_path)
#           file_type = os.path.splitext(self.file_path)[1].lower()
#           
#           # Получаем время создания, изменения и последнего открытия
#           file_create_timestamp = os.path.getctime(self.file_path)
#           file_modify_timestamp = os.path.getmtime(self.file_path)
#           file_access_timestamp = os.path.getatime(self.file_path)
#
#           # Преобразуем временные метки в читаемый формат
#           file_create_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_create_timestamp))
#           file_update_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_modify_timestamp))
#           file_last_open_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_access_timestamp))
#
#           # Получаем атрибуты файла
#           file_modify = oct(os.stat(self.file_path).st_mode)[-3:]
#           if file_modify == "666":
#               file_modify = "None"
#
#           file_info_text = (
#               f"{translations[self.current_language]['File']} : {file_name}\n"
#               f"{translations[self.current_language]['Type']} : {file_type}\n"
#               f"{translations[self.current_language]['Size']} : {file_size} байт\n"
#               f"{translations[self.current_language]['On disk']} : {file_size} байт\n"
#               f"---------------------------\n"
#               f"{translations[self.current_language]['Created']} : {file_create_data}\n"
#               f"{translations[self.current_language]['Modified']} : {file_update_data}\n"
#               f"{translations[self.current_language]['Opened']} : {file_last_open_data}\n"
#               f"---------------------------\n"
#               f"{translations[self.current_language]['Attributes']} : {file_modify}\n"
#           )
#           self.file_info_label.configure(text=file_info_text,justify=LEFT)
#
#       # Button to select a file
#       select_file_button = CTkButton(
#           self.cnv_frame_l, text=translations[self.current_language]["Select File"], command=select_file
#       )
#       select_file_button.pack(padx=5, pady=10)
#
#       self.file_path = ""
#       self.file_info_label = CTkLabel(self.cnv_frame_l, text="")  # Новая метка для информации о файле
#       self.file_info_label.pack(pady=5)
#
#       # --- Right Frame (Conversion Options) ---
#       def segmented_button_callback(value):
#           # This function will be called every time the segment button changes
#           print("segmented button clicked:", value)
#           update_conversion_options()
#
#       self.segment_var = tk.StringVar(value="Image")
#       segmented_button = CTkSegmentedButton(
#           self.cnv_frame_r,
#           values=[translations[self.current_language]["Image"], translations[self.current_language]["Video"], translations[self.current_language]["Audio"], translations[self.current_language]["Document"]],
#           command=segmented_button_callback,
#           variable=self.segment_var,
#       )
#       segmented_button.pack(pady=10)
#
#       # Conversion Options (Dynamically updated)
#       self.conversion_options_label = CTkLabel(
#           self.cnv_frame_r, text=translations[self.current_language]["Select a file to see conversion options."]
#       )
#       self.conversion_options_label.pack(pady=5)
#
#       self.option_menu = CTkOptionMenu(
#           self.cnv_frame_r, variable=None, values=[]
#       )
#       self.option_menu.pack(pady=10)
#
#       # --- Conversion Progress Label ---
#       self.conversion_progress = CTkLabel(
#           self.cnv_frame_r, text="", font=("Arial", 10)
#       )
#       self.conversion_progress.pack()
#
#       # --- Function to Open Converted File Location ---
#       def open_file_location():
#           """Opens the file explorer to the location of the converted file."""
#           if hasattr(self, "converted_file_path"):
#               folder_path = os.path.dirname(self.converted_file_path)
#               subprocess.Popen(f'explorer /select,"{folder_path}"')
#           else:
#               CTkMessagebox(
#                   title=translations[self.current_language]["Error"], message=translations[self.current_language]["File not yet converted or not found."]
#               )
#
#       # --- Bottom Frame (Conversion Button and Open Location Button) ---
#       def convert_file():
#           """Handles the file conversion process."""
#           if self.file_path:
#               # Update progress label
#               self.conversion_progress.configure(text=translations[self.current_language]["Converting..."])
#               self.cnv_frame_r.update()  # Update the frame to show the label
#
#               try:
#                   output_format = self.option_menu.get().lower()
#                   self.converted_file_path = self.convert_to(
#                       self.file_path, output_format
#                   )
#                   self.conversion_progress.configure(text=translations[self.current_language]["Conversion complete!"])
#
#                   # Enable or create the "Open File Location" button
#                   if hasattr(self, "open_location_button"):
#                       self.open_location_button.configure(state="normal")
#                   else:
#                       self.open_location_button = CTkButton(
#                           self.cnv_frame_r,
#                           text=translations[self.current_language]["Open File Location"],
#                           command=open_file_location,
#                       )
#                       self.open_location_button.pack(pady=10)
#
#               except Exception as e:
#                   self.conversion_progress.configure(
#                       text=f"{translations[self.current_language]['Conversion failed:']} {str(e)}"
#                   )
#           else:
#               CTkMessagebox(title=translations[self.current_language]["Error"], message=translations[self.current_language]["No file selected for conversion!"])
#
#       self.download_button = CTkButton(
#           self.cnv_frame_r, text=translations[self.current_language]["Convert"], command=convert_file
#       )
#       self.download_button.pack(pady=10)
#
#       # "Back" button
#       bck_button = CTkButton(
#           self.cnv_frame_l,
#           text=translations[self.current_language]["Back"],
#           command=lambda: self.load_functions_frame(),
#       )
#       bck_button.pack(padx=5, pady=5, side=BOTTOM)
#
#       # --- Function to update conversion options based on file type ---
#       def update_conversion_options():
#           if self.file_path: # Проверяем, выбран ли файл
#               file_ext = os.path.splitext(self.file_path)[1].lower()
#               selected_category = self.segment_var.get()  # Get selected category
#
#               if selected_category == translations[self.current_language]["Image"]:
#                   supported_formats = ["PNG", "JPG", "JPEG", "GIF"]  # Example
#               elif selected_category == translations[self.current_language]["Video"]:
#                   supported_formats = ["MP4", "AVI", "MOV"]  # Example
#               elif selected_category == translations[self.current_language]["Audio"]:
#                   supported_formats = ["MP3", "WAV", "OGG"]  # Example
#               elif selected_category == translations[self.current_language]["Document"]:
#                   supported_formats = ["TXT", "PDF", "DOC", "DOCX"]  # Example
#               else:
#                   supported_formats = []
#
#               self.conversion_options_label.configure(
#                   text=f"{translations[self.current_language]['Convert to:']} ({selected_category})"
#               )
#               self.option_menu.configure(values=supported_formats)
#               if supported_formats:
#                   self.option_menu.set(
#                       supported_formats[0]
#                   )  # Set a default option
#
#   def load_stg_frame(self):
#       self.lf_frame.forget()
#       self.fn_frame.forget()
#
#       self.stg_frame = CTkFrame(self, width=300, height=400)
#       self.stg_frame.pack(padx=5, pady=5)
#       self.stg_frame.propagate(0)
#
#       # "Create WinP Reg Key" button
#       crg_button = CTkButton(
#           self.stg_frame,
#           text=translations[self.current_language]["Activate WinP Context Menu"],
#           width=200,
#           command=lambda: create_reg_key(True),
#       )
#       crg_button.pack(padx=5, pady=5)
#
#       # "Delete WinP Reg Key" button
#       drg_button = CTkButton(
#           self.stg_frame,
#           text=translations[self.current_language]["Disable WinP Context Menu"],
#           width=200,
#           command=lambda: delete_reg_key(True),
#       )
#       drg_button.pack(padx=5, pady=5)
#
#       # Language Selection
#       self.language_label = CTkLabel(self.stg_frame, text=translations[self.current_language]["Select Language"])
#       self.language_label.pack(padx=5, pady=5)
#
#       self.language_menu = CTkOptionMenu(
#           self.stg_frame,
#           values=["English", "Русский"],
#           command=lambda lang: self.change_language(
#               "en" if lang == "English" else "ru"
#           ),
#       )
#       self.language_menu.pack(padx=5, pady=5)
#
#       # "Back" button
#       bck_button = CTkButton(
#           self.stg_frame, text=translations[self.current_language]["Back"], command=lambda: self.load_functions_frame()
#       )
#       bck_button.pack(padx=5, pady=5, side=BOTTOM)
#
#       self.update_language()  # Update text after adding language settings
#
#   def load_arh_frame(self):
#       """
#       Loads the frame with archiving options.
#
#       This function creates a frame for archive operations, including selecting a file/folder, choosing between
#       file and folder compression, optional password setting, and buttons for archive and extract operations.
#       """
#       self.lf_frame.forget()
#       self.fn_frame.forget()
#
#       self.arh_frame = CTkFrame(self, width=300, height=400)
#       self.arh_frame.pack(padx=5, pady=5)
#       self.arh_frame.propagate(0)
#
#       self.file_path = ""
#       self.target_type = StringVar(value="file")  # Default to file
#
#       def select_target():
#           """Opens a dialog to select a file or folder."""
#           if self.target_type.get() == "file":
#               self.file_path = filedialog.askopenfilename(
#                   initialdir="/", title=translations[self.current_language]["Select File"]
#               )
#           else:
#               self.file_path = filedialog.askdirectory(
#                   initialdir="/", title="Select Folder"
#               )
#           file_path_label.configure(text=self.file_path)
#
#       # Button for selecting file/folder
#       select_target_button = CTkButton(
#           self.arh_frame, text=translations[self.current_language]["Select"], command=select_target
#       )
#       select_target_button.pack(padx=5, pady=5)
#
#       # Label to display the selected path
#       file_path_label = CTkLabel(self.arh_frame, text=translations[self.current_language]["File/Folder not selected"])
#       file_path_label.pack(pady=5)
#
#       # Radiobutton to choose between file and folder
#       file_radiobutton = CTkRadioButton(
#           self.arh_frame, text="File", variable=self.target_type, value="file"
#       )
#       file_radiobutton.pack(pady=5)
#       folder_radiobutton = CTkRadioButton(
#           self.arh_frame, text="Folder", variable=self.target_type, value="folder"
#       )
#       folder_radiobutton.pack(pady=5)
#
#       # Checkbox to enable password usage
#       self.use_password = IntVar(value=0)
#       password_checkbox = CTkCheckBox(
#           self.arh_frame,
#           text=translations[self.current_language]["Use Password?"],
#           variable=self.use_password,
#           command=self.toggle_password_entry,
#       )
#       password_checkbox.pack(pady=5)
#
#       # Entry field for password (initially disabled)
#       self.password_entry = CTkEntry(
#           self.arh_frame,
#           placeholder_text=translations[self.current_language]["Enter Password"],
#           show="*",
#           state="disabled",
#       )
#       self.password_entry.pack(pady=5)
#
#       # Functions for archiving and extracting
#       def archive():
#           if self.file_path:
#               password = (
#                   self.password_entry.get() if self.use_password.get() else None
#               )
#               try:
#                   compress_file(self.file_path, password)
#                   CTkMessagebox(
#                       title=translations[self.current_language]["Success"],
#                       message=f"File/folder '{self.file_path}' successfully archived.",
#                       option_1="OK",
#                   )
#               except Exception as e:
#                   CTkMessagebox(title=translations[self.current_language]["Error"], message=f"Error during archiving: {e}")
#
#       def extract():
#           if self.file_path:
#               password = (
#                   self.password_entry.get() if self.use_password.get() else None
#               )
#               try:
#                   decompress_file(self.file_path, password)
#                   CTkMessagebox(
#                       title=translations[self.current_language]["Success"],
#                       message=f"File/folder '{self.file_path}' successfully extracted.",
#                       option_1="OK",
#                   )
#               except RuntimeError as e:
#                   CTkMessagebox(
#                       title=translations[self.current_language]["Error"], message=f"Error during extraction: {e}"
#                   )
#               except Exception as e:
#                   CTkMessagebox(
#                       title=translations[self.current_language]["Error"], message=f"Error during extraction: {e}"
#                   )
#
#       # Buttons for archiving and extracting
#       archive_button = CTkButton(self.arh_frame, text=translations[self.current_language]["Archive"], command=archive)
#       archive_button.pack(pady=5)
#       extract_button = CTkButton(self.arh_frame, text=translations[self.current_language]["Extract"], command=extract)
#       extract_button.pack(pady=5)
#
#       # "Back" button
#       bck_button = CTkButton(
#           self.arh_frame, text=translations[self.current_language]["Back"], command=lambda: self.load_functions_frame()
#       )
#       bck_button.pack(padx=5, pady=5, side=BOTTOM)
#
#   def toggle_password_entry(self):
#       """Enables/disables password entry field."""
#       if self.use_password.get():
#           self.password_entry.configure(state="normal")
#       else:
#           self.password_entry.configure(state="disabled")
#
#   def CNV():
#       pass
#
#   def TMP():
#       pass
#
#   def convert_to(self, file_path, output_format):
#       """
#       Converts the given file to the specified output format and saves it to the Downloads folder.
#       """
#       def conversion_thread():
#           """Функция для выполнения конвертации в отдельном потоке."""
#           nonlocal output_file_path
#           try:
#               if output_format == "txt":
#                   with open(output_file_path, "w") as f:
#                       pass  # Просто создаем пустой текстовый файл
#               elif output_format == "jpg":
#                   img = Image.open(file_path).convert("RGB")
#                   img.save(output_file_path, "JPEG")
#               elif output_format == "png":
#                   img = Image.open(file_path)
#                   img.save(output_file_path, "PNG")
#               elif output_format == "gif":
#                   img = Image.open(file_path)
#                   img.save(output_file_path, "GIF")
#               elif output_format == "mp4":
#                   clip = mp.VideoFileClip(file_path)
#                   clip.write_videofile(output_file_path)
#               elif output_format == "avi":
#                   clip = mp.VideoFileClip(file_path)
#                   clip.write_videofile(output_file_path, codec="png")
#               elif output_format == "mov":
#                   clip = mp.VideoFileClip(file_path)
#                   clip.write_videofile(output_file_path, codec="libx264")  # H.264 codec
#               elif output_format == "mp3":
#                   audio = AudioSegment.from_file(file_path)
#                   audio.export(output_file_path, format="mp3")
#               elif output_format == "wav":
#                   audio = AudioSegment.from_file(file_path)
#                   audio.export(output_file_path, format="wav")
#               elif output_format == "ogg":
#                   audio = AudioSegment.from_file(file_path)
#                   audio.export(output_file_path, format="ogg")
#               # Добавьте аналогичные блоки elif для других форматов документов (PDF, DOC, DOCX и т. д.)
#               else:
#                   raise ValueError(
#                       f"Конвертация в {output_format} пока не реализована!"
#                   )
#
#               # Обновляем UI после успешной конвертации
#               self.conversion_progress.configure(text=translations[self.current_language]["Conversion complete!"])
#               if hasattr(self, "open_location_button"):
#                   self.open_location_button.configure(state="normal")
#               else:
#                   self.open_location_button = CTkButton(
#                       self.cnv_frame_r,
#                       text=translations[self.current_language]["Open File Location"],
#                       command=open_file_location,
#                   )
#                   self.open_location_button.pack(pady=10)
#           except Exception as e:
#               # Обновляем UI при ошибке
#               self.conversion_progress.configure(
#                   text=f"{translations[self.current_language]['Conversion failed:']} {str(e)}"
#               )
#
#       print(f"Конвертирую {file_path} в {output_format}")
#       file_name, _ = os.path.splitext(os.path.basename(file_path))
#       downloads_path = str(Path.home() / "Downloads")
#       output_file_path = os.path.join(
#           downloads_path, f"{file_name}.{output_format.lower()}"
#       )
#       print(f"Путь вывода: {output_file_path}")
#
#       self.conversion_progress.configure(text=translations[self.current_language]["Converting..."])
#       self.cnv_frame_r.update()  # Обновляем фрейм, чтобы отобразить метку
#
#       # Создаем и запускаем поток для конвертации
#       thread = threading.Thread(target=conversion_thread)
#       thread.start()
#
#       return output_file_path
#
#
#ef compress_selected():
#   """Archives selected files or folders in a separate thread.
#
#   This function is intended to be called from the context menu integration.
#   It retrieves the selected files/folders from the command line arguments and
#   archives each of them. Error messages are displayed using CTkMessagebox.
#   """
#
#   def archive_thread(items):
#       """Function for performing archiving in a separate thread."""
#       shell = win32com.client.Dispatch("WScript.Shell")
#       selected_items = shell.Selection.Item()
#       item = selected_items(0).Path
#
#       if not item:
#           root = tk.Tk()
#           root.withdraw()
#           CTkMessagebox(title="Error", message="No file or folder selected.")
#           root.mainloop()
#           return
#
#       try:
#           compress_file(item)
#           root = tk.Tk()
#           root.withdraw()
#           CTkMessagebox(
#               title="Success", message=f"'{item}' successfully archived."
#           )
#           root.mainloop()
#
#           # Открываем папку с архивом
#           folder_path = os.path.dirname(item)
#           subprocess.Popen(f'explorer /select,"{folder_path}"')
#
#       except Exception as e:
#           root = tk.Tk()
#           root.withdraw()
#           CTkMessagebox(title="Error", message=f"Error archiving '{item}': {e}")
#           root.mainloop()
#
#   # Create and start a separate thread for archiving
#   thread = threading.Thread(target=archive_thread, args=(sys.argv[1:],))
#   thread.start()
#   thread.join()  # Wait for the thread to complete
#
#
#ef extract_selected():
#   """Extracts selected archive files in a separate thread.
#
#   Similar to `compress_selected`, this function handles the context menu action
#   for extraction. It iterates through the provided file paths, attempting to
#   decompress each one. Any errors encountered during extraction are displayed
#   using CTkMessagebox.
#
#   This version also filters the provided file paths to only process files with
#   the extensions .zis, .zip, or .7zip.
#   """
#
#   def extract_thread(items):
#       """Function to perform extraction in a separate thread."""
#       shell = win32com.client.Dispatch("WScript.Shell")
#       selected_items = shell.Selection.Item()
#       item = selected_items(0).Path
#
#       if not item:
#           root = tk.Tk()
#           root.withdraw()
#           CTkMessagebox(title="Error", message="No file or folder selected.")
#           root.mainloop()
#           return
#
#       print(item)
#       # Check if the file has a valid archive extension
#       if not any(item.lower().endswith(ext) for ext in [".zis", ".zip", ".7zip"]):
#           root = tk.Tk()
#           root.withdraw()
#           CTkMessagebox(
#               title="Error", message=f"Unsupported file type: '{item}'"
#           )
#           root.mainloop()
#           return  # Skip to the next file
#
#       try:
#           decompress_file(item)
#           root = tk.Tk()
#           root.withdraw()
#           CTkMessagebox(
#               title="Success", message=f"'{item}' successfully extracted."
#           )
#           root.mainloop()
#
#           # Открываем папку с распакованными файлами
#           file_path = os.path.splitext(item)[
#               0
#           ]  # Убираем расширение архива
#           subprocess.Popen(f'explorer /select,"{file_path}"')
#
#       except RuntimeError as e:  # Catch potential password errors
#           root = tk.Tk()
#           root.withdraw()
#           CTkMessagebox(title="Error", message=f"Error extracting '{item}': {e}")
#           root.mainloop()
#       except Exception as e:
#           root = tk.Tk()
#           root.withdraw()
#           CTkMessagebox(title="Error", message=f"Error extracting '{item}': {e}")
#           root.mainloop()
#
#   # Create and start a separate thread for extraction
#   thread = threading.Thread(target=extract_thread, args=(sys.argv[1:],))
#   thread.start()
#   thread.join()  # Wait for the thread to complete
#
#ef create_reg_key(type=None):
#   """Creates a registry entry for the context menu."""
#   try:
#       python_path = sys.executable
#       script_path = os.path.abspath(__file__)
#
#       key_paths = {
#           "Archive File with WinP": r"Software\Classes\*\shell\ArchiveFile",
#           "Archive Folder with WinP": r"Software\Classes\Folder\shell\ArchiveFolder",
#       }
#
#       # Use unique keys for each file type
#       extract_key_paths = {
#           "Extract with WinP (.zis)": r"Software\Classes\.zis\shell\ExtractFile",
#           "Extract with WinP (.zip)": r"Software\Classes\.zip\shell\ExtractFile",
#           "Extract with WinP (.7z)": r"Software\Classes\.7z\shell\ExtractFile",
#       }
#
#       for menu_text, key_path in key_paths.items():
#           key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
#           winreg.SetValueEx(key, "", 0, winreg.REG_SZ, menu_text)
#           winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f"{script_path},0")
#
#           command_key = winreg.CreateKey(
#               winreg.HKEY_CURRENT_USER, key_path + r"\command"
#           )
#           winreg.SetValueEx(
#               command_key,
#               "",
#               0,
#               winreg.REG_SZ,
#               f'"{python_path}" "{script_path}" "%1"',
#           )
#           winreg.CloseKey(command_key)
#           winreg.CloseKey(key)
#
#       for menu_text, key_path in extract_key_paths.items():
#           key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
#           winreg.SetValueEx(key, "", 0, winreg.REG_SZ, menu_text)
#           winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f"{script_path},0")
#
#           command_key = winreg.CreateKey(
#               winreg.HKEY_CURRENT_USER, key_path + r"\command"
#           )
#           winreg.SetValueEx(
#               command_key,
#               "",
#               0,
#               winreg.REG_SZ,
#               f'"{python_path}" "{script_path}" "extract" "%1"',
#           )
#           winreg.CloseKey(command_key)
#           winreg.CloseKey(key)
#
#       return True
#   except Exception as e:
#       print(f"Error creating registry key: {e}")
#       return False
#
#
#ef delete_reg_key(type=None):
#   """Deletes existing registry entries.
#
#   This function now removes the incorrect entry that was associated with folders
#   and adds the removal of the specific file type entries.
#   """
#
#   try:
#       key_paths = [
#           r"Software\Classes\*\shell\ArchiveFile",
#           r"Software\Classes\Folder\shell\ArchiveFolder",
#           r"Software\Classes\.zis\shell\ExtractFile",
#           r"Software\Classes\.zip\shell\ExtractFile",
#           r"Software\Classes\.7z\shell\ExtractFile",
#       ]
#
#       for key_path in key_paths:
#           winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path + r"\command")
#           winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
#       if type:
#           print("Done")
#       return True
#   except FileNotFoundError:
#       return True  # Key not found - this is normal
#   except Exception as e:
#       print(f"Error deleting registry key: {e}")
#       return False
#
#
#f __name__ == "__main__":
#   if len(sys.argv) > 1 and sys.argv[1] == "extract":  # Check for "extract"
#       extract_selected()
#   elif len(sys.argv) > 1:  # If there are arguments, assume it's for archiving
#       compress_selected()
#   else:
#       app = WinPWindow()
#       app.mainloop()
#
#
# OLD VERSION
#
#import os
#import tkinter as tk
#from tkinter import filedialog
#from customtkinter import *
#from CTkMessagebox import CTkMessagebox
##from func.cnv import get_file_path
## from func.tmp import clean_unused_files,clean_registry,clean_temp_folder
#from func.arh import compress_file, decompress_file
#from webbrowser import open
#import subprocess
#import os
#import sys
#import win32com.client
#import winreg
#from pathlib import Path
#from PIL import Image
#import moviepy.editor as mp
#from pydub import AudioSegment
#import threading
#import time
#
#
#class WinPWindow(CTk):
#    def __init__(self):
#        super().__init__()
#        """
#        Initialize the application.
#
#        Instantiate the WinPWindow class, set the window size to 300x400,
#        and make it non-resizable.
#        Also, load the functions frame.
#        """
#        # self.iconbitmap("assets/winp.ico")
#        self.title("WinP: F17E7")
#        self.geometry("300x400")
#        self.resizable(False, False)
#        self.load_functions_frame()
#        
#        self.protocol(
#            "WM_DELETE_WINDOW", self.on_closing
#        )  # Вызов on_closing при закрытии
#
#    def on_closing(self):
#        """Функция, которая вызывается при закрытии окна."""
#        if CTkMessagebox(
#            title="Подтверждение выхода",
#            message="Вы уверены, что хотите выйти?",
#            icon="question",
#            option_1="Да",
#            option_2="Нет",
#        ).get() == "Да":
#            self.destroy()  # Закрываем окно
#            os._exit(0)  # Завершаем процесс Python
#
#    def function(self, name):
#        """
#        Handle the click event of a button to execute a specific function.
#
#        When a button is clicked, the name of the button is passed to this function.
#        It hides the main functions frame, creates a new frame for the selected function,
#        executes the function associated with the button name, and displays a 'Back' button
#        to return to the previous frame.
#        """
#        self.lf_frame.forget()
#        self.fn_frame = CTkFrame(self, width=300, height=400)
#        self.fn_frame.pack(padx=5, pady=5)
#        self.fn_frame.propagate(0)
#
#        fncs = {
#            "ARH": self.load_arh_frame,
#            "CNV": self.load_cnv_frame,
#            "TMP": lambda: print("TMP"),
#            "STG": self.load_stg_frame,
#        }
#
#        if name in fncs:
#            fncs[name]()
#
#        bck_button = CTkButton(
#            self.fn_frame, text="Back", command=lambda: self.load_functions_frame()
#        )
#        bck_button.pack(padx=5, pady=5, side=BOTTOM)
#
#    def clear_frame(self):
#        
#        try: self.stg_frame.forget()
#        except: pass
#        try: self.fn_frame.forget()
#        except: pass
#        try: self.arh_frame.forget()
#        except: pass
#        try: self.cnv_frame_l.forget();self.cnv_frame_r.forget()
#        except: pass
#        try: self.lf_frame.forget()
#        except: pass
#        
#        self.geometry("300x400")
#
#    def load_functions_frame(self):
#        """
#        Load the main functions frame.
#
#        If any secondary function frame (like archive frame) exists, it is forgotten (hidden).
#        Then, a new frame is created to hold the main function buttons (Archive, Converter, Optimizer).
#        """
#        self.clear_frame()
#        self.lf_frame = CTkFrame(self, width=300, height=400)
#        self.lf_frame.pack(padx=5, pady=5)
#        self.lf_frame.propagate(0)
#
#        arh_button = CTkButton(
#            self.lf_frame, text="Archivate", command=lambda: self.function("ARH")
#        )
#        arh_button.pack(padx=5, pady=5)
#        cnv_button = CTkButton(
#            self.lf_frame, text="Converter", command=lambda: self.function("CNV")
#        )
#        cnv_button.pack(padx=5, pady=5)
#        tmp_button = CTkButton(
#            self.lf_frame, text="Optimizer", command=lambda: self.function("TMP")
#        )
#        tmp_button.pack(padx=5, pady=5)
#        stg_button = CTkButton(
#            self.lf_frame, text="Settings", command=lambda: self.function("STG")
#        )
#        stg_button.pack(padx=5, pady=5)
#
#        dev_button = CTkButton(self.lf_frame,text="GitHub",command=lambda: open("https://github.com/SL1dee36"))
#        dev_button.pack(padx=5, pady=5, side=BOTTOM)
#
#    def load_cnv_frame(self):
#        """Loads the frame for file conversion with input and output options."""
#        self.clear_frame()
#        self.geometry("700x400")
#
#        self.cnv_frame_l = CTkFrame(self, width=300, height=400)
#        self.cnv_frame_l.pack(padx=5, pady=5, side=LEFT)
#        self.cnv_frame_l.propagate(0)
#
#        self.cnv_frame_r = CTkFrame(self, width=400, height=400, corner_radius=0)
#        self.cnv_frame_r.pack(side=LEFT)
#        self.cnv_frame_r.propagate(0)
#
#        def select_file():
#            """Opens a dialog to select a file and updates the file path label."""
#            self.file_path = filedialog.askopenfilename(
#                initialdir="/", title="Select File"
#            )
#            if self.file_path:
#                display_file_info()
#            # Update conversion options based on selected file type
#            update_conversion_options()
#
#        def display_file_info():
#            """Displays file information in the file_info_label."""
#            if not self.file_path:  # Проверка, выбран ли файл
#                return
#
#            file_name = os.path.basename(self.file_path)
#            file_size = os.path.getsize(self.file_path)
#            file_type = os.path.splitext(self.file_path)[1].lower()
#            
#            # Получаем время создания, изменения и последнего открытия
#            file_create_timestamp = os.path.getctime(self.file_path)
#            file_modify_timestamp = os.path.getmtime(self.file_path)
#            file_access_timestamp = os.path.getatime(self.file_path)
#
#            # Преобразуем временные метки в читаемый формат
#            file_create_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_create_timestamp))
#            file_update_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_modify_timestamp))
#            file_last_open_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_access_timestamp))
#
#            # Получаем атрибуты файла
#            file_modify = oct(os.stat(self.file_path).st_mode)[-3:]
#            if file_modify == "666":
#                file_modify = "None"
#
#            file_info_text = (
#                f"Файл : {file_name}\n"
#                f"Тип : {file_type}\n"
#                f"Размер : {file_size} байт\n"
#                f"На диске : {file_size} байт\n"
#                f"---------------------------\n"
#                f"Создан : {file_create_data}\n"
#                f"Изменен : {file_update_data}\n"
#                f"Открыт : {file_last_open_data}\n"
#                f"---------------------------\n"
#                f"Атрибуты : {file_modify}\n"
#            )
#            self.file_info_label.configure(text=file_info_text,justify=LEFT)
#
#        # Button to select a file
#        select_file_button = CTkButton(
#            self.cnv_frame_l, text="Select File", command=select_file
#        )
#        select_file_button.pack(padx=5, pady=10)
#
#        # --- Left Frame (File Input) ---
#        self.file_path = ""
#        self.file_info_label = CTkLabel(self.cnv_frame_l, text="")  # Новая метка для информации о файле
#        self.file_info_label.pack(pady=5)
#
#        # --- Right Frame (Conversion Options) ---
#        def segmented_button_callback(value):
#            # This function will be called every time the segment button changes
#            print("segmented button clicked:", value)
#            update_conversion_options()
#
#        self.segment_var = tk.StringVar(value="Image")
#        segmented_button = CTkSegmentedButton(
#            self.cnv_frame_r,
#            values=["Image", "Video", "Audio", "Document"],
#            command=segmented_button_callback,
#            variable=self.segment_var,
#        )
#        segmented_button.pack(pady=10)
#
#        # Conversion Options (Dynamically updated)
#        self.conversion_options_label = CTkLabel(
#            self.cnv_frame_r, text="Select a file to see conversion options."
#        )
#        self.conversion_options_label.pack(pady=5)
#
#        self.option_menu = CTkOptionMenu(
#            self.cnv_frame_r, variable=None, values=[]
#        )
#        self.option_menu.pack(pady=10)
#
#        # --- Conversion Progress Label ---
#        self.conversion_progress = CTkLabel(
#            self.cnv_frame_r, text="", font=("Arial", 10)
#        )
#        self.conversion_progress.pack()
#
#        # --- Function to Open Converted File Location ---
#        def open_file_location():
#            """Opens the file explorer to the location of the converted file."""
#            if hasattr(self, "converted_file_path"):
#                folder_path = os.path.dirname(self.converted_file_path)
#                subprocess.Popen(f'explorer /select,"{folder_path}"')
#            else:
#                CTkMessagebox(
#                    title="Error", message="File not yet converted or not found."
#                )
#
#        # --- Bottom Frame (Conversion Button and Open Location Button) ---
#        def convert_file():
#            """Handles the file conversion process."""
#            if self.file_path:
#                # Update progress label
#                self.conversion_progress.configure(text="Converting...")
#                self.cnv_frame_r.update()  # Update the frame to show the label
#
#                try:
#                    output_format = self.option_menu.get().lower()
#                    self.converted_file_path = self.convert_to(
#                        self.file_path, output_format
#                    )
#                    self.conversion_progress.configure(text="Conversion complete!")
#
#                    # Enable or create the "Open File Location" button
#                    if hasattr(self, "open_location_button"):
#                        self.open_location_button.configure(state="normal")
#                    else:
#                        self.open_location_button = CTkButton(
#                            self.cnv_frame_r,
#                            text="Open File Location",
#                            command=open_file_location,
#                        )
#                        self.open_location_button.pack(pady=10)
#
#                except Exception as e:
#                    self.conversion_progress.configure(
#                        text=f"Conversion failed: {str(e)}"
#                    )
#            else:
#                CTkMessagebox(title="Error", message="No file selected for conversion!")
#
#        self.download_button = CTkButton(
#            self.cnv_frame_r, text="Convert", command=convert_file
#        )
#        self.download_button.pack(pady=10)
#
#        # "Back" button
#        bck_button = CTkButton(
#            self.cnv_frame_l,
#            text="Back",
#            command=lambda: self.load_functions_frame(),
#        )
#        bck_button.pack(padx=5, pady=5, side=BOTTOM)
#
#        # --- Function to update conversion options based on file type ---
#        def update_conversion_options():
#            if self.file_path: # Проверяем, выбран ли файл
#                file_ext = os.path.splitext(self.file_path)[1].lower()
#                selected_category = self.segment_var.get()  # Get selected category
#
#                if selected_category == "Image":
#                    supported_formats = ["PNG", "JPG", "JPEG", "GIF"]  # Example
#                elif selected_category == "Video":
#                    supported_formats = ["MP4", "AVI", "MOV"]  # Example
#                elif selected_category == "Audio":
#                    supported_formats = ["MP3", "WAV", "OGG"]  # Example
#                elif selected_category == "Document":
#                    supported_formats = ["TXT", "PDF", "DOC", "DOCX"]  # Example
#                else:
#                    supported_formats = []
#
#                self.conversion_options_label.configure(
#                    text=f"Convert to: ({selected_category})"
#                )
#                self.option_menu.configure(values=supported_formats)
#                if supported_formats:
#                    self.option_menu.set(
#                        supported_formats[0]
#                    )  # Set a default option
#
#    def load_stg_frame(self):
#        self.lf_frame.forget()
#        self.fn_frame.forget()
#
#        self.stg_frame = CTkFrame(self, width=300, height=400)
#        self.stg_frame.pack(padx=5, pady=5)
#        self.stg_frame.propagate(0)
#
#        # "Create WinP Reg Key" button
#        crg_button = CTkButton(
#            self.stg_frame,
#            text="Activate WinP Context Menu",
#            width=200,
#            command=lambda: create_reg_key(True),
#        )
#        crg_button.pack(padx=5, pady=5)
#
#        # "Delete WinP Reg Key" button
#        drg_button = CTkButton(
#            self.stg_frame,
#            text="Disable WinP Context Menu",
#            width=200,
#            command=lambda: delete_reg_key(True),
#        )
#        drg_button.pack(padx=5, pady=5)
#
#        # "Back" button
#        bck_button = CTkButton(
#            self.stg_frame, text="Back", command=lambda: self.load_functions_frame()
#        )
#        bck_button.pack(padx=5, pady=5, side=BOTTOM)
#
#    def load_arh_frame(self):
#        """
#        Loads the frame with archiving options.
#
#        This function creates a frame for archive operations, including selecting a file/folder, choosing between
#        file and folder compression, optional password setting, and buttons for archive and extract operations.
#        """
#        self.lf_frame.forget()
#        self.fn_frame.forget()
#
#        self.arh_frame = CTkFrame(self, width=300, height=400)
#        self.arh_frame.pack(padx=5, pady=5)
#        self.arh_frame.propagate(0)
#
#        self.file_path = ""
#        self.target_type = StringVar(value="file")  # Default to file
#
#        def select_target():
#            """Opens a dialog to select a file or folder."""
#            if self.target_type.get() == "file":
#                self.file_path = filedialog.askopenfilename(
#                    initialdir="/", title="Select File"
#                )
#            else:
#                self.file_path = filedialog.askdirectory(
#                    initialdir="/", title="Select Folder"
#                )
#            file_path_label.configure(text=self.file_path)
#
#        # Button for selecting file/folder
#        select_target_button = CTkButton(
#            self.arh_frame, text="Select", command=select_target
#        )
#        select_target_button.pack(padx=5, pady=5)
#
#        # Label to display the selected path
#        file_path_label = CTkLabel(self.arh_frame, text="File/Folder not selected")
#        file_path_label.pack(pady=5)
#
#        # Radiobutton to choose between file and folder
#        file_radiobutton = CTkRadioButton(
#            self.arh_frame, text="File", variable=self.target_type, value="file"
#        )
#        file_radiobutton.pack(pady=5)
#        folder_radiobutton = CTkRadioButton(
#            self.arh_frame, text="Folder", variable=self.target_type, value="folder"
#        )
#        folder_radiobutton.pack(pady=5)
#
#        # Checkbox to enable password usage
#        self.use_password = IntVar(value=0)
#        password_checkbox = CTkCheckBox(
#            self.arh_frame,
#            text="Use Password?",
#            variable=self.use_password,
#            command=self.toggle_password_entry,
#        )
#        password_checkbox.pack(pady=5)
#
#        # Entry field for password (initially disabled)
#        self.password_entry = CTkEntry(
#            self.arh_frame,
#            placeholder_text="Enter Password",
#            show="*",
#            state="disabled",
#        )
#        self.password_entry.pack(pady=5)
#
#        # Functions for archiving and extracting
#        def archive():
#            if self.file_path:
#                password = (
#                    self.password_entry.get() if self.use_password.get() else None
#                )
#                try:
#                    compress_file(self.file_path, password)
#                    CTkMessagebox(
#                        title="Success",
#                        message=f"File/folder '{self.file_path}' successfully archived.",
#                        option_1="OK",
#                    )
#                except Exception as e:
#                    CTkMessagebox(title="Error", message=f"Error during archiving: {e}")
#
#        def extract():
#            if self.file_path:
#                password = (
#                    self.password_entry.get() if self.use_password.get() else None
#                )
#                try:
#                    decompress_file(self.file_path, password)
#                    CTkMessagebox(
#                        title="Success",
#                        message=f"File/folder '{self.file_path}' successfully extracted.",
#                        option_1="OK",
#                    )
#                except RuntimeError as e:
#                    CTkMessagebox(
#                        title="Error", message=f"Error during extraction: {e}"
#                    )
#                except Exception as e:
#                    CTkMessagebox(
#                        title="Error", message=f"Error during extraction: {e}"
#                    )
#
#        # Buttons for archiving and extracting
#        archive_button = CTkButton(self.arh_frame, text="Archive", command=archive)
#        archive_button.pack(pady=5)
#        extract_button = CTkButton(self.arh_frame, text="Extract", command=extract)
#        extract_button.pack(pady=5)
#
#        # "Back" button
#        bck_button = CTkButton(
#            self.arh_frame, text="Back", command=lambda: self.load_functions_frame()
#        )
#        bck_button.pack(padx=5, pady=5, side=BOTTOM)
#
#    def toggle_password_entry(self):
#        """Enables/disables password entry field."""
#        if self.use_password.get():
#            self.password_entry.configure(state="normal")
#        else:
#            self.password_entry.configure(state="disabled")
#
#    def CNV():
#        pass
#
#    def TMP():
#        pass
#
#    def convert_to(self, file_path, output_format):
#        """
#        Converts the given file to the specified output format and saves it to the Downloads folder.
#        """
#        def conversion_thread():
#            """Функция для выполнения конвертации в отдельном потоке."""
#            nonlocal output_file_path
#            try:
#                if output_format == "txt":
#                    with open(output_file_path, "w") as f:
#                        pass  # Просто создаем пустой текстовый файл
#                elif output_format == "jpg":
#                    img = Image.open(file_path).convert("RGB")
#                    img.save(output_file_path, "JPEG")
#                elif output_format == "png":
#                    img = Image.open(file_path)
#                    img.save(output_file_path, "PNG")
#                elif output_format == "gif":
#                    img = Image.open(file_path)
#                    img.save(output_file_path, "GIF")
#                elif output_format == "mp4":
#                    clip = mp.VideoFileClip(file_path)
#                    clip.write_videofile(output_file_path)
#                elif output_format == "avi":
#                    clip = mp.VideoFileClip(file_path)
#                    clip.write_videofile(output_file_path, codec="png")
#                elif output_format == "mov":
#                    clip = mp.VideoFileClip(file_path)
#                    clip.write_videofile(output_file_path, codec="libx264")  # H.264 codec
#                elif output_format == "mp3":
#                    audio = AudioSegment.from_file(file_path)
#                    audio.export(output_file_path, format="mp3")
#                elif output_format == "wav":
#                    audio = AudioSegment.from_file(file_path)
#                    audio.export(output_file_path, format="wav")
#                elif output_format == "ogg":
#                    audio = AudioSegment.from_file(file_path)
#                    audio.export(output_file_path, format="ogg")
#                # Добавьте аналогичные блоки elif для других форматов документов (PDF, DOC, DOCX и т. д.)
#                else:
#                    raise ValueError(
#                        f"Конвертация в {output_format} пока не реализована!"
#                    )
#
#                # Обновляем UI после успешной конвертации
#                self.conversion_progress.configure(text="Конвертация завершена!")
#                if hasattr(self, "open_location_button"):
#                    self.open_location_button.configure(state="normal")
#                else:
#                    self.open_location_button = CTkButton(
#                        self.cnv_frame_r,
#                        text="Открыть расположение файла",
#                        command=open_file_location,
#                    )
#                    self.open_location_button.pack(pady=10)
#            except Exception as e:
#                # Обновляем UI при ошибке
#                self.conversion_progress.configure(
#                    text=f"Ошибка конвертации: {str(e)}"
#                )
#
#        print(f"Конвертирую {file_path} в {output_format}")
#        file_name, _ = os.path.splitext(os.path.basename(file_path))
#        downloads_path = str(Path.home() / "Downloads")
#        output_file_path = os.path.join(
#            downloads_path, f"{file_name}.{output_format.lower()}"
#        )
#        print(f"Путь вывода: {output_file_path}")
#
#        self.conversion_progress.configure(text="Конвертирую...")
#        self.cnv_frame_r.update()  # Обновляем фрейм, чтобы отобразить метку
#
#        # Создаем и запускаем поток для конвертации
#        thread = threading.Thread(target=conversion_thread)
#        thread.start()
#
#        return output_file_path
#
#
#def compress_selected():
#    """Archives selected files or folders in a separate thread.
#
#    This function is intended to be called from the context menu integration.
#    It retrieves the selected files/folders from the command line arguments and
#    archives each of them. Error messages are displayed using CTkMessagebox.
#    """
#
#    def archive_thread(items):
#        """Function for performing archiving in a separate thread."""
#        shell = win32com.client.Dispatch("WScript.Shell")
#        selected_items = shell.Selection.Item()
#        item = selected_items(0).Path
#
#        if not item:
#            root = tk.Tk()
#            root.withdraw()
#            CTkMessagebox(title="Error", message="No file or folder selected.")
#            root.mainloop()
#            return
#
#        try:
#            compress_file(item)
#            root = tk.Tk()
#            root.withdraw()
#            CTkMessagebox(
#                title="Success", message=f"'{item}' successfully archived."
#            )
#            root.mainloop()
#
#            # Открываем папку с архивом
#            folder_path = os.path.dirname(item)
#            subprocess.Popen(f'explorer /select,"{folder_path}"')
#
#        except Exception as e:
#            root = tk.Tk()
#            root.withdraw()
#            CTkMessagebox(title="Error", message=f"Error archiving '{item}': {e}")
#            root.mainloop()
#
#    # Create and start a separate thread for archiving
#    thread = threading.Thread(target=archive_thread, args=(sys.argv[1:],))
#    thread.start()
#    thread.join()  # Wait for the thread to complete
#
#
#def extract_selected():
#    """Extracts selected archive files in a separate thread.
#
#    Similar to `compress_selected`, this function handles the context menu action
#    for extraction. It iterates through the provided file paths, attempting to
#    decompress each one. Any errors encountered during extraction are displayed
#    using CTkMessagebox.
#
#    This version also filters the provided file paths to only process files with
#    the extensions .zis, .zip, or .7zip.
#    """
#
#    def extract_thread(items):
#        """Function to perform extraction in a separate thread."""
#        shell = win32com.client.Dispatch("WScript.Shell")
#        selected_items = shell.Selection.Item()
#        item = selected_items(0).Path
#
#        if not item:
#            root = tk.Tk()
#            root.withdraw()
#            CTkMessagebox(title="Error", message="No file or folder selected.")
#            root.mainloop()
#            return
#
#        print(item)
#        # Check if the file has a valid archive extension
#        if not any(item.lower().endswith(ext) for ext in [".zis", ".zip", ".7zip"]):
#            root = tk.Tk()
#            root.withdraw()
#            CTkMessagebox(
#                title="Error", message=f"Unsupported file type: '{item}'"
#            )
#            root.mainloop()
#            return  # Skip to the next file
#
#        try:
#            decompress_file(item)
#            root = tk.Tk()
#            root.withdraw()
#            CTkMessagebox(
#                title="Success", message=f"'{item}' successfully extracted."
#            )
#            root.mainloop()
#
#            # Открываем папку с распакованными файлами
#            file_path = os.path.splitext(item)[
#                0
#            ]  # Убираем расширение архива
#            subprocess.Popen(f'explorer /select,"{file_path}"')
#
#        except RuntimeError as e:  # Catch potential password errors
#            root = tk.Tk()
#            root.withdraw()
#            CTkMessagebox(title="Error", message=f"Error extracting '{item}': {e}")
#            root.mainloop()
#        except Exception as e:
#            root = tk.Tk()
#            root.withdraw()
#            CTkMessagebox(title="Error", message=f"Error extracting '{item}': {e}")
#            root.mainloop()
#
#    # Create and start a separate thread for extraction
#    thread = threading.Thread(target=extract_thread, args=(sys.argv[1:],))
#    thread.start()
#    thread.join()  # Wait for the thread to complete
#
#
#def create_reg_key(type=None):
#    """Creates a registry entry for the context menu."""
#    try:
#        python_path = sys.executable
#        script_path = os.path.abspath(__file__)
#
#        key_paths = {
#            "Archive File with WinP": r"Software\Classes\*\shell\ArchiveFile",
#            "Archive Folder with WinP": r"Software\Classes\Folder\shell\ArchiveFolder",
#        }
#
#        # Use unique keys for each file type
#        extract_key_paths = {
#            "Extract with WinP (.zis)": r"Software\Classes\.zis\shell\ExtractFile",
#            "Extract with WinP (.zip)": r"Software\Classes\.zip\shell\ExtractFile",
#            "Extract with WinP (.7z)": r"Software\Classes\.7z\shell\ExtractFile",
#        }
#
#        for menu_text, key_path in key_paths.items():
#            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
#            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, menu_text)
#            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f"{script_path},0")
#
#            command_key = winreg.CreateKey(
#                winreg.HKEY_CURRENT_USER, key_path + r"\command"
#            )
#            winreg.SetValueEx(
#                command_key,
#                "",
#                0,
#                winreg.REG_SZ,
#                f'"{python_path}" "{script_path}" "%1"',
#            )
#            winreg.CloseKey(command_key)
#            winreg.CloseKey(key)
#
#        for menu_text, key_path in extract_key_paths.items():
#            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
#            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, menu_text)
#            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f"{script_path},0")
#
#            command_key = winreg.CreateKey(
#                winreg.HKEY_CURRENT_USER, key_path + r"\command"
#            )
#            winreg.SetValueEx(
#                command_key,
#                "",
#                0,
#                winreg.REG_SZ,
#                f'"{python_path}" "{script_path}" "extract" "%1"',
#            )
#            winreg.CloseKey(command_key)
#            winreg.CloseKey(key)
#
#        return True
#    except Exception as e:
#        print(f"Error creating registry key: {e}")
#        return False
#
#
#def delete_reg_key(type=None):
#    """Deletes existing registry entries.
#
#    This function now removes the incorrect entry that was associated with folders
#    and adds the removal of the specific file type entries.
#    """
#
#    try:
#        key_paths = [
#            r"Software\Classes\*\shell\ArchiveFile",
#            r"Software\Classes\Folder\shell\ArchiveFolder",
#            r"Software\Classes\.zis\shell\ExtractFile",
#            r"Software\Classes\.zip\shell\ExtractFile",
#            r"Software\Classes\.7z\shell\ExtractFile",
#        ]
#
#        for key_path in key_paths:
#            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path + r"\command")
#            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
#        if type:
#            print("Done")
#        return True
#    except FileNotFoundError:
#        return True  # Key not found - this is normal
#    except Exception as e:
#        print(f"Error deleting registry key: {e}")
#        return False
#
#
#if __name__ == "__main__":
#    if len(sys.argv) > 1 and sys.argv[1] == "extract":  # Check for "extract"
#        extract_selected()
#    elif len(sys.argv) > 1:  # If there are arguments, assume it's for archiving
#        compress_selected()
#    else:
#        # if delete_reg_key() and create_reg_key():
#        #    print("Registry entry successfully updated.")
#        # else:
#        #    print("Error updating registry entry.")
#
#        app = WinPWindow()
#        app.mainloop()
#
################################################################################################################################