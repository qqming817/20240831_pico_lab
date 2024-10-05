#! usr/bin/micropython

import tools

'''
LED -> GPIO 15
光敏電阻 -> GPIO 28
可變電阻 -> GPIO 26
內建溫度Sensor -> ADC最後1Pin GPIO 28
'''
from machine import Timer, ADC, Pin, PWM, RTC
import binascii
from umqtt.simple import MQTTClient

def do_thing(t):
    '''
    :param t:Timer的實體
    負責偵測溫度和光線
    '''
    
    conversion_factor = 3.3/(65535)
    reading = adc.read_u16() * conversion_factor
    
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
    temperature = 27 - (reading - 0.706)/0.001721
    ligth = adc_light.read_u16()
    #print(datetime_str)
    
    print(f"溫度:{temperature}")
    print(f"光線:{ligth}")

#可變電阻
def do_thing_1(t):
    '''
    :param t:Timer的實體
    負責偵測可變電阻和改變LED的亮度
    '''    
    duty = adc1.read_u16()    
    pwm.duty_u16(duty) #ADC可變電阻電壓輸出給PWM控制LED登亮度
    
    light_lv = round(duty/65535*100)
    print(f"可變電阻: {light_lv}")
    #mqtt.publish('SA-12/亮度', f'{light_lv}')
    mqtt.publish('SA-12/亮度', f'{light_lv}')

def do_reconnect(t):
    tools.reconnect()

def main():
    try:
        tools.connect()
    except RuntimeError as e:
        print(e)
    except Exception:
        print('不明的錯誤')
    else:        
        #使用多個Timer可執行多個工作
        Timer(period=2000, mode=Timer.PERIODIC, callback=do_thing)
        Timer(period=1000, mode=Timer.PERIODIC, callback=do_thing_1)

if __name__ == "__main__":
    #tools.connect() #連線到Wifi
    adc = machine.ADC(4) #內建溫度 
    adc1 = ADC(Pin(26)) #可變電阻
    adc_light = ADC(Pin(28)) #PWM LED
    pwm = PWM(Pin(15), freq=65535) #freq要給
    
    #MQTT
    SERVER = "192.168.0.252"
    CLIENT_ID = binascii.hexlify(machine.unique_id())
    mqtt = MQTTClient(CLIENT_ID, SERVER, user='pi', password='raspberry')
    mqtt.connect()

    main()
