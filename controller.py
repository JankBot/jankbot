import math

import numpy as np

LOOKAHEAD = 100
DRIFT = .01  # rad/px offset
RAD_PER_DEG_STEER = math.pi/180 * (2/3)
SPEED = 105
SMOOTHING = 1.0


def smooth(old, new, alpha=SMOOTHING):
    if old is None:
        return new

    return [
        old_val + alpha * (new_val - old_val)
        for old_val, new_val in zip(old, new)
    ]


class Controller(object):
    def __init__(self, car, cam):
        self.car = car
        self.cam = cam
        self.last_line = None

    def follow_line(self, line):
        self.last_line = smooth(self.last_line, line)
        p = np.poly1d(self.last_line)

        theta_c = math.atan2(p(LOOKAHEAD), LOOKAHEAD)
        dist = math.cos(theta_c) * p(0)
        theta_t = dist * DRIFT
        theta = theta_c + theta_t
        # clip theta between -pi/2 and pi/2
        steer = theta / RAD_PER_DEG_STEER + 90
        speed = SPEED
        return speed, steer

    def step(self):
        line = self.cam.get_line()
        speed, steer = self.follow_line(line)

        self.car.drive(speed, steer)
