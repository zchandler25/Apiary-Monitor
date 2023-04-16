import socket
import ujson as json
from datetime import datetime
from tkinter import *
import tkinter as tk

# Server settings
SERVER_PORT = 1234

# Get local IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
SERVER_IP = s.getsockname()[0]
print("IP Adderess is: ",SERVER_IP)
s.close()

# Dictionaries to store data
temp_dict = {}
hum_dict = {}
weight_dict = {}

# Start server socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_IP, SERVER_PORT))
s.listen(1)
print("Server listening on {}:{}".format(SERVER_IP, SERVER_PORT))

# Listen for incoming data and store it in the dictionaries
def receive_data():
    conn, addr = s.accept()
    data = conn.recv(1024)
    if data:
        try:
            data_dict = json.loads(data.decode())
            temp_dict[str(datetime.now())] = data_dict["temperature"]
            hum_dict[str(datetime.now())] = data_dict["humidity"]
            weight_dict[str(datetime.now())] = data_dict["weight"]
            print("Data received - Temperature: {}, Humidity: {}, Weight: {}".format(temp_dict, hum_dict, weight_dict))
            update_gui()
        except json.JSONDecodeError:
            print("Error: Invalid data format received")

# Update GUI with latest temperature, humidity, and weight readings
def update_gui():
    if temp_dict and hum_dict and weight_dict:
        latest_temp = temp_dict[max(temp_dict)]
        latest_hum = hum_dict[max(hum_dict)]
        latest_weight = weight_dict[max(weight_dict)]
        temp_label.config(text="Temperature: {} °C".format(latest_temp))
        hum_label.config(text="Humidity: {:.0f}%".format(latest_hum))
        weight_label.config(text="Weight: {:.2f} kg".format(latest_weight))

# Create Tkinter GUI
root = tk.Tk()
root.title("BeeHive Monitoring")
root.geometry("1200x1200")

# Set window position to center of screen
root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())

# Add background image
bg_image = PhotoImage(file="honeycomb.jpg")

# Create a label with the image
bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set font size for labels
font_size = 30

temp_label = tk.Label(root, text="Temperature: N/A", font=("Helvetica", font_size), anchor="center")
temp_label.place(relx=0.5, rely=0.3, anchor="center")

hum_label = tk.Label(root, text="Humidity: N/A", font=("Helvetica", font_size), anchor="center")
hum_label.place(relx=0.5, rely=0.5, anchor="center")

weight_label = tk.Label(root, text="Weight: N/A", font=("Helvetica", font_size), anchor="center")
weight_label.place(relx=0.5, rely=0.7, anchor="center")

# Start receiving data

root.after(1000, receive_data)

root.mainloop()