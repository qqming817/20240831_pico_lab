import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('A590301', 'A590301AA')

'''
簡易版
'''
#while not wlan.isconnected() and wlan.status() >= 0:
#    print("Waiting to Connet:")
#    time.sleep(1)
    
#print(wlan.ifconfig())

'''
進階版
'''
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

#Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed.')
else:
    print('Connected')
    status = wlan.ifconfig() #回傳陣列
    print('IP = ' + status[0])