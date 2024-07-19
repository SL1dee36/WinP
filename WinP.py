# created by Nazaryan Artem
# Github @sl1de36 | Telegram @slide36

import os
import tkinter as tk
from tkinter import filedialog
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from func.arh import compress_file, decompress_file
from webbrowser import open_new
import subprocess
import os
import sys
import win32com.client
import winreg
from pathlib import Path
from PIL import Image
import moviepy.editor as mp
from pydub import AudioSegment
import threading
import time
import pystray
from PIL import Image
import json

from data.lang import translations


class WinPWindow(CTk):
    def __init__(self):
        super().__init__()

        self.current_language = "en"  # Default language
        self.title("WinP: F20e7")
        # self.iconbitmap("assets/winp.ico")
        self.geometry("300x400")
        self.resizable(False, False)

        self.lf_frame = None
        self.fn_frame = None
        self.arh_frame = None
        self.cnv_frame_l = None
        self.cnv_frame_r = None
        self.stg_frame = None

        self.load_settings()
        self.load_functions_frame()
        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )  # Вызов on_closing при закрытии


    def load_settings(self):
        """Loads settings from settings.json."""
        try:
            with open("data/settings.json", "r") as f:
                settings = json.load(f)
            self.current_language = settings.get("language", "en")
            self.run_on_startup = settings.get("run_on_startup", False)
        except FileNotFoundError:
            # If settings file not found, use default settings
            self.current_language = "en"
            self.run_on_startup = False

    def save_settings(self):
        """Saves settings to settings.json."""
        settings = {
            "language": self.current_language,
            "run_on_startup": self.run_on_startup,
        }
        with open(r"data/settings.json", "w") as f:
            json.dump(settings, f)

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
            self.cnv_frame_r,
            self.stg_frame,
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
        icon_image = Image.open(r"assets\winp.ico")

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
            "TMP": lambda: print("TMP"),
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
                      self.cnv_frame_l, self.cnv_frame_r, self.lf_frame]:
            try:
                frame.forget()
            except AttributeError:
                pass
        
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

        dev_button = CTkButton(self.lf_frame,text=translations[self.current_language]["GitHub"],command=lambda: open_new("https://github.com/SL1dee36"))
        dev_button.pack(padx=5, pady=5, side=BOTTOM)

        # Translate initial text
        self.update_language() 

    def load_cnv_frame(self):
        """Loads the frame for file conversion with input and output options."""
        self.clear_frame()
        self.geometry("700x400")

        self.cnv_frame_l = CTkFrame(self, width=300, height=400)
        self.cnv_frame_l.pack(padx=5, pady=5, side=LEFT)
        self.cnv_frame_l.propagate(0)

        self.cnv_frame_r = CTkFrame(self, width=400, height=400, corner_radius=0)
        self.cnv_frame_r.pack(side=LEFT)
        self.cnv_frame_r.propagate(0)

        # --- Left Frame (File Input) ---

        def select_file():
            """Opens a dialog to select a file and updates the file path label."""
            self.file_path = filedialog.askopenfilename(
                initialdir="/", title=translations[self.current_language]["Select File"]
            )
            if self.file_path:
                display_file_info()
            # Update conversion options based on selected file type
            update_conversion_options()

        def display_file_info():
            """Displays file information in the file_info_label."""
            if not self.file_path:  # Проверка, выбран ли файл
                return

            file_name = os.path.basename(self.file_path)
            file_size = os.path.getsize(self.file_path)
            file_type = os.path.splitext(self.file_path)[1].lower()
            
            # Получаем время создания, изменения и последнего открытия
            file_create_timestamp = os.path.getctime(self.file_path)
            file_modify_timestamp = os.path.getmtime(self.file_path)
            file_access_timestamp = os.path.getatime(self.file_path)

            # Преобразуем временные метки в читаемый формат
            file_create_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_create_timestamp))
            file_update_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_modify_timestamp))
            file_last_open_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_access_timestamp))

            # Получаем атрибуты файла
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
            self.file_info_label.configure(text=file_info_text,justify=LEFT)

        # Button to select a file
        select_file_button = CTkButton(
            self.cnv_frame_l, text=translations[self.current_language]["Select File"], command=select_file
        )
        select_file_button.pack(padx=5, pady=10)

        self.file_path = ""
        self.file_info_label = CTkLabel(self.cnv_frame_l, text="")  # Новая метка для информации о файле
        self.file_info_label.pack(pady=5)

        # --- Right Frame (Conversion Options) ---
        def segmented_button_callback(value):
            # This function will be called every time the segment button changes
            print("segmented button clicked:", value)
            update_conversion_options()

        self.segment_var = tk.StringVar(value="Image")
        segmented_button = CTkSegmentedButton(
            self.cnv_frame_r,
            values=[translations[self.current_language]["Image"], translations[self.current_language]["Video"], translations[self.current_language]["Audio"], translations[self.current_language]["Document"]],
            command=segmented_button_callback,
            variable=self.segment_var,
        )
        segmented_button.pack(pady=10)

        # Conversion Options (Dynamically updated)
        self.conversion_options_label = CTkLabel(
            self.cnv_frame_r, text=translations[self.current_language]["Select a file to see conversion options."]
        )
        self.conversion_options_label.pack(pady=5)

        self.option_menu = CTkOptionMenu(
            self.cnv_frame_r, variable=None, values=[]
        )
        self.option_menu.pack(pady=10)

        # --- Conversion Progress Label ---
        self.conversion_progress = CTkLabel(
            self.cnv_frame_r, text="", font=("Arial", 10)
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
                    title=translations[self.current_language]["Error"], message=translations[self.current_language]["File not yet converted or not found."]
                )

        # --- Bottom Frame (Conversion Button and Open Location Button) ---
        def convert_file():
            """Handles the file conversion process."""
            if self.file_path:
                # Update progress label
                self.conversion_progress.configure(text=translations[self.current_language]["Converting..."])
                self.cnv_frame_r.update()  # Update the frame to show the label

                try:
                    output_format = self.option_menu.get().lower()
                    self.converted_file_path = self.convert_to(
                        self.file_path, output_format
                    )
                    self.conversion_progress.configure(text=translations[self.current_language]["Conversion complete!"])

                    # Enable or create the "Open File Location" button
                    if hasattr(self, "open_location_button"):
                        self.open_location_button.configure(state="normal")
                    else:
                        self.open_location_button = CTkButton(
                            self.cnv_frame_r,
                            text=translations[self.current_language]["Open File Location"],
                            command=open_file_location,
                        )
                        self.open_location_button.pack(pady=10)

                except Exception as e:
                    self.conversion_progress.configure(
                        text=f"{translations[self.current_language]['Conversion failed:']} {str(e)}"
                    )
            else:
                CTkMessagebox(title=translations[self.current_language]["Error"], message=translations[self.current_language]["No file selected for conversion!"])

        self.download_button = CTkButton(
            self.cnv_frame_r, text=translations[self.current_language]["Convert"], command=convert_file
        )
        self.download_button.pack(pady=10)

        # "Back" button
        bck_button = CTkButton(
            self.cnv_frame_l,
            text=translations[self.current_language]["Back"],
            command=lambda: self.load_functions_frame(),
        )
        bck_button.pack(padx=5, pady=5, side=BOTTOM)

        # --- Function to update conversion options based on file type ---
        def update_conversion_options():
            if self.file_path: # Проверяем, выбран ли файл
                file_ext = os.path.splitext(self.file_path)[1].lower()
                selected_category = self.segment_var.get()  # Get selected category

                if selected_category == translations[self.current_language]["Image"]:
                    supported_formats = ["PNG", "JPG", "JPEG", "GIF"]  # Example
                elif selected_category == translations[self.current_language]["Video"]:
                    supported_formats = ["MP4", "AVI", "MOV"]  # Example
                elif selected_category == translations[self.current_language]["Audio"]:
                    supported_formats = ["MP3", "WAV", "OGG"]  # Example
                elif selected_category == translations[self.current_language]["Document"]:
                    supported_formats = ["TXT", "PDF", "DOC", "DOCX"]  # Example
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
            file_path_label.configure(text=self.file_path)

        # Button for selecting file/folder
        select_target_button = CTkButton(
            self.arh_frame, text=translations[self.current_language]["Select"], command=select_target
        )
        select_target_button.pack(padx=5, pady=5)

        # Label to display the selected path
        file_path_label = CTkLabel(self.arh_frame, text=translations[self.current_language]["File/Folder not selected"])
        file_path_label.pack(pady=5)

        # Radiobutton to choose between file and folder
        file_radiobutton = CTkRadioButton(
            self.arh_frame, text="File", variable=self.target_type, value="file"
        )
        file_radiobutton.pack(pady=5)
        folder_radiobutton = CTkRadioButton(
            self.arh_frame, text="Folder", variable=self.target_type, value="folder"
        )
        folder_radiobutton.pack(pady=5)

        # Checkbox to enable password usage
        self.use_password = IntVar(value=0)
        password_checkbox = CTkCheckBox(
            self.arh_frame,
            text=translations[self.current_language]["Use Password?"],
            variable=self.use_password,
            command=self.toggle_password_entry,
        )
        password_checkbox.pack(pady=5)

        # Entry field for password (initially disabled)
        self.password_entry = CTkEntry(
            self.arh_frame,
            placeholder_text=translations[self.current_language]["Enter Password"],
            show="*",
            state="disabled",
        )
        self.password_entry.pack(pady=5)

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

        # Buttons for archiving and extracting
        archive_button = CTkButton(self.arh_frame, text=translations[self.current_language]["Archive"], command=archive)
        archive_button.pack(pady=5)
        extract_button = CTkButton(self.arh_frame, text=translations[self.current_language]["Extract"], command=extract)
        extract_button.pack(pady=5)

        # "Back" button
        bck_button = CTkButton(
            self.arh_frame, text=translations[self.current_language]["Back"], command=lambda: self.load_functions_frame()
        )
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
                        self.cnv_frame_r,
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
        self.cnv_frame_r.update()  # Обновляем фрейм, чтобы отобразить метку

        # Создаем и запускаем поток для конвертации
        thread = threading.Thread(target=conversion_thread)
        thread.start()

        return output_file_path


