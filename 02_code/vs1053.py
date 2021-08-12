from spi_handler import SPIDevice
from micropython import const
import time

#_VS1053_CMD_BAUDRATE =   const(5000000)
#_VS1053_DATA_BAUDRATE = const(10752000)

_VS1053_CMD_BAUDRATE =   const(250000)
_VS1053_DATA_BAUDRATE =  const(8000000)
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
_VS1053_MODE_SM_LAYER12 = const(0x0002)
_VS1053_MODE_SM_RESET = const(0x0004)
_VS1053_MODE_SM_CANCEL = const(0x0008)
_VS1053_MODE_SM_DACT = const(0x0100)
_VS1053_MODE_SM_SDIORD = const(0x0200)
_VS1053_MODE_SM_SDINEW = const(0x0800)
_VS1053_MODE_SM_LINE1 = const(0x4000)

_VS1053_CLOCKF_VALUE = 0x8800

class VS1053(SPIDevice):
    _SPI_BUFFER = bytearray(4)

    def __init__(self,spi_id,sck,mosi,miso,cs,xdcs,dreq):
        self._xdcs = xdcs
        self._dreq = dreq

        super().__init__(spi_id,sck,mosi,miso,cs=cs)

        self._xdcs(1)
        self.reset()

    def _sci_write(self, address, value):
        _buf = self._SPI_BUFFER
        _buf[0] = _VS1053_SCI_WRITE
        _buf[1] = address & 0xff
        _buf[2] = (value >> 8) & 0xff
        _buf[3] = value & 0xff
        
        #with self as spi:
        #    spi.init(baudrate=_VS1053_CMD_BAUDRATE)
        #    spi.write(_buf)
        self._xdcs.value = True
        self.wait_dreq()
        self.spi.init(baudrate=_VS1053_CMD_BAUDRATE)
        self.spi.write(_buf)
        
    def _sci_read(self,address):
        _buf = self._SPI_BUFFER
        _buf[0] = _VS1053_SCI_READ
        _buf[1] =  address & 0xff
        _buf[2] =  0xff
        _buf[3] =  0xff

        #with self as spi:
        #    spi.init(baudrate=_VS1053_CMD_BAUDRATE)
        #    spi.write_readinto(_buf,_buf)
        self._xdcs.value = True
        self.wait_dreq()
        self.spi.init(baudrate=_VS1053_CMD_BAUDRATE)
        self.spi.write_readinto(_buf,_buf)
        return((_buf[2] << 8) | _buf[3])

    def _ram_read(self,address):
        self._sci_write(_VS1053_REG_WRAMADDR,address)
        return(self._sci_read(_VS1053_REG_WRAM))
    def _ram_write(self,address,value):
        self._sci_write(_VS1053_REG_WRAMADDR,address)
        return(self._sci_write(_VS1053_REG_WRAM,value))

    def soft_reset(self):
        self._sci_write(
            _VS1053_REG_MODE,
            _VS1053_MODE_SM_SDINEW | _VS1053_MODE_SM_RESET
        )
        time.sleep_ms(2)
        self.wait_dreq()
        self._sci_write(_VS1053_REG_CLOCKF,_VS1053_CLOCKF_VALUE)
        if(self._sci_read(_VS1053_REG_CLOCKF) != _VS1053_CLOCKF_VALUE):
            raise OSError("VS1053 _SCI_CLOCKF")
        time.sleep_ms(1)
        self.set_volume(40,40)
        self.wait_dreq()
    def reset(self):
        self._xdcs(1)
        self.soft_reset()
                
    def set_volume(self,left,right):
        volume = ((left & 0xff) << 8) | (right & 0xff)
        self._sci_write(_VS1053_REG_VOLUME,volume)
        
    @property
    def ready_for_data(self):
        return(self._dreq())
    def wait_dreq(self):
        while not self._dreq.value:
            pass


    def start_play(self):
        # reset
        self._sci_write(
            _VS1053_REG_MODE,
            _VS1053_MODE_SM_LINE1 | _VS1053_MODE_SM_SDINEW 
        )
        # resync
        #self._sci_write(_VS1053_REG_WRAMADDR, 0x1E29)
        #self._sci_write(_VS1053_REG_WRAM, 0)
        #self._sci_write(_VS1053_REG_DECODETIME, 0)

    def stop_play(self):
        self.print_HDAT()
        self._sci_write(
            _VS1053_REG_MODE,
            _VS1053_MODE_SM_LINE1 | _VS1053_MODE_SM_SDINEW | _VS1053_MODE_SM_CANCEL
        )
    
    def playb(self,stream,buf=bytearray(32)):
        
        while stream.readinto(buf):
            #while not self._dreq():
            #    pass
            self._xdcs.value(0)
            with self as spi:
                spi.init(baudrate=_VS1053_DATA_BAUDRATE)
                spi.write(buf)
            self._xdcs.value(1)
        else:
            self.stop_play()


    def play(self,data_buffer,start=0,end=None):
        try:
            if end is None:
                end = len(data_buffer)
            self._xdcs.value(0)
            with self as spi:
                spi.init(baudrate=_VS1053_DATA_BAUDRATE)
                spi.write(data_buffer)
        finally:
            self._xdcs.value(1)

    def sine_test(self,n,secs):
        #self.reset()
        mode = self._sci_read(_VS1053_REG_MODE)
        mode |= 0x0020
        self._sci_write(_VS1053_REG_MODE,mode)
        while not self.ready_for_data:
            pass
        try:
            self._xdcs.value(0)
            with self as spi:
                spi.init(baudrate=_VS1053_DATA_BAUDRATE)
                spi.write(bytes([0x53, 0xEF, 0x6E,n & 0xFF, 0x00, 0x00, 0x00, 0x00]))
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
    
    def print_HDAT(self):
        hdat1 = self._sci_read(_VS1053_REG_HDAT1)
        hdat0 = self._sci_read(_VS1053_REG_HDAT0)

        print("HDAT1 : "+str(hdat1))
        print("..sync "+str((hdat1&0xff70)>>5))
        print("..ID "+str((hdat1>>3)&0x0003))
        print("..layer "+str((hdat1>>1)&0x0003))
        print("..protect "+str(hdat1&0x0001))

        print("HDAT0 : "+str(hdat0))
        print("..bitr "+str((hdat0&0xf000)>>12))
        print("..sampler "+str((hdat0>>10)&0x0003))
        print("..mode "+str((hdat0>>6)&0x0003))
        