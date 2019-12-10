from time import sleep_ms
from _finger import Finger
finger = Finger()

while True:
	sleep_ms(250)
	print(finger.state)
