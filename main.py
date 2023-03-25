import urequests
import time
from machine import Pin, I2C
from dht import DHT22
import network
import secrets

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
INFLUXDB_URL = 'https://us-east-1-1.aws.cloud2.influxdata.com'
INFLUXDB_TOKEN = 'aBKAtdFnwGkKWlo9bNuuUfBVX2IQcMeogVh1buDryed9z6vbPcU_MdKQ2k4ZuGxGBR03JV5e7rEV14QDxXjSlw=='
INFLUXDB_ORG = '728e39e951451c80'
INFLUXDB_BUCKET = 'e8f3f6b06d47534f'

# Connect to the DHT11 sensor
d = DHT22(Pin(6))

while True:
    try:
        # Read the temperature and humidity from the DHT11 sensor
        d.measure()
        temperature = d.temperature()
        humidity = d.humidity()

        # Get the current time in Unix timestamp format
        timestamp = int(time.time())

        # Construct the data payload in InfluxDB Line Protocol format with timestamp
        data = 'temperature,location=office value={} {}'.format(temperature, timestamp) + '\n'
        data += 'humidity,location=office value={} {}'.format(humidity, timestamp) + '\n'

        # Print the data payload for debugging purposes
        print('Data payload: {}'.format(data))

        # Send the data to InfluxDB Cloud using the POST method and the urequests library
        headers = {
            'Authorization': 'Token {}'.format(INFLUXDB_TOKEN),
            'Content-Type': 'application/octet-stream',
            'User-Agent': 'micropython-urequests'
        }
        url = '{}/api/v2/write?org={}&bucket={}&precision=s'.format(INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_BUCKET)
        response = urequests.post(url, headers=headers, data=data)

        # Print the response code and text for debugging purposes
        print('Response code: {}'.format(response.status_code))
        print('Response text: {}'.format(response.text))

        # Sleep for 10 seconds before reading the sensor again
        time.sleep(10)

    except Exception as e:
        print('Error reading sensor: {}'.format(e))