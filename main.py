import tkinter as tk

from keyboard_canvas import QWERTYKeyboard
class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Teclado espião Portal")
        self.geometry("1920x1080")

        self.sidebar = tk.Frame(self, width=200, bg="gray")
        self.sidebar.pack(side="left", fill="y")

        self.button_frame = tk.Frame(self.sidebar, bg="gray")
        self.button_frame.pack(side="top", fill="x")

        self.button1 = tk.Button(self.button_frame, text="Button 1", bg="blue", fg="white", command=self.button1_clicked)
        self.button1.pack(fill="x")

        self.button2 = tk.Button(self.button_frame, text="Button 2", bg="blue", fg="white", command=self.button2_clicked)
        self.button2.pack(fill="x")

        self.button3 = tk.Button(self.button_frame, text="Button 3", bg="blue", fg="white", command=self.button3_clicked)
        self.button3.pack(fill="x")

        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.box = tk.Frame(self.main_frame, bg="white",)
        self.box.pack(padx=20, pady=20)

        self.canvas = QWERTYKeyboard(self, self.main_frame, self.main_frame.winfo_width()/2 + 100, self.main_frame.winfo_height()/2)
    def button1_clicked(self):
        print("Button 1 clicked")

    def button2_clicked(self):
        print("Button 2 clicked")

    def button3_clicked(self):
        print("Button 3 clicked")

    def button_clicked(self):
        print("Button clicked")

if __name__ == "__main__":
    app = Application()
    app.mainloop()