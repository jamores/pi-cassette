from machine import Pin, SPI
from io import pinout

import sdcard
import spi_handler
import uos

def run():
    spi = SPI(0, sck=pinout.SPI_SCK, mosi=pinout.SPI_MOSI, miso=pinout.SPI_MISO)
    spih = spi_handler.SPIHandler(0,spi,pinout.SPI_CS_SD)
    sd = sdcard.SDCard(spi, pinout.SPI_CS_SD)
    uos.mount(sd, '/sd')

    with spih as spi_sd:
        for f in uos.listdir('/sd'):
            print(f)
        
