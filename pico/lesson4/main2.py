from machine import Timer

tim = Timer(period=1000, mode=Timer.ONE_SHOT, callback=lambda t:print(1))
tim.init(period=5000, mode=Timer.PERIODIC, callback=lambda t:print(1))