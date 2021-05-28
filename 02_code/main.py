import sd,io
import vs1053
import time

sd.run()

_ = vs1053.VS1053(0,
        sck = io.pinout.SPI_SCK,
        mosi = io.pinout.SPI_MOSI,
        miso = io.pinout.SPI_MISO,
        cs = io.pinout.SPI_CS_MP3,
        xdcs = io.pinout.AUDIO_XDCS,
        dreq = io.pinout.AUDIO_DREQ)
_.set_volume(10,10)
_.sine_test(0,2)
_.set_volume(20,20)
_.sine_test(10,2)
_.set_volume(30,30)
_.sine_test(20,2)
_.set_volume(40,40)
_.sine_test(10,2)

while True:
    for a in range(0,65536,10000):
        io.setLed(a)
        io.toString()
        time.sleep_ms(500)