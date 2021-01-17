# microbit_sensor.py  17/01/2021  D.J.Whale
#
# 1. drag into python.microbit.org
# 2. download hex file and flash to microbit device.

from microbit import *
import radio

DEADZONE = 300
ACCMAX   = 1000
UPDATEMS = 500
STOP     = "S"
FORWARD  = "F"
BACKWARD = "B"
UNIQUE   = "RC"
seqno    = 0
#radio.configure(channel=7, power=6, group=0)

IMG_STOP  = Image("00000:00000:00900:00000:00000")
IMG_FWDM2 = Image("00000:09000:90000:09000:00000")
IMG_FWDM1 = Image("99000:90000:00000:00000:00000")
IMG_FWD0  = Image("00900:09090:00000:00000:00000")
IMG_FWDP1 = Image("00099:00009:00000:00000:00000")
IMG_FWDP2 = Image("00000:00090:00009:00090:00000")
IMG_BWDM1 = Image("00000:00000:00000:90000:99000")
IMG_BWD0  = Image("00000:00000:00000:09090:00900")
IMG_BWDP1 = Image("00000:00000:00000:00009:00099")

def sense(x, y):
    # work out which gear we are in
    if abs(y) < DEADZONE and abs(x) < DEADZONE:
        return STOP, 0, 0
    if y < 0: gear = FORWARD
    else:     gear = BACKWARD

    # work out rate
    rate = abs(y)
    if rate > ACCMAX: rate = ACCMAX
    rate -= DEADZONE  # 0..(ACCMAX-DEADZONE)
    rate = int(rate * 100 / (ACCMAX-DEADZONE))  # 0..100

    # work out steer
    steer = abs(x)
    if steer > ACCMAX: steer = ACCMAX
    steer -= DEADZONE
    steer = int(steer * 100 / (ACCMAX-DEADZONE))
    if x < 0: steer = -steer

    return gear, rate, steer

def update_display(gear, steer):
    spos = int(steer / 33)  # 0{0..33}, 1{34..66}, 2{67..99}
    img = IMG_STOP

    if gear == FORWARD:
        if   spos == -2: img = IMG_FWDM2
        elif spos == -1: img = IMG_FWDM1
        elif spos == 1:  img = IMG_FWDP1
        elif spos == 2:  img = IMG_FWDP2
        else:            img = IMG_FWD0

    elif gear == BACKWARD:
        if   spos < 0:   img = IMG_BWDM1
        elif spos > 0:   img = IMG_BWDP1
        else:            img = IMG_BWD0

    display.show(img)

def chksum(payload):
    return 0  #TODO

def dig2(v, signed=False):
    s = v < 0
    v = abs(v)
    if v > 99: v = 99
    if v < 10: v = "0" + str(v)
    else:      v = str(v)
    if signed:
        sf = "-" if s else "+"
        v = sf + v
    return v

def encode(gear, rate, steer, user=None):
    global seqno
    ba = "1" if button_a.is_pressed() else "0"
    bb = "1" if button_b.is_pressed() else "0"
    payload = UNIQUE + dig2(seqno) + ba + bb + gear + dig2(rate) + dig2(steer, signed=True)
    chk = dig2(chksum(payload))
    payload += chk
    if user is not None: payload += user
    seqno = (seqno + 1) % 100
    return payload

def loop():
    while True:
        x, y, z = accelerometer.get_values()
        ##print(x, y)
        gear, rate, steer = sense(x, y)
        ##print(gear, rate, steer)
        update_display(gear, steer)
        payload = encode(gear, rate, steer)
        print(payload)
        ##radio.send(payload)
        sleep(UPDATEMS)

# MAIN PROGRAM
radio.on()
loop()
