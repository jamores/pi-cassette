from machine import Pin, SPI
from io import pinout

import sdcard
import spi_handler
import uos

SD_SPI_ID = 0

class SDWrapper(spi_handler.SPIDevice):
    def __init__(self,spi_id,sck,mosi,miso,cs):
        super().__init__(spi_id,sck,mosi,miso,cs)

def run():
    sd_wrapper = SDWrapper(SD_SPI_ID,sck=pinout.SPI_SCK, mosi=pinout.SPI_MOSI, miso=pinout.SPI_MISO, cs = pinout.SPI_CS_SD)
    sd = sdcard.SDCard(sd_wrapper.spi, pinout.SPI_CS_SD)
    uos.mount(sd, '/sd')

    with sd_wrapper as spi:
        for f in uos.listdir('/sd'):
            print(f)

        
