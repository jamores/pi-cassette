import pinout
import time

while True:
    for a in range(0,65536,10000):
        pinout.setLed(a)
        pinout.toString()
        time.sleep_ms(500)