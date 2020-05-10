import time
import RoboPiLib as RPL
import setup

pwm_freq = 0
pwm_pin = int(raw_input("PWM Pin:  "))
step = int(raw_input("PWM Step: "))


try:
    while True:
        RPL.servoWrite(pwm_pin, pwm_freq)
        print("PWM Frequency at {}".format(pwm_freq))
        time.sleep(0.5)
        pwm_freq += step
except:
    RPL.servoWrite(pwm_pin, 0)
    print("Finished at {}".format(pwm_freq))
