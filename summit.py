import RoboPiLib as RPL
import sys,tty,termios,signal,setup,time
from cytron import Cytron

motor_controller = Cytron(max_pwm=20000, percent_power=10, m1_pwm=0, m1_dir=1)
motor = motor_controller.m1

RPL.pinMode(motor_controller.m1["pwm"], RPL.PWM)
RPL.pinMode(motor_controller.m1["dir"], RPL.OUTPUT)

steering_pin = 3
power = motor_controller.max_freq / 2
print("Initialized Motor Speed at {}/{} : 50%".format(power, motor_controller.max_freq))

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

def interrupted(signum, frame):
    stop()

def stop():
    motor_controller.stop()
    RPL.servoWrite(steering_pin, 1500)

def right(percent):
    RPL.servoWrite(steering_pin, 5 * percent + 1500)
def left(percent):
    RPL.servoWrite(steering_pin, -5 * percent + 1500)

def speed_change(fast):
    global power
    if fast:
        if power + 1000 >= motor_controller.max_freq:
            print("Maximum PWM Reached")
            power = motor_controller.max_freq
        else:
            power += 1000
    else:
        if power - 1000 <= 0:
            print("Minimum PWM Reached")
            power = 0
        else:
            power -= 1000
    print("PWM Frequency Updated: {}/{} : {}%".format(power, motor_controller.max_freq, int(power / motor_controller.max_freq) * 100))



print("Press 1 to quit")
signal.signal(signal.SIGALRM, interrupted)
tty.setraw(sys.stdin.fileno())
while True:
    DELAY = 0.5
    #key press delay is 0.5 seconds
    signal.setitimer(signal.ITIMER_REAL,DELAY)
    ch = sys.stdin.read(1)
    signal.setitimer(signal.ITIMER_REAL,0)
    if ch == '1':
        stop()
        termios.tcsetattr(fd,termios.TCSADRAIN, old_settings)
        break


    elif ch == ' ':
        print("Deus Halt")
        stop()


    elif ch == 'w':
        motor_controller.control(direction=False, power=power)
    elif ch == 's':
        motor_controller.control(direction=True, power=power)
    elif ch == 'a':
        left(100)
    elif ch == 'd':
        right(100)
    elif ch == 'q':
        left(25)
    elif ch == 'e':
        right(25)
    elif ch == ']':
        speed_change(True)
    elif ch == '[':
        speed_change(False)
