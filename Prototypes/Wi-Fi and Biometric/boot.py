# This file is executed on every boot (including wake-boot from deepsleep)
import sys
import gc

# Set default path
# Needed for importing modules and upip
sys.path.append('/flash/lib')
sys.path.append('/flash/sys_lib')

'''

# timer: init timer 0 as EXTBASE, m5cloud used 6, button use 7, speak use 8, mqtt use 9
# free: 1, 2, 3, 4, 5, 10, 11 -> need application: tof, ir
# pwm timer: analogWrite, lcd pwm use timer 1, speak use timer 2 , Serveo use timer3
from machine import Timer
tex = Timer(0)
tex.init(mode = tex.EXTBASE)

# boot view
import uos as os
import utime as time
# from m5stack import *
from config import __VERSION__
import ujson as json

from m5stack import *
import i2c_bus
import peripheral

def reboot(res):
    if axp.btnState() & 0x02:
        lcd.clear(lcd.BLACK)
        from machine import reset
        reset()

_time = peripheral.get_timer()
_timer = Timer(_time)
_timer.init(period=200, mode=_timer.PERIODIC, callback=reboot)

lcd.clear(lcd.BLACK)

lcd.image(lcd.CENTER, 35, 'img/uiflow_logo_80x80.bmp')
lcd.print(__VERSION__, lcd.CENTER, 10)

with open('modeconfig.json', 'r') as f:
    config = json.loads(f.read())

if config['start'] == 'flow':
    if config['mode'] == 'internet':
        lcd.print('Cloud', lcd.CENTER, 125)
    else:
        lcd.print('USB', lcd.CENTER, 125)
else:
    lcd.print(config['start'].upper(), lcd.CENTER, 120)
# wait 1000 for user choose
cnt_down = time.ticks_ms() + 800

while time.ticks_ms() < cnt_down:
    if buttonA.wasPressed():   # M5Cloud upload     
        lcd.clear()
        choose = 0
        lcd.image(0, 0, 'img/2-1.jpg')
        while True:
            time.sleep_ms(50)
            if buttonB.wasPressed():
                choose = choose + 1 if choose < 2 else 0
                lcd.image(0, 0, 'img/2-{}.jpg'.format(choose + 1))
            elif buttonA.wasPressed():
                if choose == 0:
                    core_start('flow')
                elif choose == 1:
                    from app_manage import file_choose
                    file_choose()
                    core_start('app')
                elif choose == 2:
                    import statechoose
                    statechoose.start()
                break
        break

with open('modeconfig.json', 'r') as f:
    config = json.loads(f.read())
# 0 -> run main.py
# 1 -> run flow.py
# 2 -> run debug.py
import m5base
if config['start'] == 'app':
    m5base.app_start(0)
elif config['start'] == 'flow':
    if config['mode'] == 'usb':
        m5base.app_start(3)
    else:
        m5base.app_start(1)
elif config['start'] == 'debug':
    m5base.app_start(2)

# m5button.clear()

config = None
cnt_down = None
gc.collect() 
del config
del cnt_down'''
