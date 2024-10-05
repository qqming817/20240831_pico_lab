import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('A590301', 'A590301AA')

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to Connet:")
    time.sleep(1)
    
print(wlan.ifconfig())