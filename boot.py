import network
from uasyncio import sleep, get_event_loop
from machine import SoftI2C,Pin

from lcd.I2C_LCD import I2cLcd
from animations.ariplaneframes import airplane_frames, runway_frames

DEFAULT_I2C_ADDR = 0x27
i2c = SoftI2C(scl=Pin(14), sda=Pin(13), freq=400000)
screen = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

led = Pin(2,Pin.OUT) # onboard led
led.value(0)

def flash(speed):
    """as flash contains sleep , must be awaited"""
    led.value(1)
    sleep(speed)
    led.value(0)
    sleep(speed)

async def apiManager(api_url,data):
    while True:
        try:
            print("Connecting to API...")
            # Simulate API connection and data retrieval
            await sleep(2)  # Simulate network delay
            
            print("Connected to API")
            # Simulate data retrieval
            data['temperature'] = 25.0  # Example data
            
            await sleep(0.1)
        except Exception as e:
            print("Error connecting to API:", e)

async def screenManager(data):
    print("Initializing screen...")
    screen.clear()
    screen.move_to(0, 0)
    screen.putstr("Initializing...")

    # Load custom characters into CGRAM
    for i, frame in enumerate(airplane_frames):
        screen.custom_char(i, frame)
    for i, frame in enumerate(runway_frames):
        screen.custom_char(i + len(airplane_frames), frame)
        print("Custom character loaded:", i + len(airplane_frames))
    
    print("Screen initialized")
    await sleep(1)

    while True:
        try:
            screen.clear()
            screen.move_to(0, 0)
            screen.putstr("Temperature:")
            screen.move_to(0, 1)
            screen.putstr("Waiting for data")

            await flash(0.5)

            # Display airplane animation
            screen.clear()
            
            # add runway
            for i in range(0,15):
                screen.move_to(i,1)
                if i % 2 == 0:
                    c = len(airplane_frames)
                else:
                    c = len(airplane_frames)+1
                screen.putchar(chr(c))  # Display the current frame

            for i in range(len(airplane_frames)):
                screen.move_to(0, 0)
                screen.putchar(chr(i))  # Display the current frame
                await sleep(0.5)  # Delay between frames

            await sleep(1)

            if data:
                screen.clear()
                screen.move_to(0, 0)
                screen.putstr("Temperature:")
                screen.move_to(0, 1)
                screen.putstr(str(data['temperature']) + " C")
                flash(0.5)
                                
            await sleep(0.5) # Update every 0.5 seconds
        except Exception as e:
            print("Error updating screen:", e)

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
        loop = get_event_loop()
        loop.create_task(apiManager(api_url,data))
        loop.create_task(screenManager(data))
        loop.run_forever()

    except Exception as e:
        print('Exception ',e)
        loop.stop()
        loop.close()

if __name__ == "__main__":
    main()
        