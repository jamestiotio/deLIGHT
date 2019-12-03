# Bluetooth Lighter Unlock Script
# Use ampy to put the code and use rshell to REPL into ESP32 and run the script.
# IMPORTANT NOTE: Pairing is not supported by ubluetooth yet as of the time of writing of this code.
# Created by James Raphael Tiovalen (2019)

# Import libraries
import ubluetooth, utime
from micropython import const
import machine

# Initialize BLE singleton class object
bt = ubluetooth.BLE()

# Define UUIDs (or can use GATT service name in terms of bytes)
# UUID Generator: https://www.uuidgenerator.net/
LIGHTER_UUID = ubluetooth.UUID(0x1815)
# Indicate GATT characteristics
# List of characteristics: https://www.bluetooth.com/specifications/gatt/characteristics/
LIGHTER_CHAR = (ubluetooth.UUID(0x2B37), ubluetooth.FLAG_READ | ubluetooth.FLAG_NOTIFY,)
LIGHTER_SERVICE = ((LIGHTER_UUID, (LIGHTER_CHAR,),),)

# Define constants for BLE IRQ
_IRQ_ALL = const(0xffff)
_IRQ_CENTRAL_CONNECT                 = const(1 << 0)
_IRQ_CENTRAL_DISCONNECT              = const(1 << 1)
_IRQ_GATTS_WRITE                     = const(1 << 2)
_IRQ_GATTS_READ_REQUEST              = const(1 << 3)
_IRQ_SCAN_RESULT                     = const(1 << 4)
_IRQ_SCAN_COMPLETE                   = const(1 << 5)
_IRQ_PERIPHERAL_CONNECT              = const(1 << 6)
_IRQ_PERIPHERAL_DISCONNECT           = const(1 << 7)
_IRQ_GATTC_SERVICE_RESULT            = const(1 << 8)
_IRQ_GATTC_CHARACTERISTIC_RESULT     = const(1 << 9)
_IRQ_GATTC_DESCRIPTOR_RESULT         = const(1 << 10)
_IRQ_GATTC_READ_RESULT               = const(1 << 11)
_IRQ_GATTC_WRITE_STATUS              = const(1 << 12)
_IRQ_GATTC_NOTIFY                    = const(1 << 13)
_IRQ_GATTC_INDICATE                  = const(1 << 14)

# Define PWM variables for servo control
pin = machine.Pin(4)
servo = machine.PWM(pin, freq=50)


### Start defining functions for scan purposes

def adv_decode(adv_type, data):
    i = 0
    while i + 1 < len(data):
        if data[i + 1] == adv_type:
            return data[i + 2:i + data[i] + 1]
        i += 1 + data[i]
    return None


def adv_decode_name(data):
    n = adv_decode(const(0x09), data)
    if n:
        return n.decode('utf-8')
    return data


### End of scanning functions

### Start defining functions for advertise purposes

def adv_encode(adv_type, value):
    return bytes((len(value) + 1, adv_type,)) + value


def adv_encode_name(name):
    return adv_encode(const(0x09), name.encode())


def adv():
    # Indicate GATT service name in reverse byte order in second argument of adv_encode(0x03, b'')
    # List of services: https://www.bluetooth.com/specifications/gatt/services/
    bt.gap_advertise(100, adv_encode(0x01, b'\x06') + adv_encode(0x03, b'\x15\x18') + adv_encode(0x19, b'\xc1\x03') + adv_encode_name('deLIGHTer'))

### End of advertising functions


# Main event handler function
def bt_irq(event, data):
    if event == _IRQ_CENTRAL_CONNECT:
        # A central has connected to this peripheral.
        # NOTE: Default behavior of normal devices are acting as centrals, not peripherals.
        conn_handle, addr_type, addr = data
        print('bt irq', event, data)
        
        # Duty for servo is between 40 - 115
        # servo.duty(100)

    elif event == _IRQ_CENTRAL_DISCONNECT:
        # A central has disconnected from this peripheral.
        conn_handle, addr_type, addr = data
        # Start advertising again to allow a new connection.
        adv()
    
    elif event == _IRQ_SCAN_RESULT:
        # A single scan result.
        addr_type, addr, connectable, rssi, adv_data = data
        # For addr_type, 0 is public device address, while 1 is random device address.
        # No Resolvable Private Addresses are advertised (since Bluetooth v4.0) due to privacy reasons.
        # Even though some older devices might still emit their RPAs, this still remains a stubborn issue.
        print(addr_type, bytes(addr), adv_decode_name(adv_data))

    elif event == _IRQ_SCAN_COMPLETE:
        # Scan duration finished or manually stopped.
        print('Scan complete!')

    elif event == _IRQ_PERIPHERAL_CONNECT:
        # Connect successful.
        conn_handle, addr_type, addr = data
        bt.gattc_discover_services(conn_handle)
    
    elif event == _IRQ_PERIPHERAL_DISCONNECT:
        # Disconnect (either initiated by us or the remote end).
        conn_handle, addr_type, addr = data

    elif event == _IRQ_GATTC_SERVICE_RESULT:
        # Connected device returned a service.
        conn_handle, start_handle, end_handle, uuid = data
        bt.gattc_discover_characteristics(conn_handle, start_handle, end_handle)
    
    elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
        # Connected device returned a characteristic.
        conn_handle, def_handle, value_handle, properties, uuid = data
        print(data)
        
    elif event == _IRQ_GATTC_READ_RESULT:
        # A read completed successfully.
        conn_handle, value_handle, char_data = data
        print(data)
        
    elif event == _IRQ_GATTC_NOTIFY:
        # The script periodically notifies its value.
        conn_handle, value_handle, notify_data = data
        print(data)


def main():
    while not bt.active():
        # Activate ESP32's Bluetooth module
        bt.active(True)

    # Choose mode through REPL Python terminal
    command = input('Enter your command (scan/advertise): ')
        
    if command == 'scan':
        bt.irq(handler=bt_irq)
        # Scan continuously (at 100% duty cycle)
        bt.gap_scan(0, 30000, 30000)
    
    elif command == 'advertise':
        # Register GATT services only after bt is active
        ((dl,),) = bt.gatts_register_services(LIGHTER_SERVICE)
        bt.irq(bt_irq, _IRQ_ALL)
        adv()
    
    else:
        print('Input command is not valid!')


main()  # NOTE: Do not name this file as bluetooth.py, as that will cause module detection problems.
