# displays values as either a graph or text values
# uses a function to grab "value"

import tkinter as tk

S
# Create a new window object
window = tk.Tk()

# Set the window title
window.title("Temperature and Humidity")

# Set the window size
window.geometry("300x200")

# Create labels for the temperature and humidity
temp_label = tk.Label(window, text="Temp: 75C", font=("Arial", 30))
temp_label.pack(pady=10)

humidity_label = tk.Label(window, text="Humidity: 70%", font=("Arial", 30))
humidity_label.pack(pady=10)

# Update the temperature and humidity values (you can replace these values with your actual readings)
temp_label.config(text="Temp:", grabvalue(temp_dict.py))
humidity_label.config(text="Humidity:", grabvalue(temp_dict.py))

# Run the main event loop
window.mainloop()