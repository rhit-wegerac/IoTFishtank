from gpiozero import Servo
from time import sleep

servo = Servo(17)
val = -1

while True:
    #servo.min()
    #sleep(0.5)
    #servo.mid()
    #sleep(0.5)
    #servo.max()
    #sleep(0.5)
#     servo.value = val
#     sleep(0.1)
#     val = val + 0.1
#     if val > 1:
#         val = -1
    servo.min()
    sleep(2)
    servo.max()
    sleep(2)
