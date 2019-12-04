# Wi-Fi Lighter Unlock Script
# Use ampy to put the code and use rshell to REPL into ESP32 and run the script.
# Created by James Raphael Tiovalen (2019)

# Import libraries
import utime
import network
import machine

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
LID_OPEN = 41
servo_state = 'CLOSED'

# Define button for closing servo
button = machine.Pin(37, machine.Pin.IN)


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
                    print('Authorized device disconnected! Closing...')
                else:
                    print('Main button pressed! Closing...')
                servo_state = 'CLOSED'
                return


    def device_scan():
        global servo_state
        while True:
            if button.value() == 0 and ap.isconnected():  # TODO: Add condition to pass to integrated finger module and do fingerprint method if ap.isconnected() == false
                for i in range(len(ap.status('stations'))):
                    print('Got a connection from %s.' % str(ap.status('stations')[i][0]))
                    
                    if ap.status('stations')[i][0] in authorized_users and servo_state == 'CLOSED':
                        # Duty for servo is between 41 - 120, but mileage might differ
                        servo.duty(LID_OPEN)
                        servo_state = 'OPEN'
                        return
    
    
    # Main access point loop
    # TODO: Add LCD screen text indicators
    # M5Stack module is not available in the current firmware used for the M5 stick
    # Need to fetch the Lobo MicroPython build
    while True:
        while True:
            if button.value() == 0 and servo_state == 'CLOSED':
                device_scan()
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
