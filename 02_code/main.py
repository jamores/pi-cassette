import io
import time

while True:
    for a in range(0,65536,10000):
        io.setLed(a)
        io.toString()
        time.sleep_ms(500)