from spi_handler import SPIDevice
from micropython import const
import time

_VS1053_CMD_BAUDRATE = const(250000)
_VS1053_DATA_BAUDRATE = const(8000000)
# CMD
_VS1053_SCI_READ = const(0x03)
_VS1053_SCI_WRITE = const(0x02)
# REGISTERS
_VS1053_REG_MODE = const(0x00)
_VS1053_REG_STATUS = const(0x01)
_VS1053_REG_BASS = const(0x02)
_VS1053_REG_CLOCKF = const(0x03)
_VS1053_REG_DECODETIME = const(0x04)
_VS1053_REG_AUDATA = const(0x05)
_VS1053_REG_WRAM = const(0x06)
_VS1053_REG_WRAMADDR = const(0x07)
_VS1053_REG_HDAT0 = const(0x08)
_VS1053_REG_HDAT1 = const(0x09)
_VS1053_REG_VOLUME = const(0x0B)
# MODES
_VS1053_MODE_SM_LINE1 = const(0x4000)
_VS1053_MODE_SM_SDINEW = const(0x0800)
_VS1053_MODE_SM_CANCEL = const(0x0008)
_VS1053_MODE_SM_RESET = const(0x0004)

class VS1053(SPIDevice):
    _SPI_BUFFER = bytearray(4)

    def __init__(self,spi_id,sck,mosi,miso,cs,xdcs,dreq):
        self._xdcs = xdcs
        self._dreq = dreq
        
        super().__init__(spi_id,sck,mosi,miso,cs)

    def _sci_write(self, address, value):
        self._SPI_BUFFER[0] = _VS1053_SCI_WRITE
        self._SPI_BUFFER[1] = address & 0xff
        self._SPI_BUFFER[2] = (value >> 8) & 0xff
        self._SPI_BUFFER[3] = value & 0xff
        
        with self as spi:
            spi.init(baudrate=_VS1053_CMD_BAUDRATE)
            spi.write(self._SPI_BUFFER)
    def _sci_read(self,address):
        self._SPI_BUFFER[0] = _VS1053_SCI_READ
        self._SPI_BUFFER[1] =  address & 0xff

        with self as spi:
            spi.init(baudrate=_VS1053_CMD_BAUDRATE)
            spi.write(self._SPI_BUFFER[:2])
            time.sleep(0.00001)
            spi.readinto(self._SPI_BUFFER)
        return((self._SPI_BUFFER[0] << 8) | self._SPI_BUFFER[1])


    def soft_reset(self):
        self._sci_write(
            _VS1053_REG_MODE,
            _VS1053_MODE_SM_SDINEW | _VS1053_MODE_SM_RESET
        )
        time.sleep(0.1)
    def reset(self):
        self._xdcs.value(1)
        self.soft_reset()
        time.sleep(0.1)
        self._sci_write(_VS1053_REG_CLOCKF,0x6000)
        self.set_volume(40,40)

    def set_volume(self,left,right):
        volume = ((left & 0xff) << 8) | (right & 0xff)
        self._sci_write(_VS1053_REG_VOLUME,volume)
        
    @property
    def ready_for_data(self):
        return(self._dreq.value())

    def start_play(self):
        # reset
        self._sci_write(
            _VS1053_REG_MODE,
            _VS1053_MODE_SM_LINE1 | _VS1053_MODE_SM_SDINEW
        )
        # resync
        self._sci_write(_VS1053_REG_WRAMADDR, 0x1E29)
        self._sci_write(_VS1053_REG_WRAM, 0)

    def stop_play(self):
        self._sci_write(
            _VS1053_REG_MODE,
            _VS1053_MODE_SM_LINE1 | _VS1053_MODE_SM_SDINEW | _VS1053_MODE_SM_CANCEL
        )
    
    def sine_test(self,n,secs):
        self.reset()
        mode = self._sci_read(_VS1053_REG_MODE)
        mode |= 0x0020
        self._sci_write(_VS1053_REG_MODE,mode)
        while not self.ready_for_data:
            pass
        #
        try:
            self._xdcs.value(0)
            with self as spi:
                spi.init(baudrate=_VS1053_DATA_BAUDRATE)
                spi.write(bytes([0x53, 0xEF, 0x6E,0xFF, 0x00, 0x00, 0x00, 0x00]))
        finally:
            self._xdcs.value(1)
        time.sleep(secs)
        try:
            self._xdcs.value(0)
            with self as spi:
                spi.init(baudrate=_VS1053_DATA_BAUDRATE)
                spi.write(bytes([0x45, 0x78, 0x69, 0x74, 0x00, 0x00, 0x00, 0x00]))
        finally:
            self._xdcs.value(1)