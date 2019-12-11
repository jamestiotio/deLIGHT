# DELIGHT BIOMETRIC UPY
# RAGULBALAJI 2019

from m5stack import lcd, buttonA
from random import randint, getrandbits
from time import sleep_ms
from machine import Pin, PWM, reset

TONE_DELIGHT = [(1174, 250), (1479, 250), (1760, 250), (2349, 500)]
TONE_DENY = [(1760, 100), (1, 50), (1760, 400)]

def clrscrn(rot=1):
	lcd.setRotation(rot)
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


GAME_RUNNING = False
def game_start():
	lcd.font(lcd.FONT_DejaVu18)
	GAME_RUNNING = True
	HEALTH = 20
	bird = [80,20,0,0,15] # y,x,vy,vx,r
	blns = [[80,-10,0,-1,15,lcd.BLUE],[40,-10,0.2,-0.5,10,lcd.GREEN]] # y,x,vy,vx,r,color
	GRAV = -1
	lastbtn = False
	while GAME_RUNNING:
		if HEALTH < 0: break
		if buttonA.isPressed() and not lastbtn: bird[2] += 15
		lastbtn = buttonA.isPressed()
		bird[2] += GRAV
		bird[2] *= 0.9
		bird[0] += bird[2]
		bird[0] = min(max(bird[4], bird[0]), 160-bird[4])
		lcd.clear()
		lcd.fillCircle(int(bird[0]), bird[1], bird[4], lcd.RED)
		lcd.fillCircle(int(bird[0])+6, bird[1]+2, 3, lcd.WHITE)
		lcd.fillCircle(int(bird[0])+6, bird[1]+10, 3, lcd.WHITE)
		lcd.fillCircle(int(bird[0])+6, bird[1]+2, 1, lcd.BLACK)
		lcd.fillCircle(int(bird[0])+6, bird[1]+10, 1, lcd.BLACK)
		lcd.fillTriangle(int(bird[0])-5, bird[1]+13, int(bird[0])-10, bird[1]+3, int(bird[0]), bird[1]+3, lcd.YELLOW)
		for b in blns:
			if b[1] < -b[4]:
				b[1] = 80+b[4]
				b[0] = randint(20,140)
				b[2] = (randint(0,10)-5)/5.0
				b[3] = -randint(5,10)/5.0
				b[4] = randint(5,15)
				b[5] = getrandbits(24)
			b[0] += b[2]
			b[1] += b[3]
			if((b[0]-bird[0])**2 + (b[1]-bird[1])**2 < (bird[4]+b[4])**2):
				HEALTH -= 1
				b[1] = -100
				tone([(440, 100)])
			lcd.line(int(b[0]),int(b[1]),int(b[0])-(4*b[4]),int(b[1]),lcd.WHITE)
			lcd.fillCircle(int(b[0]),int(b[1]),b[4],b[5])
		lcd.print(str(HEALTH)+" <3",140,0,lcd.WHITE,rotate=90)
		sleep_ms(30)
	
	lcd.setTextColor(lcd.WHITE)
	lcd.print("GAME\nOVER")
	while not buttonA.isPressed(): sleep_ms(10)

from _finger import Finger
finger = Finger()
def fingerOKCb(user_id, access):
	GAME_RUNNING = False
	clrscrn()
	lcd.print("Welcome\nUser #"+str(user_id))
	tone(TONE_DELIGHT)
	sleep_ms(1000)
	mainScrn()
def fingerDENYCb():
	GAME_RUNNING = False
	clrscrn()
	lcd.print("Unknown  :(\nFinger")
	tone(TONE_DENY)
	sleep_ms(1000)
	game_start()
	reset()
finger.readFingerCb(callback=fingerOKCb)
finger.getUnknownCb(callback=fingerDENYCb)