def compress_selected():
    """Archives selected files or folders in a separate thread.

    This function is intended to be called from the context menu integration.
    It retrieves the selected files/folders from the command line arguments and
    archives each of them. Error messages are displayed using CTkMessagebox.
    """

    def archive_thread(items):
        """Function for performing archiving in a separate thread."""
        shell = win32com.client.Dispatch("WScript.Shell")
        selected_items = shell.Selection.Item()
        item = selected_items(0).Path

        if not item:
            root = tk.Tk()
            root.withdraw()
            CTkMessagebox(title="Error", message="No file or folder selected.")
            root.mainloop()
            return

        try:
            compress_file(item)
            root = tk.Tk()
            root.withdraw()
            CTkMessagebox(
                title="Success", message=f"'{item}' successfully archived."
            )
            root.mainloop()

            # Открываем папку с архивом
            folder_path = os.path.dirname(item)
            subprocess.Popen(f'explorer /select,"{folder_path}"')

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
        shell = win32com.client.Dispatch("WScript.Shell")
        selected_items = shell.Selection.Item()
        item = selected_items(0).Path

        if not item:
            root = tk.Tk()
            root.withdraw()
            CTkMessagebox(title="Error", message="No file or folder selected.")
            root.mainloop()
            return

        print(item)
        # Check if the file has a valid archive extension
        if not any(item.lower().endswith(ext) for ext in [".zis", ".zip", ".7zip"]):
            root = tk.Tk()
            root.withdraw()
            CTkMessagebox(
                title="Error", message=f"Unsupported file type: '{item}'"
            )
            root.mainloop()
            return  # Skip to the next file

        try:
            decompress_file(item)
            root = tk.Tk()
            root.withdraw()
            CTkMessagebox(
                title="Success", message=f"'{item}' successfully extracted."
            )
            root.mainloop()

            # Открываем папку с распакованными файлами
            file_path = os.path.splitext(item)[
                0
            ]  # Убираем расширение архива
            subprocess.Popen(f'explorer /select,"{file_path}"')

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

    # Create and start a separate thread for extraction
    thread = threading.Thread(target=extract_thread, args=(sys.argv[1:],))
    thread.start()
    thread.join()  # Wait for the thread to complete

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
    """
    Deletes existing registry entries.

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


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "extract":  # Check for "extract"
        extract_selected()
    elif len(sys.argv) > 1:  # If there are arguments, assume it's for archiving
        compress_selected()
    else:
        app = WinPWindow()
        app.mainloop()