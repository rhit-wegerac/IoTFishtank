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
import camera
import sys
GPIO.setwarnings(False)
try:
    print("[MAIN] : Checking user permissions... ")
    open(os.getcwd()+"/secure/needroot","w+").write("")
    os.remove(os.getcwd()+"/secure/needroot")
except Exception as e:
    print(str(e))
    print("You need to have root privileges to run this program.\nPlease try again, this time using 'sudo'. Exiting.")
    sys.exit(1);
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
camera.set_logger(logger)
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
CAMERA_LIMIT=6
camera_counter=6
alive=1
reboot_flag=False
def update_air(air):
        if(air=="True" or air==True):
            logger.log_info(MY_NAME+"/update_air","Setting air to true")
            GPIO.output(airpin,GPIO.HIGH)
        elif(air=="False" or air==True):
            logger.log_info(MY_NAME+"/update_air","Setting air to false")
            GPIO.output(airpin,GPIO.LOW)
        else:
            logger.log_err(MY_NAME+"/update_air","Something went wrong...")
def fix_fill(value):
        for i in range(13,60):
            time.sleep(0.001)
            leds[i]=value
def update_led(light):
        if(light == "off"):
                leds.fill((0,0,0))
        elif(light == "white"):
#                leds[0]=(255,255,255)
#                leds.fill((255,255,255))
                fix_fill((255,255,255))
        elif(light == "green"):
                fix_fill((0,255,0))

        elif(light == "red"):
                fix_fill((255,0,0))
        elif(light == "blue"):
                fix_fill((0,0,255))
        else:
                logger.log_err(MY_NAME+"/update_led","Something went wrong...")

def measure_ds(dummy):
       res=ds.measure()
       mqtt.publish("ds",str(res))
def resetter(dummy):
       global alive
       alive=0;
       mqtt.publish("stat","RES");
def reboot(dummy):
       global alive
       global reboot_flag
       mqtt.publish("stat","REB");
       alive=0
       reboot_flag=True
try:
    mqtt.subscribe("light",1)
    mqtt.register_callback("light",update_led)
    mqtt.subscribe("Air",True)
    mqtt.register_callback("Air",update_air)
    mqtt.subscribe("measure/ds",True)
    mqtt.register_callback("measure/ds",measure_ds)
    mqtt.subscribe("pic/take",True)
    mqtt.register_callback("pic/take",camera.take_pic)
    mqtt.subscribe("reset",True)
    mqtt.subscribe("reboot",True)
    mqtt.register_callback("reset",resetter)
    mqtt.register_callback("reboot",reboot)
    logger.log_special(MY_NAME,"System Started!")
    mqtt.publish("stat","True");

    while alive:
        camera_counter = camera_counter+1
        if(camera_counter>=CAMERA_LIMIT):
                logger.log_info(MY_NAME,"Picture triggered!")
                camera.take_pic(0)
                camera_counter=0
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
        measure_ds(None)
        power_stat = GPIO.input(powerpin)
        
        if(power_stat!=last_stat):
            last_stat=power_stat
            logger.log_info(MY_NAME,"Power status changed")
            if(not power_stat):
                mqtt.publish("power", False)
                logger.log_warn(MY_NAME,"Power has been lost!")
            else:
                logger.log_special(MY_NAME,"Power has been restored!")
                mqtt.publish("power", True)
        
     
        time.sleep(10)
    if(reboot_flag):
       sys.exit(100)
    else:
       sys.exit(99)
finally:
    logger.log_special(MY_NAME,"Received kill signal")
    ds.cleanup()
    mqtt.publish("stat","False");
