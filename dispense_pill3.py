
from __future__ import division
import time

import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)


servo_min = 150
servo_max = 600

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length //= 20       # 20 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 2, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(80)

print('Pill 003 dispensed')

    # Move servo on channel O between extremes.


pwm.set_pwm(2, 2, servo_max)
time.sleep(0.2)
pwm.set_pwm(2, 2, servo_min)
time.sleep(0.3)
