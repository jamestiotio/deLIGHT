# Wi-Fi Lighter Unlock Script
# Use ampy to put the code and use rshell to REPL into ESP32 and run the script.
# Created by James Raphael Tiovalen (2019)

# Import libraries
import network
import machine

import esp
esp.osdebug(None)

import gc
gc.collect()

# Define Wi-Fi Access Point SSID & Password
ap_ssid = 'deLIGHTer'
ap_password = ''

# Define Wi-Fi Station SSID & Password
sta_ssid = ''
sta_password = ''

# Define PWM variables for servo control
# Duty for servo is between 40 - 115
pin = machine.Pin(4)
servo = machine.PWM(pin, freq=50)


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
    
    # Main access point loop
    while True:
        if ap.isconnected():
            for i in range(len(ap.status('stations'))):
                print('Got a connection from %s.' % str(ap.status('stations')[i][0]))
                
                # if ap.status('stations')[i][0] == b'':
                    # Duty for servo is between 40 - 115
                    # servo.duty(100)


def main():
    station()  # TODO: Need to forward network packet data to the Internet and back to corresponding devices so that we can use ESP32 as Wi-Fi Repeater as well to maintain Internet access for connected stations.
    access_point()


main()
