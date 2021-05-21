from machine import ADC,Pin,PWM
import time

VOL_WAIT_MS = 10
A0_VOL = ADC(26)

TAPE_SENSE_WAIT_MS = 10
TAPE_SENSE_00 = Pin(0,Pin.IN) # DI0_TAPE_SENSE_00
TAPE_SENSE_01 = Pin(1,Pin.IN) # DI1_TAPE_SENSE_01
TAPE_SENSE_02 = Pin(2,Pin.IN) # DI2_TAPE_SENSE_02
TAPE_SENSE_03 = Pin(3,Pin.IN) # DI3_TAPE_SENSE_03
TAPE_SENSE_04 = Pin(6,Pin.IN) # DI4_TAPE_SENSE_04

BUTTON_WAIT_MS = 10
BUTTON_00 = Pin(12,mode=Pin.IN,pull=Pin.PULL_UP) # DI5_BUTTON_00
BUTTON_01 = Pin(11,mode=Pin.IN,pull=Pin.PULL_UP) # DI6_BUTTON_01
BUTTON_02 = Pin(24,mode=Pin.IN,pull=Pin.PULL_UP) # DI7_BUTTON_02
BUTTON_03 = Pin(25,mode=Pin.IN,pull=Pin.PULL_UP) # DI8_BUTTON_03

VOL_SENSE_EN = Pin(29,Pin.OUT,value=1)  # DO0_VOL_SENSE_EN
TAPE_SENSE_EN = Pin(28,Pin.OUT,value=1) # DO1_TAPE_SENSE_EN
DO2_LED = PWM(Pin(13,Pin.OUT,value=0))


def readTapeSense():
    # activate optical sensor enable
    TAPE_SENSE_EN.value(1)

    # wait
    time.sleep_ms(TAPE_SENSE_WAIT_MS)

    # read sensors
    _  = (  TAPE_SENSE_00.value(),
            TAPE_SENSE_01.value(),
            TAPE_SENSE_02.value(),
            TAPE_SENSE_03.value(),
            TAPE_SENSE_04.value())
    TAPE_SENSE_EN.value(0)
    return(_)

def readVolume():
    # activate optical sensor enable
    VOL_SENSE_EN.value(0)

    # wait
    time.sleep_ms(VOL_WAIT_MS)
    
    # read sensor
    _ = A0_VOL.read_u16()
    VOL_SENSE_EN.value(1)
    return(_)

def readButtons():
    _ = (BUTTON_00.value(),
        BUTTON_01.value(),
        BUTTON_02.value(),
        BUTTON_03.value())
    return(_)

def setLed(bright=65535):
    DO2_LED.duty_u16(bright)

def toString():
    print("---------------------------")
    _ = readTapeSense()
    print("TAPE_SENSE : {}".format(_))

    _ = readVolume()
    print("VOLUME     : {}".format(_))

    _ = readButtons()
    print("BUTTONS    : {}".format(_))