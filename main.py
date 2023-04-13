import time
from machine import Pin, I2C
from dht import DHT22
import network
import secrets
import ssd1306
import socket

## WiFi network details
SSID = secrets.secrets['ssid']
PASSWORD = secrets.secrets['password']

# Connect to WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

# Wait until connected
while not wifi.isconnected():
    pass

# Define your InfluxDB Cloud settings
INFLUXDB_URL = 'us-east-1-1.aws.cloud2.influxdata.com'
INFLUXDB_TOKEN = 'aBKAtdFnwGkKWlo9bNuuUfBVX2IQcMeogVh1buDryed9z6vbPcU_MdKQ2k4ZuGxGBR03JV5e7rEV14QDxXjSlw=='
INFLUXDB_ORG = '728e39e951451c80'
INFLUXDB_BUCKET = 'e8f3f6b06d47534f'

# Connect to the DHT11 sensor
d = DHT22(Pin(6))

# Define the OLED screen settings
WIDTH = 128
HEIGHT = 32
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Initialize the timestamp and readings dictionaries
timestamps_temp = {}
timestamps_humid = {}
readings_temp = {}
readings_humid = {}

while True:
    try:
        # Read the temperature and humidity from the DHT11 sensor
        d.measure()
        temperature = d.temperature()
        humidity = d.humidity()

        # Get the current time in Unix timestamp format
        timestamp = int(time.time())

        # Add the temperature and humidity readings to the timestamped readings dictionaries
        timestamps_temp[timestamp] = temperature
        timestamps_humid[timestamp] = humidity

        # Keep only the last 5 readings in each dictionary
        if len(timestamps_temp) > 5:
            oldest_temp = min(timestamps_temp.keys())
            del timestamps_temp[oldest_temp]
        if len(timestamps_humid) > 5:
            oldest_humid = min(timestamps_humid.keys())
            del timestamps_humid[oldest_humid]

        # Construct the data payload in InfluxDB Line Protocol format with timestamp
        data = 'temperature,location=office value={} {}'.format(temperature, timestamp) + '\n'
        data += 'humidity,location=office value={} {}'.format(humidity, timestamp) + '\n'

        # Print the data payload for debugging purposes
        print('Data payload: {}'.format(data))

        # Send the data to InfluxDB Cloud using the POST method and sockets
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((INFLUXDB_URL, 443))
        s = ssl.wrap_socket(s, server_hostname=INFLUXDB_URL)
        headers = {
            'Authorization': 'Token {}'.format(INFLUXDB_TOKEN),
            'Content-Type': 'application/octet-stream',
            'User-Agent': 'micropython-sockets'
        }
        url = '/api/v2/write?org={}&bucket={}&precision=s'.format(INFLUXDB_ORG, INFLUXDB_BUCKET)
        request = 'POST {} HTTP/1.1\r\nHost

        
