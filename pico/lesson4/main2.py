from machine import Timer

#tim = Timer(period=1000, mode=Timer.ONE_SHOT, callback=lambda t:print(1))
#tim.init(period=5000, mode=Timer.PERIODIC, callback=lambda t:print(1))

count = 0
def mycallback(t:Timer):
    global count
    count = count + 1
    print(f"目前mycallback被執行: {count}次")
    if count >= 10:
        t.deinit()

local_timer = Timer(period=1000, mode=Timer.PERIODIC, callback=mycallback)