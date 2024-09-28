from machine import Timer, ADC, Pin

adc = machine.ADC(4)
conversion_factor = 3.3/(65535)

def do_thing(t):
    reading = adc.read_u16() * conversion_factor
    
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
    temperature = 27 - (reading - 0.706)/0.001721
    print(temperature)

#可變電阻
def do_thing_1(t):
    adc1 = ADC(Pin(26))
    duty = adc1.read_u16()
    print(f"可變電阻: {round(duty/65535*100)}")

#使用多個Timer可執行多個工作
Timer(period=2000, mode=Timer.PERIODIC, callback=do_thing)
Timer(period=500, mode=Timer.PERIODIC, callback=do_thing_1)

