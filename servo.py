from gpiozero import Servo
from time import sleep
import math

servo = Servo(17)
val = -1

x = [0, 20, 40, 80]
#values = [1, 0.56, 0.12, -0.32, -0.76]
values = [0.7, 0.26, -0.18, 0.48, -0.78]
for num in values:
	servo.value = num
	print(num)
	sleep(1)


