import machine
import network
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from dht import DHT22
import socket
import ujson as json
import utime as time
import logging

# Constants
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"
SERVER_IP = "your_server_ip"
SERVER_PORT = 1234
WAIT_TIME = 3  # Wait for 3 seconds before reading the sensor again

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize display
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
oled = SSD1306_I2C(128, 32, i2c)

# Initialize sensor and LED
sensor = DHT22(Pin(6))
led = machine.Pin('LED', machine.Pin.OUT)

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    logging.info('Connected to Wi-Fi: %s', wlan.ifconfig())

# Send data to server via socket
def send_data(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((SERVER_IP, SERVER_PORT))
        s.sendall(json.dumps(data))
        logging.info('Data sent to server: %s', data)
    except Exception as e:
        logging.error('Error sending data to server: %s', e)
    finally:
        s.close()

# Read sensor values and update display
def read_sensor():
    try:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)
    
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        weight = "170"
        logging.info("Temperature: %s°C   Humidity: %s%% ", temp, hum)
        
        # Display temperature, humidity, and weight values on separate lines
        oled.text("Temp: {:.1f}°C ".format(temp), 0, 0)
        oled.text("Hum: {:.0f}%".format(hum), 0, 10)
        oled.text("LB: {}".format(weight), 0, 20)
        oled.show()

        # Send data to server via socket
        data = {"temperature": temp, "humidity": hum, "weight": weight}
        send_data(data)

    except Exception as e:
        logging.error('Error reading sensor data: %s', e)

# Main loop
def main():
    connect_wifi()
    while True:
        read_sensor()
        time.sleep(WAIT_TIME)

if __name__ == '__main__':
    main()