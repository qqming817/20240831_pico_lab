import time
import binascii
import machine
from umqtt.simple import MQTTClient
from machine import Pin
import tools
import random

# Many ESP8266 boards have active-low "flash" button on GPIO0.
#button = Pin(0, Pin.IN)

def main():
    try:
        tools.connect() #先連wifi
        mqtt = MQTTClient(CLIENT_ID, SERVER, user='pi',password='raspberry')
        mqtt.connect()
        #print("Connected to %s, waiting for button presses" % server)
        
        while True:
            #while True:
                #if button.value() == 0:
                #    break
                #time.sleep_ms(20)
            #print("Button pressed")
            random_temperature = random.random()*100
            #mqtt.publish(TOPIC, b"26.5")
            mqtt.publish(TOPIC, str(random_temperature))
            print(f'Publish Succeed {random_temperature}.')
            time.sleep_ms(2000)
                                
    except:
        mqtt.disconnect()
    
if __name__ == "__main__":    
    # Default MQTT server to connect to
    SERVER = "192.168.0.252"
    CLIENT_ID = binascii.hexlify(machine.unique_id())
    USER = "pi"
    PASSWORD = "raspberry"
    TOPIC = b"SA-12/雞舍/溫度"
    
    main()
