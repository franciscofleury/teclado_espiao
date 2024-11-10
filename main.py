import tkinter as tk
import paho.mqtt.client as mqtt
import ast
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

        keyboard = QWERTYKeyboard(self, main_frame, main_frame.winfo_width()/2 + 100, main_frame.winfo_height()/2 + 20)
        keyboard.set_mode("listen")

        self.set_topic_handler(teclas_in, self.key_listener_factory(keyboard, text_box))

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