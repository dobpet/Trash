#from machine import Signal
import sys
#import gc
#import ubinascii
#from AppSettings import *
import uasyncio
#import ustruct
import utime
#from machine import RTC
from mqtt_as import MQTTClient, config
import math
from SHT40 import *


# if sys.implementation._machine == 'Raspberry Pi Pico W with RP2040':
#     import network       # https://docs.micropython.org/en/latest/library/network.WLAN.html#network.WLAN.status
#     STA = None
#     AP = None
#     
#     class PicoNet():
#                      
#         @property
#         def AP_MAC(self):
#             if self.AP.active():
#                 return ubinascii.hexlify(self.AP.config('mac'),':').decode().upper()
#             else:
#                 return "inactive"
#             
#         @property
#         def STA_MAC(self):
#             if self.active():
#                 return ubinascii.hexlify(self.STA.config('mac'),':').decode().upper()
#             else:
#                 return "inactive"
        
        
class MQTT():
    Net = None
    Temperature = None
    Humidity = None
    MQTT = None
    MQTT_task = None
    MQTT_Connected = False
    MQTT_Enable = False
    
    def MQTT_callback(self, topic, msg, retained):
        print(' -> MQTT message received :')
        print('  - topic : {0:s}'.format(topic.decode('utf-8')))
        print('  - msg   : {0:s}'.format(msg.decode('utf-8')))
        print('  - retain: {0}'.format(retained))     
#         if topic == 'SOUT_HW/LED':
#             if msg == 'ON':
#                 a = self.LED_Brightness
#                 self.LED = True
#             else:
#                 a = 0
#                 self.LED = False
#             for i in range(2, self.Board.NeoLEDs.n):
#                 self.Board.NeoLEDs[i] = (a, a, a)
#             self.Board.NeoLEDs.write()
#         elif topic == 'SOUT_HW/LED_Brightness':
#             b = msg.decode('utf-8').strip()
#             l = int(int(b) * 2.55)
#             self.LED_Brightness = l
#             if self.LED:
#                 for i in range(2, self.Board.NeoLEDs.n):
#                     self.Board.NeoLEDs[i] = (l, l, l)
#                 self.Board.NeoLEDs.write()
        
    async def MQTT_connect_callback(self, MQTT):
        print(' -> MQTT connected')
        self.MQTT_Connected = True
        await uasyncio.sleep_ms(0)
        
    async def MQTT_task_async(self):
        while (self.Net.status() < 3) or (self.MQTT_Enable == False):
            await uasyncio.sleep_ms(1000)
        
        await uasyncio.sleep_ms(1500)
        print(" -> MQTT connecting ...                  ")
        await self.MQTT.connect()
        while not self.MQTT.isconnected():
            await uasyncio.sleep_ms(10)
        await uasyncio.sleep_ms(1000)
#         await self.MQTT.subscribe('Inverter/EnableControl', 1)
#         await self.MQTT.subscribe('Inverter/NominalPV', 1)
        Last_Temperature = None
        Last_Humidity = None
      
        while True:  
            if self.MQTT_Connected:
                ( self.Humidity, self.Temperature ) = self.THS.Measure(SHT4X_Meas_HighP_NoHeat)
                bf = self.Temperature
                if Last_Temperature == None or math.fabs(Last_Temperature - bf) > 1: 
                    await self.MQTT.publish('Car/Temperature', '{0:3.2f}'.format(bf), retain = 1, qos=1)
                    Last_Temperature = bf
                    
                bf = self.Humidity
                if Last_Humidity == None or math.fabs(Last_Humidity - bf) > 1: 
                    await self.MQTT.publish('Car/Humidity', '{0:3.2f}'.format(bf), retain = 1, qos=1)
                    Last_Humidity = bf
              
                if (self.Net.status() != 3) or (self.MQTT_Enable == False):
                    print(" -> MQTT close due to network error / dont Enable")
                    self.MQTT.close()
                    self.MQTT_Connected = False
                    Last_Inverter_SOC = None

            else:
                if (self.Net.status() == 3) and (self.MQTT_Enable == True):
                    print(" -> MQTT reconnecting ...")
                    self.MQTT.connect()
                    await uasyncio.sleep_ms(5000)
            
            await uasyncio.sleep_ms(1000)
                    

    def __init__(self, MQTT_Enable, MQTT_Url, MQTT_User, MQTT_Pwd, Net, THS, Temperature, Humidity):
        self.MQTT_Enable = MQTT_Enable
        self.Temperature = Temperature
        self.THS = THS 
        
        self.Humidity = Humidity
        if sys.implementation._machine == 'Raspberry Pi Pico W with RP2040':
            self.Net = Net
            print(" -> Configuring MQTT client ...          ", end='')
            MQTTClient.DEBUG = True
            broker = MQTT_Url
            config['server'] = broker
            config['ssl'] = True
            config['ssl_params'] = {"server_hostname":broker}
            config['user'] = MQTT_User
            config['password'] = MQTT_Pwd
            config['subs_cb'] = self.MQTT_callback
            config['connect_coro'] = self.MQTT_connect_callback
            self.MQTT = MQTTClient(config, self.Net)
            print('done')
            self.MQTT_task = uasyncio.create_task(self.MQTT_task_async())
                
        
        
        
        
    def deinit(self):
        if self.Net != None:
            if self.MQTT_task != None:
                self.MQTT.close()
                self.MQTT_task.cancel()
        self.Board.deinit()
