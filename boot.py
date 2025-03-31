import network
import uasyncio

from machine import Pin
from utime import sleep

led=Pin(2,Pin.OUT) # onboard led
led.value(0)

def flash(speed):
    led.value(1)
    uasyncio.sleep(speed)
    led.value(0)
    uasyncio.sleep(speed)

async def apiManager(api_url,data):
    
    await uasyncio.sleep(0.01)

async def screenManager(data):
                        
    await uasyncio.sleep(0.01)

def main():
    # A WLAN interface must be active to send()/recv()
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.disconnect() 

    # api url
    api_url = "https://api.example.com/data" # replace with your API URL

    #object for store data 
    data = {}

    try:
        loop = uasyncio.get_event_loop()
        loop.create_task(apiManager(api_url,data))
        loop.create_task(screenManager(data))
        loop.run_forever()

    except Exception as e:
        print('Exception ',e)
        loop.stop()
        loop.close()

if __name__ == "__main__":
    main()
        