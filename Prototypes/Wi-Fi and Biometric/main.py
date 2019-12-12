# DELIGHT BIOMETRIC UPY
# RAGULBALAJI 2019

from m5stack import lcd, buttonA, buttonB
from random import randint, getrandbits
from time import sleep_ms
from machine import Pin, PWM, reset
import json

def readConfig():
	config = json.load(open('lighter.json'))
	return config
	
def writeConfig(config): # Use responsibly
	cfile = open('lighter.json','w')
	json.dump(config, cfile)
	cfile.close()

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


GAME_RUNNING = False
def game_start():
	lcd.font(lcd.FONT_DejaVu18)
	GAME_RUNNING = True
	HEALTH = 10
	bird = [80,20,0,0,15] # y,x,vy,vx,r
	blns = [[80,-10,0,-1,15,lcd.BLUE],[40,-10,0.2,-0.5,10,lcd.GREEN]] # y,x,vy,vx,r,color
	GRAV = -1
	lastbtn = False
	while GAME_RUNNING:
		if HEALTH < 1: break
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
	lcd.text(40,0,"GAME")
	lcd.text(20,0,"OVER")
	sleep_ms(700)
	tone(TONE_DENY)
	reset()

from _finger import Finger
finger = Finger()
IGNORE_FINGER = False
def fingerOKCb(user_id, access):
	global IGNORE_FINGER
	if IGNORE_FINGER: return
	GAME_RUNNING = False
	clrscrn()
	lcd.print("Welcome\nUser #"+str(user_id))
	tone(TONE_DELIGHT)
	sleep_ms(1000)
	mainScrn()
def fingerDENYCb():
	global IGNORE_FINGER
	if IGNORE_FINGER: return
	GAME_RUNNING = False
	clrscrn()
	lcd.print("Unknown  :(\nFinger")
	tone(TONE_DENY)
	sleep_ms(1000)
	clrscrn()
	lcd.setTextColor(lcd.MAGENTA)
	lcd.print("Hold button\nto skip\nthe game")
	sleep_ms(2000)
	if buttonA.isPressed(): mainScrn()
	else: game_start()
finger.readFingerCb(callback=fingerOKCb)
finger.getUnknownCb(callback=fingerDENYCb)

def enrolCb():
	global IGNORE_FINGER
	IGNORE_FINGER = True
	clrscrn()
	lcd.setTextColor(lcd.RED)
	lcd.print("Counting\nRegistered\nUsers")
	finger.uart.read()
	finger.uart.write(b'\xf5\t\x00\x00\x00\x00\t\xf5')
	sleep_ms(50)
	pkt = finger.uart.read(8)
	while len(pkt) != 8: pkt = finger.uart.read(8) 
	print(pkt)
	if pkt[0] != 0xf5 or pkt[1] != 0x09:
		clrscrn()
		tone(TONE_DENY)
		lcd.print("TRY AGAIN\n:(")
		sleep_ms(1000)
		mainScrn()
	usrid = pkt[3]
	clrscrn()
	lcd.setTextColor(lcd.GREEN)
	lcd.print("Enrol #"+str(usrid)+"\n")
	lcd.setTextColor(lcd.WHITE)
	lcd.print("Place Finger\non Sensor")
	finger.addUser(usrid+1, 1)
	while not finger.state.startswith("Add user success"):
		print(finger.state)
		sleep_ms(200)
	clrscrn()
	lcd.setTextColor(lcd.GREEN)
	lcd.print("Enrol Finger\n\nSUCCESS")
	IGNORE_FINGER = False
	sleep_ms(500)
	mainScrn()
buttonB.wasReleased(callback=enrolCb)

def mainScrn():
	clrscrn()
	lcd.setTextColor(lcd.RED)
	lcd.print("deLIGHTer\n")
	lcd.setTextColor(lcd.WHITE)
	lcd.print("Scan Finger to Unlock")
mainScrn()
