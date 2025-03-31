import network
import json
from hadware.leds import led
from utime import sleep

class myNetwork:
    def __init__(self):
        # Opening JSON file
        f = open('utils/mynetwork/networks.json')

        self.jsondata = json.load(f)

        # Closing file
        f.close()
        
        self.nets = self.jsondata["networks"]
        
        loadedNets = []
        
        for n in self.nets:
            loadedNets.append(n['ssid'])

        print("networks loaded ",loadedNets)

        self.sta_if = network.WLAN(network.STA_IF) # wifi station mode
        self.sta_if.active(True) # wifi on
        
        self.myled = led()


    def connectOrReconect(self):
        while not self.sta_if.isconnected(): # or not self.sconected:
            for n in self.nets:
                self.myled.turnOn()
                try:
                    print("connecting to ",n["ssid"])
                    self.sta_if.connect(n["ssid"],n["pass"])
                    sleep(5)
                    if self.sta_if.isconnected():
                        print("connected to ",n["ssid"])
                        self.myled.flash(0.1)
                        return # exit function
                except Exception as e:
                    self.myled.turnOff()
                    print('Exception ',e)
                    self.sta_if.active(False) # wifi off
                    sleep(1)
                    self.sta_if.active(True) # wifi on
                    pass
        print("connected to ",self.sta_if.config('essid'))
        self.myled.flash(0.1)

    def closeSocket(self):
        self.s.close()

    def sendMessage(self,message:str):
        self.s.send(bytes(message))

    def reciveMessage(self):
        return self.s.recv(1000)