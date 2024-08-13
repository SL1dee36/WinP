from customtkinter import *

class WinPWindow(CTk):
    def __init__(self):
        super().__init__()

        # Инициализация настроек
        self.current_theme = "default"

        # Создание элементов управления
        self.create_theme_menu()

    def create_theme_menu(self):
            self.theme_menu = CTkOptionMenu(self, values=["Default", "Dark", "Light", "Blue", "Green", "Red"], command=self.change_theme)
            self.theme_menu.pack(pady=10)

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