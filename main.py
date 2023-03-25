from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import utime as time
from dht import DHT22
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import network
import secrets

## WiFi network details
SSID = secrets.secrets['ssid']
PASSWORD = secrets.secrets['password']

# InfluxDB Cloud account details
bucket = secrets.secrets['bucket']
org = secrets.secrets['org']
token = secrets.secrets['token']
url = secrets.secrets['url']

# Connect to WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

# Wait until connected
while not wifi.isconnected():
    pass


# Initialize InfluxDB client
client = InfluxDBClient(url=url, token=token)

# Display
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
WIDTH = 128
HEIGHT = 32

# Sensor
sensor = DHT22(Pin(6))

# LED
led = machine.Pin('LED', machine.Pin.OUT)

# Main loop
while True:
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)
    
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    weight = ("150")
    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, hum))

    # Write sensor data to InfluxDB Cloud
    write_api = client.write_api(write_options=SYNCHRONOUS)
    point = Point("my-measurement").tag("location", "my-location").field("temperature", temp).field("humidity", hum)
    write_api.write(bucket=bucket, org=org, record=point)
    
    # Clear the OLED display and add text
    oled.fill(0)       
    oled.text("Temp: ",0,0)
    oled.text(str(temp),50,0)
    oled.text("C",90,0)
    oled.text("Hum: ",0,10)
    oled.text(str(hum),50,10)
    oled.text("%",90,10)
    oled.text("LB: ",0,20)
    oled.text(str(weight),50,20)
    
    time.sleep(1)
    oled.show()
