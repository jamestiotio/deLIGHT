import ubluetooth, utime

bt = ubluetooth.BLE()
bt.active(True)

LIGHTER_SERVICE = ubluetooth.UUID("276a050e-7b9f-49bb-80f1-117952adc1f6")
LIGHTER_CHAR = (ubluetooth.UUID("0538f7de-1bf7-466b-b06e-f5f98b3fdfdb"), ubluetooth.FLAG_READ|ubluetooth.FLAG_NOTIFY,)

((hr,),) = bt.gatts_register_services(((LIGHTER_SERVICE, (LIGHTER_CHAR,),),))

def bt_irq(event, data):
    print('bt irq', event, data)

IRQ_ALL = const(0xffff)
bt.irq(bt_irq, IRQ_ALL)

def adv_encode(adv_type, value):
    return bytes((len(value) + 1, adv_type,)) + value

def adv_encode_name(name):
    return adv_encode(0x09, name.encode())

def adv():
    bt.gap_advertise(100, adv_encode(0x01, b'\x06') + adv_encode(0x03, b'\x0d\x18') + adv_encode(0x19, b'\xc1\x03') + adv_encode_name('delighter'))

adv()