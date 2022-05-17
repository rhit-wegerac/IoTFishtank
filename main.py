#!/usr/bin/python3

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
GPIO.setwarnings(False)
try:
    print("[MAIN] : Checking user permissions... ")
    open(os.getcwd()+"/secure/needroot","w+").write("")
    os.remove(os.getcwd()+"/secure/needroot")
except Exception as e:
    print(str(e))
    exit("You need to have root privileges to run this program.\nPlease try again, this time using 'sudo'. Exiting.")
MY_NAME = "MAIN"
GPIO.setmode(GPIO.BCM)
ledpin = 27 # assign a variable name to pin 4
pushpin = 22 # assign a variable name to pin 17
powerpin = 26 # assign 26 to be powerpin
airpin = 19 # assign 19 to air
# Setup GPIO
GPIO.setup(powerpin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ledpin, GPIO.OUT) # set GPIO pin 4 as Output
GPIO.setup(pushpin, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # set GPIO pin 17 as Input
GPIO.setup(airpin, GPIO.OUT) # set GPIO pin 17 as Input
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW) # set the initial output of pin 4 to be LOW
# Setup logger
logger.init_logger("main.log") # Start the logger
logger.log_info("MAIN","Logger started!")
# pass logger library to sub-modules
mqtt.set_logger(logger) # Set the logger
ds.set_logger(logger)
temp.set_logger(logger)
# Start MQTT
mqtt.start_mqtt() # start mqtt connection
# Start LED
leds = neopixel.NeoPixel(board.D21, 60)

## Define Statuses
power_stat=True;
last_stat = True;
air_stat = True;
last_air = True;
last_level = True;
last_temp = 0;
## 
mqtt.publish("Air","True")
def update_air(air):
        if(air=="True" or air==True):
            logger.log_info(MY_NAME+"/update_air","Setting air to true")
            GPIO.output(airpin,GPIO.HIGH)
        elif(air=="False" or air==True):
            logger.log_info(MY_NAME+"/update_air","Setting air to false")
            GPIO.output(airpin,GPIO.LOW)
        else:
            logger.log_err(MY_NAME+"/update_air","Something went wrong...")
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
                leds.fill((0,0,255))
        else:
                logger.log_err(MY_NAME+"/update_led","Something went wrong...")

def measure_ds(dummy):
       res=ds.measure()
       mqtt.publish("ds",res)
try:
    mqtt.subscribe("light",1)
    mqtt.register_callback("light",update_led)
    mqtt.subscribe("Air",True)
    mqtt.register_callback("Air",update_air)
    mqtt.subscribe("measure/ds",True)
    mqtt.register_callback("measure/ds",measure_ds)
    logger.log_special(MY_NAME,"System Started!")
    while True:

        GPIO.output(ledpin, not GPIO.input(pushpin))
        try:
            temp_c,temp_f = temp.read_temp()
            temp_f = round(temp_f,2)
            if(temp_f != last_temp):
                mqtt.publish("temp",str(temp_f))
                logger.log_info(MY_NAME,"Temperatrue has changed! : "+str(temp_f))
                last_temp=temp_f
        except:
             logger.log_warn(MY_NAME,"Temp returned invalid value!")
        water = GPIO.input(pushpin) 
        if(water!=last_level):
            last_level=water
            logger.log_info(MY_NAME,"Water level has changed")
            if(water == 0): 
                   logger.log_warn(MY_NAME,"Water level is low!")
                   mqtt.publish("waterlevel","low")
            else:
                   logger.log_info(MY_NAME,"Water level is good!")
                   mqtt.publish("waterlevel","good")
                   
        power_stat = GPIO.input(powerpin)
        
        if(power_stat!=last_stat):
            last_stat=power_stat
            logger.log_info(MY_NAME,"Power status changed")
            if(not power_stat):
                mqtt.publish("power", False)
                logger.log_warn(MY_NAME,"Power has been lost!")
            else:
<<<<<<< HEAD
                logger.log_special(MY_NAME,"Power has been restored!")
=======
                logger.log_info(MY_NAME,"Power has been restored!")
                mqtt.publish("power", True)
        
     
>>>>>>> 207aa90d379066155d10c02dddc921fec3653d1c
        time.sleep(10)

finally:
    logger.log_special(MY_NAME,"Received kill signal")
    ds.cleanup()
