import influxdb_client
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import secrets

# InfluxDB Cloud connection details
org = "728e39e951451c80"
bucket = "e8f3f6b06d47534f"
token = "aBKAtdFnwGkKWlo9bNuuUfBVX2IQcMeogVh1buDryed9z6vbPcU_MdKQ2k4ZuGxGBR03JV5e7rEV14QDxXjSlw=="
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

# Create an InfluxDB client instance
client = InfluxDBClient(url=url, token=token)

# Create a write API instance
write_api = client.write_api(write_options=SYNCHRONOUS)

# Define the data point to send
data_point = Point("test_measurement").tag("location", "test").field("value", 69420)

# Write the data point to InfluxDB Cloud
write_api.write(bucket=bucket, record=data_point, org=org)

# Close the client connection
client.close()