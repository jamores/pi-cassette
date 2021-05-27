import _thread as threading
from machine import SPI

class SPIDevice:
    locks = {}
    LOCK_TOUT = 1.0

    def __init__(self,id,sck,mosi,miso,cs=None):
        self.id = id
        # CS
        self.cs = cs
        if(self.cs):self.cs.init(mode=self.cs.OUT,value=1)
        # SPI channel LOCK
        try:      
            if(self.__class__.locks[id] is None):self.__class__.locks[id] = threading.allocate_lock()
        except KeyError:
            self.__class__.locks[id] = threading.allocate_lock()
        # SPI
        self.spi = SPI(id,sck=sck,mosi=mosi,miso=miso)

    def __enter__(self):
        if(self.__class__.locks[self.id].acquire() is False):
            # timeout
            return(None)
        if(self.cs):self.cs.low()
        return(self.spi)

    def __exit__(self,type,value,traceback):
        if(self.cs):
            self.cs.high()
        return(False)
