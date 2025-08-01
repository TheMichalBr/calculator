import math
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from tkinter import PhotoImage
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Frame, Entry, Button, Label
import ctypes as ct

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.master.geometry("400x520")
        self.master.minsize(350, 500)
        self.master.resizable(False, False)
        self.set_dark_title_bar()

        try:
            self.master.iconbitmap("calculator.ico")
        except:
            pass    # Launch without icon.

        self.expression = ""
        self.equation = tk.StringVar()

        self.style = ttk.Style()
        self.style.configure("Calc.TButton", font=("Segoe UI", 20, "bold"), padding=10, borderwidth=1, relief="flat")

        self.display_frame = ttk.Frame(self.master, padding=(10, 10, 10, 0))
        self.display_frame.pack(fill=X)

        self.display = ttk.Entry(
            self.display_frame,
            textvariable=self.equation,
            font=('Segoe UI', 32, 'bold'),
            justify='right',
            state='readonly',
            foreground='white',
            background='black',
        )
        self.display.pack(fill=X, expand=True, ipady=10)

        self.button_frame = ttk.Frame(self.master, padding=10)
        self.button_frame.pack(fill=BOTH, expand=True)

        buttons = [
            ('C', 1, 0, 'danger'), ('(', 1, 1, 'info'), (')', 1, 2, 'info'), ('/', 1, 3, 'info'),
            ('7', 2, 0, 'secondary'), ('8', 2, 1, 'secondary'), ('9', 2, 2, 'secondary'), ('*', 2, 3, 'info'),
            ('4', 3, 0, 'secondary'), ('5', 3, 1, 'secondary'), ('6', 3, 2, 'secondary'), ('-', 3, 3, 'info'),
            ('1', 4, 0, 'secondary'), ('2', 4, 1, 'secondary'), ('3', 4, 2, 'secondary'), ('+', 4, 3, 'info'),
            ('0', 5, 0, 'secondary', 2), ('.', 5, 2, 'secondary'), ('=', 5, 3, 'success')
        ]

        for (text, row, col, style, *args) in buttons:
            colspan = args[0] if args else 1
            btn = ttk.Button(
                self.button_frame,
                text=text,
                style="Calc.TButton",
                bootstyle="info rounded",
                command=lambda t=text: self.on_button_press(t)
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

        for i in range(6):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)

        self.master.bind("<Key>", self.key_input)

    def on_button_press(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '=':
            try:
                expression_safe = self.expression.replace(',', '.')
                result = str(eval(expression_safe))
                self.expression = result
                self.display.configure(foreground="green")
            except Exception:
                self.expression = ""
                self.equation.set("Error")
                self.display.configure(foreground="red")
                return
        else:
            if self.equation.get() == "Error":
                self.expression = ""
                self.display.configure(foreground="black")
            if char == '.' and self.expression and self.expression[-1] == '.':
                return
            self.expression += str(char)
            self.display.configure(foreground="black")

        self.equation.set(self.expression.replace('.', ','))

    def key_input(self, event):
        key = event.char
        if key in '0123456789+-*/.()':
            self.on_button_press(key)
        elif key in ('\r', '='):
            self.on_button_press('=')
        elif key.lower() == 'c':
            self.on_button_press('C')

    def set_dark_title_bar(self):
        try:
            self.master.update()
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ct.windll.user32.GetParent
            hwnd = get_parent(self.master.winfo_id())
            value = ct.c_int(1)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ct.byref(value), ct.sizeof(value))
        except Exception:
            pass

if __name__ == "__main__":
    app = ttk.Window(themename="darkly")
    CalculatorApp(app)
    app.mainloop()