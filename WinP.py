#created by Nazaryan Artem
#Github @sl1de36 | Telegram @slide36

from customtkinter import *
#from func.cnv import *
#from func.tmp import *
#from func.arh import *

class MyApp(CTk):
    def __init__(self):
        super().__init__()
        """
        Initialize the application.

        Instantiate the MyApp class, set the window size to 300x400, and make it non-resizable.
        Also, load the functions frame.
        """

        self.geometry("300x400")
        self.resizable(False, False)
        self.load_functions_frame()

    def function(self, name):
        """
        Handle the click event of a button to execute a specific function.

        When a button is clicked, the name of the button is passed to this function. It creates a new frame,
        executes the function associated with the button name, and displays a 'Back' button to return to the previous frame.
        """

        self.lf_frame.forget()
        self.fn_frame = CTkFrame(self, width=300, height=400)
        self.fn_frame.pack(padx=5, pady=5)
        self.fn_frame.propagate(0)

        fncs = {
            'ARH': lambda: print("ARH"),
            'CNV': lambda: print("CNV"),
            'TMP': lambda: print("TMP")
        }

        if name in fncs:
            fncs[name]()

        bck_button =  CTkButton(self.fn_frame, text="Back", command=lambda: self.load_functions_frame())
        bck_button.pack(padx=5, pady=5, side=BOTTOM)

    def load_functions_frame(self):
        """
        Load the main functions frame.

        If the secondary function frame exists, it is forgotten. Then, a new frame is created with buttons for different functions.
        """

        try: self.fn_frame.forget()
        except: pass

        self.lf_frame = CTkFrame(self, width=300, height=400)
        self.lf_frame.pack(padx=5, pady=5)

        arh_button = CTkButton(self.lf_frame, text="Archivate", command=lambda: self.function("ARH"))
        arh_button.pack(padx=5, pady=5)
        cnv_button = CTkButton(self.lf_frame, text="Converter", command=lambda: self.function("CNV"))
        cnv_button.pack(padx=5, pady=5)
        tmp_button = CTkButton(self.lf_frame, text="Optimizer", command=lambda: self.function("TMP"))
        tmp_button.pack(padx=5, pady=5)

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()