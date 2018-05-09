import smbus
import numpy as np
import math

i2c = smbus.SMBus(1)
LOOKAHEAD = 200
DRIFT = .01  # rad/px offset
RAD_PER_DEG_STEER = math.pi/180 * (2/3)
SPEED = 100

class Car(object):
    def __init__(self, addr, trim_throttle=0, trim_steer=0):
        self.addr = addr
        self.trim_throttle = trim_throttle
        self.trim_steer = trim_steer

    def drive(self, esc, steer):
        clip = lambda x: min(180, max(0, x))

        actual_throttle = clip(esc + self.trim_throttle)
        actual_steer = clip(steer + self.trim_steer)

        i2c.write_byte_data(self.addr, actual_throttle, actual_steer)


car = Car(19)


class Controller(object):
    def __init__(self, car, cam):
        self.car = car
        self.cam = cam

    def step(self):
        line = self.cam.get_line()
        p = np.poly1d(line)

        theta_c = math.atan2(p(LOOKAHEAD), LOOKAHEAD)
        dist = math.cos(theta_c) * p(0)
        theta_t = dist * DRIFT
        theta = theta_c + theta_t
        # clip theta between -pi/2 and pi/2
        steer = theta / RAD_PER_DEG_STEER + 90
        speed = SPEED

        self.car.drive(speed, steer)

