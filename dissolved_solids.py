import os
import time
import RPi.GPIO as gpio
detection=18
pump=20
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(pump,gpio.OUT)
gpio.setup(detection,gpio.IN,pull_up_down=gpio.PUD_DOWN)
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
#CLK  = 18
#MISO = 23
#MOSI = 24
#CS   = 25
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
logger=None
MY_NAME="DS"
def set_logger(l):
	global logger
	logger=l
	l.log_info(MY_NAME,"Logger linked!")
def measure():
	gpio.setmode(gpio.BCM)
	global logger
#	print("[DS] : Filling")
	logger.log_info(MY_NAME,"Filling")
	while (gpio.input(detection)==0):
		gpio.output(pump,gpio.LOW)
	gpio.output(pump,gpio.HIGH)
	out=mcp.read_adc(0)
	logger.log_info(MY_NAME,"Measure: "+str(out))
#	print("[DS] : Measure: "+str(out))
	return out
def cleanup():
	global logger
	gpio.cleanup()
#	print("[DS] : Cleaning up..")
	logger.log_special(MY_NAME,"Cleaning up...")
print("[DS] : Dissolved Solids started")
