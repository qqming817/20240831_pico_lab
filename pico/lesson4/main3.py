from machine import Timer, Pin

green_led = Pin("LED", Pin.OUT)
green_count = 0
def green_led_callback(t:Timer):
    global green_count
    green_count += 1
    green_led.toggle() #如果現在是開啟(亮的)。改成關閉；反之亦然
    print(f"Green_timer被執行{green_count}次")
    if green_count >= 10:
        t.deinit()
        green_led.off()

green_led_timer = Timer(period=1000, mode=Timer.PERIODIC, callback=green_led_callback)

red_led = Pin(15, Pin.OUT) #看接哪個pin角(PGX)
red_count = 0
def red_led_callback(t:Timer):
    global red_count
    red_count += 1
    red_led.toggle() #如果現在是開啟(亮的)。改成關閉；反之亦然
    print(f"Red_timer被執行{red_count}次")
    if red_count >= 10:
        t.deinit()
        red_led.off()

red_led_timer = Timer(period=2000, mode=Timer.PERIODIC, callback=red_led_callback)
