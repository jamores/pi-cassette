import sd,io
import sdcard,spi_handler
import vs1053
import time
import uos

BUFFER_SIZE = 64

#sd.run()

class AudioFeeder(object):
    def __init__(self,dreq):
        self.cb_cnt = 0
        dreq.irq(self.cb,io.Pin.IRQ_RISING)
    def cb(self,_):
        self.cb_cnt += 1
    

audio = vs1053.VS1053(0,
        sck = io.pinout.SPI_SCK,
        mosi = io.pinout.SPI_MOSI,
        miso = io.pinout.SPI_MISO,
        cs = io.pinout.SPI_CS_MP3,
        xdcs = io.pinout.AUDIO_XDCS,
        dreq = io.pinout.AUDIO_DREQ)

sd_wrapper = sd.SDWrapper(0,sck=io.pinout.SPI_SCK, mosi=io.pinout.SPI_MOSI, miso=io.pinout.SPI_MISO, cs = io.pinout.SPI_CS_SD)
sd = sdcard.SDCard(sd_wrapper.spi, io.pinout.SPI_CS_SD)
uos.mount(sd, '/sd')

if 0:
    print("io : read text file")
    with open("/sd/file_00.txt",'r') as fp:
        for line in fp:
            print(line)
    print("io : DONE read text file")

if 0:
    print("io : read binary file")
    with open("/sd/mp3_01.mp3","rb") as fp:
        i_read = 0
        music_data = fp.read(BUFFER_SIZE)
        while(music_data):
            music_data = fp.read(BUFFER_SIZE)
            i_read += 1
            print(i_read)
    print("io : DONE read binary file")

if 1:
    audio.reset()
    print("audio : playing test tone")
    audio.set_volume(40,40)
    audio.sine_test(0x44,2.0)

if 1:
    print("audio : play MP3 file")
    
    #audio_feeder = AudioFeeder(io.pinout.AUDIO_DREQ)

    i_read = 0
    not_ready = 0
    audio.reset()
    audio.start_play()
    
    with open('/sd/mp3_01.mp3',"rb") as fp:
        audio.playb(fp)
    print("audio : STOP play MP3 file")

    if 0:
        with open('/sd/mp3_01.mp3',"rb") as fp:
            music_data = fp.read(BUFFER_SIZE)
            i_read += 1
            #while (music_data is not None) and (music_data != "") and (i_read <=10):
            while (music_data):
                while not audio.ready_for_data:
                    not_ready += 1
                audio.play(music_data)
                music_data = fp.read(BUFFER_SIZE)
                i_read += 1
                print(i_read*BUFFER_SIZE)
                print("audio : irq.cb_cnt : {}".format(audio_feeder.cb_cnt))
        print("audio : nr : {}".format(not_ready))
        print("audio : irq.cb_cnt : {}".format(audio_feeder.cb_cnt))
        print("audio : STOP play MP3 file")

while True:
    for a in range(0,65536,10000):
        io.setLed(a)
        io.toString()
        time.sleep_ms(500)