import socket
import time
from machine import Pin
from dht import DHT22
import network
import secrets

# WiFi network details
SSID = secrets.secrets['ssid']
PASSWORD = secrets.secrets['password']

# InfluxDB Cloud settings
INFLUXDB_URL = 'https://us-east-1-1.aws.cloud2.influxdata.com'
INFLUXDB_TOKEN = 'aBKAtdFnwGkKWlo9bNuuUfBVX2IQcMeogVh1buDryed9z6vbPcU_MdKQ2k4ZuGxGBR03JV5e7rEV14QDxXjSlw=='
INFLUXDB_ORG = '728e39e951451c80'
INFLUXDB_BUCKET = 'e8f3f6b06d47534f'

# Connect to WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

# Wait until connected
while not wifi.isconnected():
    pass

# Connect to the DHT22 sensor
dht22 = DHT22(Pin(6))

# Initialize dictionaries to store the last 5 readings of temperature and humidity
temperature_dict = {}
humidity_dict = {}

while True:
    try:
        # Read the temperature and humidity from the DHT22 sensor
        dht22.measure()
        temperature = dht22.temperature()
        humidity = dht22.humidity()

        # Get the current time in Unix timestamp format
        timestamp = int(time.time())

        # Construct the data payload in InfluxDB Line Protocol format with timestamp
        data = 'temperature,location=office value={} {}'.format(temperature, timestamp) + '\n'
        data += 'humidity,location=office value={} {}'.format(humidity, timestamp) + '\n'

        # Print the data payload for debugging purposes
        print('Data payload: {}'.format(data))

        # Send the data to InfluxDB Cloud using the POST method and sockets
        headers = {
            'Authorization': 'Token {}'.format(INFLUXDB_TOKEN),
            'Content-Type': 'application/octet-stream',
            'User-Agent': 'micropython-sockets'
        }
        url = '/api/v2/write?org={}&bucket={}&precision=s'.format(INFLUXDB_ORG, INFLUXDB_BUCKET)
        message = 'POST {} HTTP/1.1\r\nHost: {}\r\n{}\r\n{}'.format(url, INFLUXDB_URL[8:], headers, data)
        s = socket.socket()
        s.connect(socket.getaddrinfo(INFLUXDB_URL[8:], 443)[0][-1])
        s = ssl.wrap_socket(s)
        s.write(message)
        response = s.read(1024)
        s.close()

        # Print the response code and text for debugging purposes
        print('Response code: {}'.format(response.decode().split()[1]))
        print('Response text: {}'.format(response.decode().split('\r\n\r\n')[1]))

        # Store the latest reading of temperature and humidity in their respective dictionaries
        temperature_dict[timestamp] = temperature
        humidity_dict[timestamp] = humidity

        # Remove the oldest reading from the dictionaries if there are more than 5 readings
        if len(temperature_dict) > 5:
            oldest_timestamp = min(temperature_dict.keys())
            del temperature_dict[oldest_timestamp]
        if len(humidity_dict) > 5:
            oldest_timestamp = min(humidity_dict.keys())
           
