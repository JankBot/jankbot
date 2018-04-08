import smbus

i2c = smbus.SMBus(1)

class Car:
    def __init__(self, addr):
        self.addr = addr

    def drive(self, esc, steer):
        i2c.write_byte_data(self.addr, esc, steer);

car = Car(19)
