import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
from keyboard_canvas import QWERTYKeyboard

teclas_in = "teclado-espiao/teclas-in"
teclas_out = "teclado_espiao/teclas-out"

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

        self.routines = {"teste": "", "aaa": "", "bbb":"", "cccccc":"", "ddddd":""}
        self.keyboards = {}
         
        self.frames = {}
        self.topic_handlers = {}
        self.create_frames()
        self.show_frame("Home")
        self.start_mqtt()

    def set_topic_handler(self, topic, func):
        self.topic_handlers[topic] = func

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(teclas_in)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        topic = str(msg.topic)
        message = str(msg.payload.decode("utf-8"))
        print(topic + " " + message)
        if topic in self.topic_handlers:
            self.topic_handlers[topic](msg)

    def start_mqtt(self):
        print("starting mqtt...")
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

        self.mqtt_client.connect("test.mosquitto.org", 1883, 60)
        self.step_mqtt()

    def step_mqtt(self):
        self.mqtt_client.loop_read()
        self.mqtt_client.loop_write()
        self.mqtt_client.loop_misc()
        self.after(20, self.step_mqtt)

    def key_listener_factory(self, keyboard, text_box): 
        def listener(msg):
            msg = msg.payload.decode('utf-8')
            print(msg)
            msg = msg.strip("()")
            msg = msg.replace(" ", "")
            msg = msg.replace("'", "")
            action = msg.split(",")
            print(action)
            if action[1] == "PRESSED":
                keyboard.highlight_key(action[0])
                text_box.insert("end", str(action) + " ")
            elif action[1] == "RELEASED":
                keyboard.reset_key(action[0])
                text_box.insert("end", str(action) + " ")
            else:
                print(f"ERROR {action}")
        return listener
    
    def create_home_screen(self):
        main_frame = tk.Frame(self.main_container)
        text_box = tk.Text(main_frame, width=100, height=10, bg="white")
        text_box.pack(padx=20, pady=20)

        self.keyboards["Home"] = QWERTYKeyboard(self, main_frame, main_frame.winfo_width()/2 + 100, main_frame.winfo_height()/2 + 20)
        self.keyboards["Home"].set_mode("listen")

        self.set_topic_handler(teclas_in, self.key_listener_factory(self.keyboards["Home"], text_box))

        return main_frame

    def create_routine_screen(self):
        main_frame = tk.Frame(self.main_container)
        routine_list = tk.Frame(main_frame, name="routine_list", height=200, relief="solid")
        routine_list.pack(fill='x', padx=30, pady=30)
        
        canvas = tk.Canvas(routine_list, height=800)
        scrollbar = ttk.Scrollbar(routine_list, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind the frame to the canvas
        canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Configure grid layout
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        def _on_frame_configure(event=None):
            """Reset the scroll region to encompass the inner frame"""
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas_configure(event):
            """When canvas is resized, resize the inner frame to match"""
            canvas.itemconfig(canvas_frame, width=event.width)

        def _on_mousewheel(event):
            """Handle mouse wheel scrolling"""
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        def build_routine_list():
            for child in scrollable_frame.winfo_children():
                child.destroy()
            for routine in self.routines:
                btn = ttk.Button(scrollable_frame, text=routine)
                btn.pack(pady=2, padx=5, fill="x")
                
        # Building routine list
        build_routine_list()

        # Configure canvas scrolling
        scrollable_frame.bind("<Configure>", _on_frame_configure)
        canvas.bind("<Configure>", _on_canvas_configure)
        
        # Enable mouse wheel scrolling
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        

        def new_routine_screen():
            popup = tk.Toplevel(main_frame, name="newRoutinePopup")
            popup.title("New Routine")
            popup.geometry("1080x800")  # Set the size of the popup window
            
            text_box = tk.Text(popup, name="text_box", width=100, height=10, bg="white")
            text_box.pack(padx=20, pady=20)

            self.keyboards["Routines"] = QWERTYKeyboard(popup, popup, popup.winfo_width()/2 + 100, popup.winfo_height()/2 + 20)
            self.keyboards["Routines"].set_mode("typing", lambda action: None)
            self.keyboards["Routines"].bind_keys()
            
            self.is_recording = False

            record_button = tk.Button(popup, name="record_button", text="RECORD", bg="gray", fg="black", command=self.toggle_record)
            record_button.pack(pady=5)

            # Label for the input
            info_frame = tk.Frame(popup)
            info_frame.pack(padx=125, pady=5, fill="x")

            input_frame = tk.Frame(info_frame)
            input_frame.pack(side="left")

            prompt_label = tk.Label(input_frame, text="Routine name:")
            prompt_label.grid(row=0, column=0, padx=5, pady=10)

            name_entry = tk.Entry(input_frame)
            name_entry.grid(row=0, column=1, padx=5)

            button_frame = tk.Frame(info_frame)
            button_frame.pack(side="right")

            cancel_button = tk.Button(button_frame, text="Cancel", command=popup.destroy)
            cancel_button.grid(row=0, padx=20, column=2, pady=10)

            def save_routine():
                routine_commands = text_box.get("1.0", "end")
                routine_name = name_entry.get()
                self.routines[routine_name] = routine_commands
                build_routine_list()

            save_button = tk.Button(button_frame, text="Save", command=save_routine)
            save_button.grid(row=0, column=3, pady=10)
        # Button to trigger the popup window
        new_routine_button = tk.Button(main_frame, text="NEW", width=8, height=2, command=new_routine_screen)
        new_routine_button.pack(side="right", padx=60)

    
        return main_frame
    
    def toggle_record(self):
        popup = self.frames["Routines"].children["newRoutinePopup"]
        if self.is_recording:
            self.keyboards["Routines"].set_mode("typing", lambda action: None)
            popup.children["record_button"].config(text="RECORD")
        else:
            popup.children["text_box"].delete("1.0", "end")
            self.keyboards["Routines"].set_mode("typing", lambda action: popup.children["text_box"].insert("end", str(action)+" "))
            self.keyboards["Routines"].bind_keys()
            popup.children["record_button"].config(text="STOP")
        self.is_recording = not self.is_recording
    
    def create_frames(self):
        # Home Frame
        self.frames["Home"] = self.create_home_screen()

        # Routines Frame
        self.frames["Routines"] = self.create_routine_screen()

        for frame in self.frames.values():
            frame.place(in_=self.main_container, relwidth=1, relheight=1)

    def show_frame(self, frame_name):
        # Hide all frames
        for frame in self.frames.values():
            frame.place_forget()
        
        # Show the selected frame
        self.frames[frame_name].place(in_=self.main_container, relwidth=1, relheight=1)
        if self.frames[frame_name] != None:
            if frame_name in self.keyboards:
                self.keyboards[frame_name].bind_keys()
    
    def go_to_home(self):
        self.show_frame("Home")

    def go_to_routine(self):
        self.show_frame("Routines")

    def go_to_log(self):
        print("LOG SCREEN IN CONSTRUCTION")

if __name__ == "__main__":
    app = Application()
    app.mainloop()