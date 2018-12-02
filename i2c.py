import time
from  pylibftdi import BitBangDevice
class I2c:

    def __init__(self):
        self.device = BitBangDevice(auto_detach=False)
        self.ACK = 0  # Ответ удачный
        self.NACK = 1  # Ответ не удачный
        self.SCL = 0
        self.SDA = 4
        self.SDA_IN = 2
        self.OK = 0  # Линия в норме
        self.SCL_FAIL = 1  # Ошибка линии SCL
        self.SDA_FAIL = 2  # Ошибка линии SDA
        self.SDA_SCL_FAIL = 3  # Ошибка линий SCL и SDA
        self.device.direction |= (1 << self.SCL)
        self.device.direction |= (1 << self.SDA)
        self.device.direction &= ~(1 << self.SDA_IN)

    def delay(self):
        #time.sleep(0.0000001)	# Общая пауза на шине
        pass

    def __set_scl_hi(self): #Установка единицы на линии SCL
        self.device.port |= (1 << self.SCL)

    def __set_scl_low(self):
        self.device.port &= ~(1 << self.SCL) # Установка нуля на линии SCL

    def __set_sda_hi(self):
        self.device.port |= (1 << self.SDA)  # Установка единицы на линии SDA

    def __set_sda_low(self):
        self.device.port &= ~(1 << self.SDA) # Установка нуля на линии SDA

    def __get_sda_val(self):
        self.__set_scl_hi()
        val =  (self.device.read_pins() >> self.SDA_IN) & 0x1
        self.__set_scl_low()
        return val

    def stop(self):
        error = self.OK
        self.__set_scl_low()
        self.delay()
        self.__set_sda_low()
        self.delay()

        self.__set_scl_hi()
        self.delay()
        self.__set_sda_hi()
        self.delay()

        self.delay()
        self.delay()
        self.delay()
        self.delay()

    def start(self):
       self.__set_sda_low()
       self.delay()
       self.__set_scl_low()
       self.delay()

    def restart(self):
        self.set_sda_hi()
        self.delay()
        self.set_scl_hi()
        self.delay()
        self.set_sda_low()
        self.delay()
        self.set_scl_low()
        self.delay()

    def init(self):
        self.__set_sda_hi()
        self.__set_scl_hi()
        self.stop()

    def send_byte(self,data):
        ask = self.ACK
        for i in range(0,8):
            if ((data & 0b10000000) == 0):
                self.__set_sda_low()
            else:
                self.__set_sda_hi()

            self.delay()
            self.__set_scl_hi()
            self.__set_scl_low()
            data = (data << 1)

        self.__set_sda_hi()

        if self.__get_sda_val():
            ask = self.NACK
        else:
            ask = self.ACK
        return ask

    def read_byte(self,ask):
        byte = 0
        self.__set_sda_hi()
        for i in range(0,8):
            byte = (byte << 1)
            self.__set_scl_hi()
            self.delay()
            if self.__get_sda_val():
                byte |= 0x01
                self.__set_scl_low()
                self.delay()

        if (ask == self.ACK):
            self.__set_sda_low()
        else:
            self.__set_sda_hi()
        self.delay()
        self.__set_scl_hi()
        self.delay()
        self.__set_scl_low()
        self.delay()
        self.__set_sda_hi()

        return byte
