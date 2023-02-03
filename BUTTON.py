from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import utime as time
from dht import DHT22
time.sleep(1.5)
 
WIDTH  = 128                                            # oled display width
HEIGHT = 32                                             # oled display height
 
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)       # Init I2C using pins GP8 & GP9 (default I2C0 pins)
 a
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display
sensor = DHT22(Pin(6))
button = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    weight = ("150")
    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, hum))
    
    if  button.value() = 0:
            oled.fill(0)       
            oled.text("Temp: ",0,0)
            oled.text(str(temp*9/5+32),50,0)
            oled.text("F",90,0)
            
            oled.text("Hum: ",0,10)
            oled.text(str(hum),50,10)
            oled.text("%",90,10)
            
            oled.text("LB: ",0,20)
            oled.text(str(weight),50,20)
            
            time.sleep(30)
        
    else:
        oled.fill(0)
