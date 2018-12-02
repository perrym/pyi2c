from i2c import I2c
SSD1306_LCDWIDTH   =   128
SSD1306_LCDHEIGHT   =   64
SSD1306_SETCONTRAST  = 0x81
SSD1306_DISPLAYALLON_RESUME =0xA4
SSD1306_DISPLAYALLON =0xA5
SSD1306_NORMALDISPLAY =0xA6
SSD1306_INVERTDISPLAY =0xA7
SSD1306_DISPLAYOFF =0xAE
SSD1306_DISPLAYON =0xAF
SSD1306_SETDISPLAYOFFSET =0xD3
SSD1306_SETCOMPINS =0xDA
SSD1306_SETVCOMDETECT= 0xDB
SSD1306_SETDISPLAYCLOCKDIV= 0xD5
SSD1306_SETPRECHARGE =0xD9
SSD1306_SETMULTIPLEX =0xA8
SSD1306_SETLOWCOLUMN =0x00
SSD1306_SETHIGHCOLUMN= 0x10
SSD1306_SETSTARTLINE =0x00
SSD1306_MEMORYMODE =0x20
SSD1306_COLUMNADDR =0x21
SSD1306_PAGEADDR  = 0x22
SSD1306_COMSCANINC= 0xC0
SSD1306_COMSCANDEC= 0xC8
SSD1306_SEGREMAP= 0xA0
SSD1306_CHARGEPUMP= 0x8D
SSD1306_EXTERNALVCC =0x1
SSD1306_SWITCHCAPVCC =0x2

SSD1306_ADDRESS= 0x78

class Ssd1306:
    def __init__(self):

        self.i2c = I2c()
        self.display_buffer = []
        for x in range(0, 1000):
            self.display_buffer.append(0x02)

    def send_command(self,c):
        self.i2c.start()
        self.i2c.send_byte(SSD1306_ADDRESS)
        self.i2c.send_byte(0x0)
        self.i2c.send_byte(c)
        self.i2c.stop()

    def set_col_addr(self):
        self.send_command(SSD1306_COLUMNADDR) # 0x21    COMMAND
        self.send_command(0) # Column    start    address
        self.send_command(SSD1306_LCDWIDTH - 1) # Column     end    address

    def set_page_addr(self):
        self.send_command(SSD1306_PAGEADDR)  # 0x22    COMMAND
        self.send_command(0)  # Column    start    address
        self.send_command(int(SSD1306_LCDHEIGHT/8) - 1)  # End Page address

    def send_data(self, data, data_size):
        self.set_col_addr()
        self.set_page_addr()
        self.i2c.start()
        self.i2c.send_byte(SSD1306_ADDRESS)
        self.i2c.send_byte(0x40)
        for j in range(0,data_size):
            self.i2c.send_byte(data[j])
        self.i2c.stop()

    def receive_data(self, data, data_size):
        self.set_col_addr()
        self.set_page_addr()
        self.i2c.start()
        self.i2c.send_byte(SSD1306_ADDRESS)
        self.i2c.send_byte(0x40)
        for j in range(0,data_size):
            self.i2c.send_byte(data[j])
        self.i2c.stop()


    def init(self):
        self.i2c.init()

        self.send_command(SSD1306_DISPLAYOFF) # 0xAE
        self.send_command(SSD1306_SETDISPLAYCLOCKDIV) # 0xD5
        self.send_command(0x80) # the
        self.send_command(SSD1306_SETMULTIPLEX) # 0xA8
        self.send_command(0x3D)
        self.send_command(SSD1306_SETDISPLAYOFFSET) # 0xD3
        self.send_command(0x0) # no
        self.send_command(SSD1306_SETSTARTLINE) # | 0x0) # line  # 0
        self.send_command(0x0)
        self.send_command(SSD1306_CHARGEPUMP) # 0x8D
        self.send_command(0x14) # using
        self.send_command(SSD1306_MEMORYMODE) # 0x20
        self.send_command(0x00) # 0x00
        self.send_command(SSD1306_SEGREMAP | 0x1) # rotate
        self.send_command(SSD1306_COMSCANDEC) # rotate
        self.send_command(SSD1306_SETCOMPINS) # 0xDA
        self.send_command(0x12)
        self.send_command(SSD1306_SETCONTRAST) # 0x81
        self.send_command(0xCF)
        self.send_command(SSD1306_SETPRECHARGE) # 0xd9
        self.send_command(0xF1)
        self.send_command(SSD1306_SETVCOMDETECT) # 0xDB
        self.send_command(0x40)
        self.send_command(SSD1306_DISPLAYALLON_RESUME) # 0xA4
        self.send_command(SSD1306_NORMALDISPLAY) # 0xA6
        self.send_command(SSD1306_DISPLAYON) # switch