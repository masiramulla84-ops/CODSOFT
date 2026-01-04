import tkinter as tk
from tkinter import messagebox

# --- THEME CONSTANTS ---
BG_DARK = "#171717"  # Deep matte black
DISPLAY_BG = "#171717"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#888888"
BTN_NUM = "#333333"  # Dark grey for numbers
BTN_OP = "#ff9500"  # Vibrant orange for operators
BTN_ACTIVE = "#4d4d4d"  # Color when pressed
FONT_MAIN = ("Inter", 36, "bold")
FONT_SUB = ("Inter", 14)


class PolishedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro Calculator")
        self.root.geometry("380x550")
        self.root.configure(bg=BG_DARK)

        self.expression = ""

        # UI Setup
        self._setup_display()
        self._setup_buttons()
        self._setup_keyboard_bindings()

    def _setup_display(self):
        """Creates a layered display for current input and history."""
        self.display_frame = tk.Frame(self.root, bg=BG_DARK, pady=20)
        self.display_frame.pack(fill="both")

        # History label (shows previous part of calculation)
        self.history_var = tk.StringVar(value="")
        self.history_label = tk.Label(self.display_frame, textvariable=self.history_var,
                                      font=FONT_SUB, bg=BG_DARK, fg=TEXT_SECONDARY, anchor="e")
        self.history_label.pack(fill="x", padx=25)

        # Main Input display
        self.display_var = tk.StringVar(value="0")
        self.main_display = tk.Label(self.display_frame, textvariable=self.display_var,
                                     font=FONT_MAIN, bg=BG_DARK, fg=TEXT_PRIMARY, anchor="e")
        self.main_display.pack(fill="x", padx=20)

    def _setup_buttons(self):
        self.btn_container = tk.Frame(self.root, bg=BG_DARK, padx=10, pady=10)
        self.btn_container.pack(expand=True, fill="both")

        layout = [
            ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 2), ('.', 4, 2), ('=', 4, 3)
        ]

        self.buttons = {}
        for item in layout:
            text, row, col = item[0], item[1], item[2]
            colspan = item[3] if len(item) > 3 else 1

            color = BTN_OP if text in ['/', '*', '-', '+', '=', 'C'] else BTN_NUM

            btn = tk.Label(self.btn_container, text=text, font=("Inter", 18),
                           bg=color, fg=TEXT_PRIMARY, width=4, height=2)
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=6, pady=6)

            # Hover and Click Animations
            btn.bind("<Enter>", lambda e, b=btn, c=color: self._on_hover(b, c))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
            btn.bind("<Button-1>", lambda e, t=text: self._handle_click(t))

            self.buttons[text] = btn

        for i in range(4): self.btn_container.grid_columnconfigure(i, weight=1)
        for i in range(5): self.btn_container.grid_rowconfigure(i, weight=1)

    def _setup_keyboard_bindings(self):
        """Maps physical keys to calculator functions."""
        self.root.bind("<Key>", self._handle_keypress)
        self.root.bind("<Return>", lambda e: self._handle_click("="))
        self.root.bind("<BackSpace>", lambda e: self._handle_click("C"))

    def _on_hover(self, btn, base_color):
        # Lighten the color slightly for hover
        btn.config(bg=BTN_ACTIVE)

    def _handle_keypress(self, event):
        char = event.char
        if char in "0123456789+-*/.":
            self._handle_click(char)

    def _handle_click(self, char):
        if char == "C":
            self.expression = ""
            self.history_var.set("")
        elif char == "=":
            try:
                # Sanitize input: replace visual operators with python ones
                result = str(eval(self.expression.replace('×', '*').replace('÷', '/')))
                self.history_var.set(self.expression + " =")
                self.expression = result
            except ZeroDivisionError:
                messagebox.showwarning("Math Error", "Cannot divide by zero")
                self.expression = ""
            except Exception:
                messagebox.showerror("Error", "Invalid Format")
                self.expression = ""
        else:
            if self.expression == "0": self.expression = ""
            self.expression += str(char)

        self.display_var.set(self.expression if self.expression else "0")


if __name__ == "__main__":
    root = tk.Tk()
    app = PolishedCalculator(root)
    root.mainloop()