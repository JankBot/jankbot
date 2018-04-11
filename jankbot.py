#!/usr/bin/env python3

from picamera import PiCamera

camera = PiCamera()

if __name__ == '__main__':
    for n in range(30):
        with open('test{}.jpg'.format(n), 'wb') as img:
            camera.capture(img)
    with open('index.html', 'w') as html:
        for n in range(30):
            html.write('<img src="test{}.jpg" /><br/>'.format(n))

