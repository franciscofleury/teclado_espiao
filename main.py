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

        self.home_button = tk.Button(self.button_frame, text="HOME", bg="gray", fg="black", height=5, command=self.go_to_home)
        self.home_button.pack(fill="x")

        self.routine_button = tk.Button(self.button_frame, text="ROTINAS", bg="gray", fg="black", height=5, command=self.go_to_routine)
        self.routine_button.pack(fill="x")

        self.log_button = tk.Button(self.button_frame, text="LOGS", bg="gray", fg="black", height=5, command=self.go_to_log)
        self.log_button.pack(fill="x")

        # Create main frame to stack content frames
        self.main_container = tk.Frame(self)
        self.main_container.pack(side="right", fill="both", expand=True)

        self.frames = {}
        self.create_frames()
        self.show_frame("Home")

    def create_home_screen(self):
        main_frame = tk.Frame(self.main_container)
        text_box = tk.Text(main_frame, width=100, height=10, bg="white")
        text_box.pack(padx=20, pady=20)

        keyboard = QWERTYKeyboard(self, main_frame, main_frame.winfo_width()/2 + 100, main_frame.winfo_height()/2 + 20)
        keyboard.set_mode("typing", lambda action: print(action))

        return (main_frame, keyboard)
    
    def create_routine_screen(self):
        main_frame = tk.Frame(self.main_container)
        text_box = tk.Text(main_frame, name="text_box", width=100, height=10, bg="white")
        text_box.pack(padx=20, pady=20)

        keyboard = QWERTYKeyboard(self, main_frame, main_frame.winfo_width()/2 + 100, main_frame.winfo_height()/2 + 20)
        keyboard.set_mode("typing", lambda action: None)
        
        self.is_recording = False

        record_button = tk.Button(main_frame, name="record_button", text="RECORD", bg="gray", fg="black", command=self.toggle_record)
        record_button.pack()
    
        return (main_frame, keyboard)
    
    def toggle_record(self):
        if self.is_recording:
            self.frames["Routines"][0].children["text_box"].delete("1.0", "end")
            self.frames["Routines"][1].set_mode("typing", lambda action: None)
            self.frames["Routines"][0].children["record_button"].config(text="RECORD")
        else:
            print(self.frames["Routines"][0].children)
            self.frames["Routines"][1].set_mode("typing", lambda action: self.frames["Routines"][0].children["text_box"].insert("end", str(action)+" "))
            self.frames["Routines"][0].children["record_button"].config(text="STOP")
        self.is_recording = not self.is_recording

    def create_frames(self):
        # Home Frame
        self.frames["Home"] = self.create_home_screen()

        # Routines Frame
        self.frames["Routines"] = self.create_routine_screen()

        for frame in self.frames.values():
            frame[0].place(in_=self.main_container, relwidth=1, relheight=1)

    def show_frame(self, frame_name):
        # Hide all frames
        for frame in self.frames.values():
            frame[0].place_forget()
        
        # Show the selected frame
        self.frames[frame_name][0].place(in_=self.main_container, relwidth=1, relheight=1)
        if self.frames[frame_name][1] != None:
            self.frames[frame_name][1].bind_keys()
    
    def go_to_home(self):
        self.show_frame("Home")

    def go_to_routine(self):
        self.show_frame("Routines")

    def go_to_log(self):
        print("LOG SCREEN IN CONSTRUCTION")

if __name__ == "__main__":
    app = Application()
    app.mainloop()