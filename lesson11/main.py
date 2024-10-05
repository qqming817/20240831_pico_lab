import tools

from machine import Timer, ADC, Pin, PWM, RTC

#tools.connect() #連線到Wifi
conversion_factor = 3.3/(65535)

adc = machine.ADC(4)
adc_light = ADC(Pin(28))

pwm = PWM(Pin(15), freq=65535) #freq要給

rtc = RTC()

def do_thing(t):
    reading = adc.read_u16() * conversion_factor
    
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
    temperature = 27 - (reading - 0.706)/0.001721
    
    #顯示日期時間(by電腦)
    #year, month, week, day, hours, minutes, seconds, subseconds = rtc.datetime()
    #datetime_str = f"{year}-{month}-{day} {hours}:{minutes}:{seconds} {subseconds}"
    
    ligth = adc_light.read_u16()
    #print(datetime_str)
    
    print(f"溫度:{temperature}")
    print(f"光線:{ligth}")

#可變電阻
def do_thing_1(t):
    adc1 = ADC(Pin(26))
    duty = adc1.read_u16()
    
    pwm.duty_u16(duty) #ADC可變電阻電壓輸出給PWM控制LED登亮度
    print(f"可變電阻: {round(duty/65535*100)}")
    

def do_reconnect(t):
    tools.reconnect()

#使用多個Timer可執行多個工作
Timer(period=2000, mode=Timer.PERIODIC, callback=do_thing)
Timer(period=1000, mode=Timer.PERIODIC, callback=do_thing_1)
#Timer(period=10000, mode=Timer.PERIODIC, callback=do_reconnect)
