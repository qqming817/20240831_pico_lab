from machine import Pin
import time

led = Pin("LED", Pin.OUT)
status = False

while True:
    if status == False:
        led.on()
        status = True        
    else:
        led.off()
        status = False
    print(status)
    time.sleep_ms(100)