import paho.mqtt.client as mqtt
import tkinter as tk
from keyboard_canvas import QWERTYKeyboard
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("house/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic = str(msg.topic)
    message = str(msg.payload.decode("utf-8"))
    print(topic + " " + message)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# With loop_start you have to write the while loop yourself but the programma will continue

def step_mqtt():
    client.loop_read()
    client.loop_write()
    client.loop_misc()

app = tk.Tk()
app.title("Extern keyboard simulator")
app.geometry("1000x500")

main_frame = tk.Frame(app)
main_frame.pack(fill="both", expand=True)
keyboard = QWERTYKeyboard(app, main_frame, 100, 10)
keyboard.set_mode("typing", lambda action: client.publish("teclado-espiao/teclas-in", str(action)))
keyboard.bind_keys()

if __name__ == "__main__":
    app.mainloop()