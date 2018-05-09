import smbus
import math

i2c = smbus.SMBus(1)

class Car(object):
    def __init__(self, addr, trim_throttle=0, trim_steer=0):
        self.addr = addr
        self.trim_throttle = trim_throttle
        self.trim_steer = trim_steer

    def drive(self, esc, steer):
        clip = lambda x: min(180, max(0, x))

        actual_throttle = int(clip(esc + self.trim_throttle))
        actual_steer = int(clip(steer + self.trim_steer))

        i2c.write_byte_data(self.addr, actual_throttle, actual_steer)


car = Car(19)


