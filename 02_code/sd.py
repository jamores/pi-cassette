from machine import Pin, SPI
from io import pinout
import sdcard
import uos

def run():
    spi = SPI(0, sck=pinout.SPI_SCK, mosi=pinout.SPI_MOSI, miso=pinout.SPI_MISO)
    sd = sdcard.SDCard(spi, pinout.SPI_CS_SD)
    uos.mount(sd, '/sd')

    for f in uos.listdir('/sd'):
        print(f)

#with open("/sd/test.txt", "w") as f:
#    f.write("Hello world!\r\n")
