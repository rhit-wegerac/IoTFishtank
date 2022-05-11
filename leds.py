import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D21, 60)


#pixels[1] = (0, 0, 255)
#pixels.show()
#pixels.fill((0, 0, 255))
#pixels.fill((0,0,0))
#pixels[0] = (0,0,100)
#pixels.show()
#for i in range(60):
#	pixels[i] = (0, 0, 100)
#	pixels.show()
#	time.sleep(0.5)
pixels.fill((0,0,0))
pixels.show()
