from machine import Pin, SPI
from io import pinout

import sdcard
import spi_handler
import uos

SD_SPI_ID = 0

def run():
    spi_sd = spi_handler.SPIDevice(SD_SPI_ID,sck=pinout.SPI_SCK, mosi=pinout.SPI_MOSI, miso=pinout.SPI_MISO, cs = pinout.SPI_CS_SD)
    sd = sdcard.SDCard(spi_sd.spi, pinout.SPI_CS_SD)
    uos.mount(sd, '/sd')

    with spi_sd as spi:
        for f in uos.listdir('/sd'):
            print(f)

        
