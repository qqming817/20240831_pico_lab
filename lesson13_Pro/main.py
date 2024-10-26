#! usr/bin/micropython

import tools, config

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
    temperature = round(27 - (reading - 0.706)/0.001721, 2)
    print(f"溫度:{temperature}")    
    mqtt.publish('SA-12/TEMPERATURE', f'{temperature}')
    blynk_mqtt.publish('ds/temperature', f'{temperature}')

    light_lv = adc_light.read_u16()
    print(f"光線:{light_lv}")
    mqtt.publish('SA-12/LIGHT_LV', f'{light_lv}')
    line_status = 0 if light_lv < 10000 else 1
    print(f"開關:{line_status}")
    mqtt.publish('SA-12/LIGHT_SWITCH', f'{line_status}')
    blynk_mqtt.publish('ds/light_switch', f'{line_status}')
    
    #last_light_lv = light_lv
    
    #if light_lv < last_light_lv * 0.95 or light_lv > last_light_lv * 1.05:
    #    print(f"光線:{light_lv}")
    #    mqtt.publish('SA-12/LIGHT_LV', f'{light_lv}')
        

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
    #mqtt.publish('SA-12/亮度', f'{light_lv}') #中文好像有問題
    mqtt.publish('SA-12/LED_LV', f'{light_lv}')
    blynk_mqtt.publish('ds/led_lv', f'{light_lv}')

def do_reconnect(t):
    tools.reconnect()

#第三階段
def main():
    global blynk_mqtt
    print(config.BLYNK_MQTT_BROKER)
    blynk_mqtt = MQTTClient(config.BLYNK_TEMPLATE_ID, config.BLYNK_MQTT_BROKER, user='device', password=config.BLYNK_AUTH_TOKEN, keepalive=60)
    blynk_mqtt.connect()
    
if __name__ == "__main__":
    #tools.connect() #連線到Wifi
    adc = machine.ADC(4) #內建溫度 
    adc1 = ADC(Pin(26)) #可變電阻
    adc_light = ADC(Pin(28)) #PWM LED
    pwm = PWM(Pin(15), freq=65535) #freq要給
    
    #last_light_lv = 0
    
    #連線到Internet
    try:
        tools.connect()
    except RuntimeError as e:
        print(e)
    except Exception:
        print('不明的錯誤')
    else:
        #MQTT
        SERVER = "192.168.0.252"
        CLIENT_ID = binascii.hexlify(machine.unique_id())
        mqtt = MQTTClient(CLIENT_ID, SERVER, user='pi', password='raspberry')
        mqtt.connect()
    
        #使用多個Timer可執行多個工作
        Timer(period=2000, mode=Timer.PERIODIC, callback=do_thing)
        Timer(period=1000, mode=Timer.PERIODIC, callback=do_thing_1)
    
    blynk_mqtt = None
    main()
