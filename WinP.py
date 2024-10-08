# created by Nazaryan Artem
# Github @sl1de36 | Telegram @slide36

import tkinter as tk
from tkinter import filedialog
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from packages.func.arh import compress_file, decompress_file, set_icon_for_extension, remove_icon_for_extension
from packages.func.tmp import *
from packages.func.ctmenu import *
import webbrowser, subprocess, os, sys, win32com.client, win32con, win32api, winreg, tempfile
import json, datetime, shutil, gc, shutil, psutil, threading, time, pystray
import pywinstyles
from pathlib import Path
from PIL import Image
import moviepy.editor as mp
from pydub import AudioSegment
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

from packages.data.lang import translations
from packages.func.themes import *
class WinPWindow(CTk):
    def __init__(self):
        super().__init__()

        self.current_language = "en"  # Default language
        self.title("WinP: F27e8 0.50.10")

        # Инициализация настроек
        self.current_theme = "default"

        try: self.iconbitmap("packages/assets/winp.ico") 
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

        self.settings_path_debug = "packages/data/settings.json"
        self.settings_path_correct = "_internal/data/settings.json"
        self.icon_path_debug = "packages/assets/zis_folder.ico" 
        self.icon_path_correct = "_internal/zis_folder.ico" 

        self.Extended_menu = False
        self.file_info_text = ""

        self.correct_packages()
        self.load_settings()
        self.load_functions_frame()
        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )  # Вызов on_closing при закрытии

    def correct_packages(self):
        try:
            with open(self.settings_path_correct, "r") as f:
                settings = json.load(f)
            self.settings_path = self.settings_path_correct
        except: self.settings_path = self.settings_path_debug

        try:
            if os.path.isfile(self.icon_path_correct):
                self.icon_path = self.icon_path_correct
            else:
                self.icon_path = self.icon_path_debug
        except: pass

        print(self.settings_path, self.icon_path)

    def load_settings(self):
        """Loads settings from settings.json."""
        try:
            with open(self.settings_path, "r") as f:
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
        settings = {
            "language": self.current_language,
            "run_on_startup": self.run_on_startup,
        }
        with open(self.settings_path, "w") as f:
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
    
    def create_theme_menu(self):
            self.theme_menu = CTkOptionMenu(self.spec_frame, values=["Default", "Dark", "Light", "Blue", "Green", "Red"], command=self.change_theme)
            self.theme_menu.pack(pady=5,padx=5,side='right',anchor='se')

    def change_theme(self, theme):
            self.current_theme = theme.lower()
        
    def apply_theme(self):
        if self.current_theme == "default":
            set_appearance_mode("System")  # Стандарт
        elif self.current_theme == "dark":
            set_appearance_mode("dark")  # Темная тема
        elif self.current_theme == "light":
            set_appearance_mode("light")  # Светлая тема
        elif self.current_theme == "blue":
            set_appearance_mode("blue")  # Темно-синяя тема (не стандартная, задайте стиль для blue)
            # Вы можете настроить ваши собственные цвета
        elif self.current_theme == "green":
            set_appearance_mode("green")  # Темно-зеленая тема (не стандартная)
            # Настройки аналогично
        elif self.current_theme == "red":
            set_appearance_mode("red")  # Темно-красная тема (не стандартная)
            # Настройки аналогично

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
            
            print(self.file_path)

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

        def dnd_cnv_func(files):
            # Ensure files is a list and get the first element
            if isinstance(files, (list, tuple)) and files:
                self.file_path = files[0]  # Get the first dropped file
            else:
                self.file_path = ''
                print("Invalid file dropped:", files) 
                return  # Handle cases where dropping might not give a list

            display_file_info()
            
            
        # Button for selecting file/folder\

        self.dnd_cnv_place = CTkFrame(self.cnv_frame_l,width=250,height=120)
        self.dnd_cnv_place.pack(pady=5,padx=15)
        self.dnd_cnv_place.propagate(0)

        self.dnd_cnv_label = CTkLabel(self.dnd_cnv_place,text='\n\nDrag & Drop\nor',width=250,height=60)#translations[self.current_language]["File/Folder not selected"])
        self.dnd_cnv_label.pack(padx=5)

        # Button to select a file
        select_file_button = CTkButton(
            self.dnd_cnv_place,
            text=translations[self.current_language]["Select File"],
            command=select_file, width=250
        )
        select_file_button.pack(padx=5, pady=5,side=BOTTOM)

        self.file_path = ""
        self.file_info_label = CTkLabel(
            self.cnv_frame_l, text=""
        )  # New label for file information
        self.file_info_label.pack(pady=5)

        pywinstyles.apply_dnd(self.dnd_cnv_place, dnd_cnv_func)

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
            command=lambda: self.load_functions_frame(),width=250
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
                    supported_formats = ["PNG", "JPG", "JPEG", "GIF", "ICO"]
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

        extension = ".zis"  # Замените на ваше расширение

        ico_button = CTkButton(
            self.stg_frame,
            text='Setup WinP ".zis" icons',#translations[self.current_language]["Disable WinP Context Menu"],
            width=200,
            command=lambda: set_icon_for_extension(extension, self.icon_path),
        )
        ico_button.pack(padx=5, pady=5)

        ico_uninst_button = CTkButton(
            self.stg_frame,
            text='Setup WinP ".zis" icons',#translations[self.current_language]["Disable WinP Context Menu"],
            width=200,
            command=lambda: remove_icon_for_extension(extension),
        )
        ico_uninst_button.pack(padx=5, pady=5)

        self.spec_frame = CTkFrame(self.stg_frame, width=250, height=100)
        self.spec_frame.pack(padx=5, pady=5)
        self.spec_frame.propagate(0)

        # Языковая метка
        self.language_label = CTkLabel(self.spec_frame, text=translations[self.current_language]["Select Language"])
        self.language_label.pack(side='left', padx=5, pady=5, anchor='nw')  # Слева

        # Получаем список доступных языков из словаря переводов
        available_languages = list(translations.keys())
        language_names = {
            "en": "English",
            "ru": "Русский",
            "de": "Deutsch",
            "fr": "Français",
            "hy": "Հայոց լեզու"
        }

        # Отображаемые языки
        display_languages = [language_names.get(lang, lang) for lang in available_languages]

        # Выпадающее меню для выбора языка
        self.language_menu = CTkOptionMenu(
            self.spec_frame,
            values=display_languages,
            command=lambda lang: self.change_language(
                available_languages[display_languages.index(lang)]
            )
        )
        self.language_menu.pack(side='right', padx=5, pady=5,anchor='ne')  # Слева

        # Метка для выбора тем
        self.label = CTkLabel(self.spec_frame, text="Выберите тему:",anchor='sw')
        self.label.pack(side='left', padx=5, pady=5)

        # Создание элементов управления для темы
        self.theme_menu = CTkOptionMenu(self.spec_frame, values=["Default", "Dark", "Light", "Blue", "Green", "Red"], command=self.change_theme,anchor='se')
        self.theme_menu.pack(pady=5,padx=5,side='right')
        # Кнопка для применения темы
        self.apply_theme_button = CTkButton(self.spec_frame, text="Применить тему", command=self.apply_theme)
        self.apply_theme_button.pack(side='bottom', padx=5, pady=5)

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

        def drop_func(files):
            for file in files:
                print(file)

                self.file_path = f"{file}"
                self.file_path_label.configure(text=f'{os.path.basename(self.file_path)}')
        # Button for selecting file/folder\

        self.dragndrop_place = CTkFrame(self.arh_frame,width=250,height=120)
        self.dragndrop_place.pack(pady=5,padx=15)
        self.dragndrop_place.propagate(0)

        self.dragndrop_label = CTkLabel(self.dragndrop_place,text='\n\nDrag & Drop\nor',width=250,height=60)#translations[self.current_language]["File/Folder not selected"])
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