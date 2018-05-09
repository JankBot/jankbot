import smbus

i2c = smbus.SMBus(1)


class Car(object):
    def __init__(self, addr, trim_throttle=0, trim_steer=0):
        self.addr = addr
        self.trim_throttle = trim_throttle
        self.trim_steer = trim_steer

    def drive(self, esc, steer):
        i2c.write_byte_data(self.addr, esc + self.trim_throttle, steer + self.trim_steer)


car = Car(19)


class Controller(object):
    def __init__(self, car, cam):
        self.car = car
        self.cam = cam

    def step(self):
        line = self.cam.get_line()

        speed = 100
        steer = 90

        self.car.drive(speed, steer)