print("[MAIN] : System Starting...")
import logger
import os
import time
import temp
import mqtt_loader as mqtt
import dissolved_solids as ds
import requests
import RPi.GPIO as GPIO
import glob
import math
import neopixel
import board
MY_NAME = "MAIN"
GPIO.setmode(GPIO.BCM)
ledpin = 27 # assign a variable name to pin 4
pushpin = 22 # assign a variable name to pin 17
GPIO.setup(ledpin, GPIO.OUT) # set GPIO pin 4 as Output
GPIO.setup(pushpin, GPIO.IN) # set GPIO pin 17 as Input
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW) # set the initial output of pin 4 to be LOW
logger.init_logger("main.log") # Start the logger
logger.log_info("MAIN","Logger started!")
mqtt.set_logger(logger) # Set the logger
ds.set_logger(logger)
temp.set_logger(logger)
mqtt.start_mqtt() # start mqtt connection
leds = neopixel.NeoPixel(board.D21, 60)
def update_led(light):
        if(light == "off"):
                leds.fill((0,0,0))
        elif(light == "white"):
                leds.fill((255,255,255))
        elif(light == "green"):
                leds.fill((0,255,0))
        elif(light == "red"):
                leds.fill((255,0,0))
        elif(light == "blue"):
                print("BLUE")
                leds.fill((0,0,255))
        else:
                #print("[MAIN:<update_led>] : Something went wrong...")
                logger.log_err(MY_NAME+"/update_led","Something went wrong...")


try:
    mqtt.subscribe("light",1)
    mqtt.register_callback("light",update_led)
    print("[MAIN] : System Started!")
    while True:

        GPIO.output(ledpin, not GPIO.input(pushpin))
        try:
            temp_c,temp_f = temp.read_temp()
            temp_f = round(temp_f,2)
            mqtt.publish("temp",str(temp_f))
        except:
#            print("[MAIN] : Temp returned invalid value!")
             logger.log_warn(MY_NAME,"Temp returned invalid value!")
        #print(type(temp_f))
        #print(temp_f)
        #requests.get('https://iot:fishtank@smartfish.ddns.net/node/publish/temp/'+str(temp_f)) 
        water = GPIO.input(pushpin) 
        if(water == 0): 
               mqtt.publish("waterlevel","low")
        else:
               mqtt.publish("waterlevel","good")
#       print(GPIO.input(pushpin))
        light = (requests.get('https://iot:fishtank@smartfish.ddns.net/node/poll/light').json())

        time.sleep(10)

finally:
    ds.cleanup()
