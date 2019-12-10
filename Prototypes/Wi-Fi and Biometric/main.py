# DELIGHT BIOMETRIC UPY
# RAGULBALAJI 2019

from m5stack import lcd
from time import sleep_ms
from machine import Pin, PWM

TONE_DELIGHT = [(1174, 250), (1479, 250), (1760, 250), (2349, 500)]
TONE_DENY = [(1760, 100), (1, 50), (1760, 400)]

def clrscrn():
	lcd.setRotation(1)
	lcd.clear()
	lcd.font(lcd.FONT_DejaVu24)
	lcd.setTextColor(lcd.WHITE)
	lcd.setCursor(0,0)


spkr = PWM(Pin(26), freq = 1)
spkr.duty(50)
def note(freq, ms, duty=50):
	spkr.duty(duty)
	spkr.freq(freq)
	sleep_ms(ms)

def tone(tonearr):
	for n in tonearr:
		note(n[0],n[1])
	spkr.freq(1) # almost silent!


clrscrn()
lcd.setTextColor(lcd.RED)
lcd.print("deLIGHTer\nv2.3-fut2d\n")
sleep_ms(100)
tone(TONE_DELIGHT)
sleep_ms(500)

def mainScrn():
	clrscrn()
	lcd.setTextColor(lcd.RED)
	lcd.print("deLIGHTer\n")
	lcd.setTextColor(lcd.WHITE)
	lcd.print("Scan Finger to Unlock")
mainScrn()


from _finger import Finger
finger = Finger()
def fingerOKCb(user_id, access):
	clrscrn()
	lcd.print("Welcome\nUser #"+str(user_id))
	tone(TONE_DELIGHT)
	sleep_ms(1000)
	mainScrn()
def fingerDENYCb():
	clrscrn()
	lcd.print("Unknown  :(\nFinger")
	tone(TONE_DENY)
	sleep_ms(1000)
	mainScrn()
finger.readFingerCb(callback=fingerOKCb)
finger.getUnknownCb(callback=fingerDENYCb)

