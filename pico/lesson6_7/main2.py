from machine import Timer, ADC

adc = machine.ADC(4)
conversion_factor = 3.3/(65535)

def do_thing(t):
    reading = adc.read_u16() * conversion_factor
    
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
    temperature = 27 - (reading - 0.706)/0.001721
    print(temperature)

Timer(period=2000, mode=Timer.PERIODIC, callback=do_thing)

