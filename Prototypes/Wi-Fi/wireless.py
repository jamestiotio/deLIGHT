# Wi-Fi Lighter Unlock Script
# Use ampy to put the code and use rshell to REPL into ESP32 and run the script.
# Set it to run on boot by renaming the file to main.py
# Created by James Raphael Tiovalen (2019)

# Import libraries
import utime
import network
import machine
from ST7735 import TFT
from sysfont import sysfont
import math

import esp
esp.osdebug(None)

import gc
gc.collect()

# Define Wi-Fi Access Point SSID & Password
ap_ssid = 'deLIGHTer'
ap_password = ''
authorized_users = [b'']  # Extend this to non-hardcoded list

# Define Wi-Fi Station SSID & Password
sta_ssid = ''
sta_password = ''

# Define PWM variables for servo control
# Duty for servo is between 41 - 120, but mileage might differ
pin = machine.Pin(26)
servo = machine.PWM(pin, freq=50)
LID_CLOSE = 120
LID_OPEN = 60
servo_state = 'CLOSED'

# Define button for closing servo
button = machine.Pin(37, machine.Pin.IN)


# Enable LCD power through power management IC (AXP192)
def enable_lcd_power():
    i2c = machine.I2C(-1, scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
    i2c.writeto_mem(0x34, 0x28, b'\xff')
    axp192_reg12 = i2c.readfrom_mem(0x34, 0x12, 1)[0]
    axp192_reg12 |= 0x0c
    i2c.writeto_mem(0x34, 0x12, bytes([axp192_reg12]))

enable_lcd_power()

# Define variables for LCD access and print title
spi = machine.SPI(1, baudrate=27000000, polarity=0, phase=0, bits=8, firstbit=machine.SPI.MSB, sck=machine.Pin(13), mosi=machine.Pin(15))  # Set baudrate way high but will be clamped to a maximum in SPI constructor
tft = TFT(spi,23,18,5)
tft.initr()  # Initialize LCD screen
tft.invertcolor(True)  # This is required for RGB to be parsed correctly (for some reason, 0x00 and 0xFF are flipped on normal mode)
tft.rgb(True)
tft.rotation(3)  # Rotate to landscape mode
tft.fill()  # We use black background since text chars would be encapsulated by black background, not transparent

tft.text((20,40), 'deLIGHT', TFT.YELLOW, sysfont, 3, nowrap=True)
tft.text((20,70), 'Wi-Fi', TFT.CYAN, sysfont, 2, nowrap=True)


def station():
    # Enable station interface
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    
    # Main station loop
    while True:
        scan_result = sta.scan()
        for i in scan_result:
            if i[0] == bytes(sta_ssid, 'utf-8'):
                sta.connect(sta_ssid, sta_password)
        
        # If connected to home network, break scan loop
        if sta.isconnected():
            print('Connected to home network!')
            break


def access_point():
    # Enable access point interface
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ap_ssid,authmode=network.AUTH_WPA_WPA2_PSK, password=ap_password)
    
    # Condition checking barrier for active access point
    while ap.active() == False:
        pass
    
    print('Access point created!')
    print(ap.ifconfig())  # Returns (ip, subnet/netmask, gateway, dns) as a tuple
    
    global servo_state

    # Define AP internal functions
    def wait_for_release():
        while True:
            if button.value() == 1:
                return

    
    def button_check():
        global servo_state
        while True:
            if servo_state == 'OPEN':
                servo.duty(LID_CLOSE)
                if not ap.isconnected():
                    tft.fill()
                    tft.text((20,40), 'Authorized device', TFT.RED, sysfont, 1, nowrap=True)
                    tft.text((20,50), 'disconnected!', TFT.RED, sysfont, 1, nowrap=True)
                    tft.text((20,70), 'Closing...', TFT.RED, sysfont, 1, nowrap=True)
                else:
                    tft.fill()
                    tft.text((20,40), 'Main button pressed!', TFT.RED, sysfont, 1, nowrap=True)
                    tft.text((20,70), 'Closing...', TFT.RED, sysfont, 1, nowrap=True)
                servo_state = 'CLOSED'
                return
    
    
    def device_scan():
        global servo_state
        while True:
            if button.value() == 0 and ap.isconnected():  # TODO: Add condition to pass to integrated finger module and do fingerprint method if ap.isconnected() == false (possibly use https://github.com/stinos/micropython-wrap)
                for i in range(len(ap.status('stations'))):
                    print('Got a connection from %s.' % str(ap.status('stations')[i][0]))
                    
                    if ap.status('stations')[i][0] in authorized_users and servo_state == 'CLOSED':
                        # Duty for servo is between 41 - 120, but mileage might differ
                        servo.duty(LID_OPEN)
                        servo_state = 'OPEN'
                        return
    

    while True:
        while True:
            if button.value() == 0 and servo_state == 'CLOSED':
                tft.fill()
                tft.text((20,40), 'Press main button to', TFT.YELLOW, sysfont, 1, nowrap=True)
                tft.text((20,50), 'open the lighter!', TFT.YELLOW, sysfont, 1, nowrap=True)
                device_scan()
                tft.fill()
                tft.text((20,40), 'Authorized device', TFT.GREEN, sysfont, 1, nowrap=True)
                tft.text((20,50), 'connected!', TFT.GREEN, sysfont, 1, nowrap=True)
                tft.text((20,70), 'Opening...', TFT.GREEN, sysfont, 1, nowrap=True)
                wait_for_release()
                break

        while True:
            if (servo_state == 'OPEN') and (button.value() == 0 or not ap.isconnected()):
                button_check()
                wait_for_release()
                break


def main():
    # station()  # TODO: Need to forward network packet data to the Internet and back to corresponding devices so that we can use ESP32 as Wi-Fi Repeater as well to maintain Internet access for connected stations.
    access_point()


main()
