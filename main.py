import machine
import network
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from dht import DHT22
import socket
import ujson as json
import utime as time

# Constants
WIFI_SSID = "IP a Lot 2G"
WIFI_PASSWORD = "A!!edegly21"
SERVER_IP = "192.168.0.170"
SERVER_PORT = 1234
WAIT_TIME = 3  # Wait for 3 seconds before reading the sensor again

# Initialize display
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
oled = SSD1306_I2C(128, 32, i2c)

# Initialize sensor and LED
sensor = DHT22(Pin(6))
led = machine.Pin('LED', machine.Pin.OUT)

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to Wi-Fi...')
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
        print('.', end='')
        if time.ticks_ms() > 15000:
            print('\nFailed to connect to Wi-Fi')
            break
if wlan.isconnected():
    print('Connected to Wi-Fi:', wlan.ifconfig()[0])

# Main loop
while True:
    try:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)

        # Read sensor values
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        weight = "170"
        print("Temperature: {:.1f}°C   Humidity: {:.0f}%".format(temp, hum))

        # Display temperature, humidity, and weight values on separate lines
        oled.text("Temp: {:.1f}°C ".format(temp), 0, 0)
        oled.text("Hum: {:.0f}%".format(hum), 0, 10)
        oled.text("LB: {}".format(weight), 0, 20)
        oled.show()

        # Send data to server via socket
        data = {"temperature": temp, "humidity": hum, "weight": weight}
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((SERVER_IP, SERVER_PORT))
            print('JSON data:', json.dumps(data))
            s.sendall(json.dumps(data))
            print('Data sent to server:', data)
        except Exception as e:
            print('Error sending data to server:', e)
        finally:
            s.close()

    except Exception as e:
        print('Error reading sensor data:', e)

    time.sleep(WAIT_TIME)
