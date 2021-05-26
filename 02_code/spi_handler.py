import _thread as threading

class SPIHandler:
    locks = {}
    LOCK_TOUT = 1.5
    
    def __init__(self,id,spi,cs=None,baudrate=100000,polarity=0,phase=0,extra_clocks=0):
        self.id = id
        self.spi = spi
        self.baudrate = baudrate
        self.polarity = polarity
        self.phase = phase
        self.extra_clocs = extra_clocks
        # CS
        self.cs = cs
        if(self.cs):
            self.cs.init(mode=self.cs.OUT,value=1)
        # lock
        try:      
            if(self.__class__.locks[id] is None):self.__class__.locks[id] = threading.allocate_lock()
        except KeyError:
            self.__class__.locks[id] = threading.allocate_lock()

    
    def __enter__(self):
        if(self.__class__.locks[self.id].acquire() is False):
            # timeout
            return(None)
        self.spi.init(baudrate=self.baudrate,polarity=self.polarity,phase=self.phase)
        if(self.cs):self.cs.low()
        return(self)
        
    def __exit__(self,type,value,traceback):
        if(self.cs):
            self.cs.high()
        return(False)