import tkinter as tk

from keyboard_canvas import QWERTYKeyboard
class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Teclado espião Portal")
        self.geometry("1920x1080")

        self.sidebar = tk.Frame(self, width=300, bg="gray")
        self.sidebar.pack_propagate(False)
        self.sidebar.pack(side="left", fill="y")

        self.button_frame = tk.Frame(self.sidebar, bg="gray")
        self.button_frame.pack(side="top", fill="x")

        self.button1 = tk.Button(self.button_frame, text="HOME", bg="gray", fg="black", height=5, command=self.button1_clicked)
        self.button1.pack(fill="x")

        self.button2 = tk.Button(self.button_frame, text="ROTINAS", bg="gray", fg="black", height=5, command=self.button2_clicked)
        self.button2.pack(fill="x")

        self.button3 = tk.Button(self.button_frame, text="LOGS", bg="gray", fg="black", height=5, command=self.button3_clicked)
        self.button3.pack(fill="x")

        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.text_box = tk.Text(self.main_frame, width=100, height=10, bg="white")
        self.text_box.pack(padx=20, pady=20)
        
        self.box = tk.Frame(self.main_frame, bg="white",)
        self.box.pack(padx=20, pady=20)

        self.canvas = QWERTYKeyboard(self, self.main_frame, self.main_frame.winfo_width()/2 + 100, self.main_frame.winfo_height()/2)
        
        self.is_recording = False

        self.record_button = tk.Button(self.main_frame, text="RECORD", bg="gray", fg="black", command=self.record_button)
        self.record_button.pack()
    
    def record_button(self):
        if self.is_recording:
            buffer = self.canvas.stop_recording()
            self.text_box.delete("1.0", "end")
            self.text_box.insert("1.0", " ".join([str(action) for action in buffer]))
            self.record_button.config(text="RECORD")
        else:
            self.canvas.start_recording()
            self.record_button.config(text="STOP")
        self.is_recording = not self.is_recording
    
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
    app.canvas.bind_action_handler(lambda action: print(action))
    app.canvas.start_recording()
    app.mainloop()