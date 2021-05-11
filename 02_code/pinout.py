from machine import Pin

class PinoutRp2040(Object):
    A0_VOL = machine.ADC(26)
    
    DI0_TAPE_SENSE_00 = Pin(27,Pin.IN)
    DI1_TAPE_SENSE_01 = Pin(28,Pin.IN)
    DI2_TAPE_SENSE_02 = Pin(29,Pin.IN)
    DI3_TAPE_SENSE_03 = Pin(24,Pin.IN)
    DI4_TAPE_SENSE_04 = Pin(25,Pin.IN)

    DI5_BUTTON_00 = Pin(12,Pin.IN)
    DI6_BUTTON_01 = Pin(11,Pin.IN)
    DI7_BUTTON_02 = Pin(3,Pin.IN)
    DI8_BUTTON_03 = Pin(2,Pin.IN)
    DI9_BUTTON_04 = Pin(4,Pin.IN)

    DO0_VOL_SENSE_EN = Pin(1,Pin.OUT)
    DO1_TAPE_SENSE_EN = Pin(0,Pin.OUT)
    DO2_LED = Pin(13,Pin.OUT)