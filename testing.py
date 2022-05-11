# import the libraries
import RPi.GPIO as GPIO
from time import sleep
import glob
import time
import requests
import math
import neopixel
import board


GPIO.setmode(GPIO.BCM)
ledpin = 27 # assign a variable name to pin 4
pushpin = 22 # assign a variable name to pin 17
GPIO.setup(ledpin, GPIO.OUT) # set GPIO pin 4 as Output
GPIO.setup(pushpin, GPIO.IN) # set GPIO pin 17 as Input
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW) # set the initial output of pin 4 to be LOW

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

leds = neopixel.NeoPixel(board.D21, 60)


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

print( requests.get('https://iot:fishtank@smartfish.ddns.net/node/poll/light').json())

while True:
	GPIO.output(ledpin, not GPIO.input(pushpin))
	temp_c,temp_f = read_temp()
	temp_f = round(temp_f,2)
	#print(type(temp_f))
	#print(temp_f)
	requests.get('https://iot:fishtank@smartfish.ddns.net/node/publish/temp/'+str(temp_f))
	water = GPIO.input(pushpin)
	if(water == 0):
		requests.get('https://iot:fishtank@smartfish.ddns.net/node/publish/waterlevel/low')
	else:
		requests.get('https://iot:fishtank@smartfish.ddns.net/node/publish/waterlevel/good')
#	print(GPIO.input(pushpin))

	light = (requests.get('https://iot:fishtank@smartfish.ddns.net/node/poll/light').json())
#	print(light["value"])
	if(light["value"] == "off"):
		leds.fill((0,0,0))
	elif(light["value"] == "white"):
		leds.fill((255,255,255))
	elif(light["value"] == "green"):
		leds.fill((0,255,0))
	elif(light["value"] == "red"):
		leds.fill((255,0,0))
	elif(light["value"] == "blue"):
		print("BLUE")
		leds.fill((0,0,255))
	else:
		print("Something went wrong...")
	time.sleep(10)
