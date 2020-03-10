import RoboPiLib as RPL
import sys,tty,termios,signal,setup,time
from cytron import Cytron

motor_controller = Cytron(max_pwm=20000, percent_power=10, m1_pwm=0, m1_dir=1)
motor = motor_controller.m1

RPL.pinMode(motor_controller.m1["pwm"], RPL.PWM)
RPL.pinMode(motor_controller.m1["dir"], RPL.OUTPUT)

steering_pin = 3
pwm_percent = 50
print("initialized Motor Speed at {}/{} : {}%".format((motor_controller.max_freq * pwm_percent) / 100, motor_controller.max_freq, pwm_percent))

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
    global pwm_percent
    if fast:
        if pwm_percent + 5 > 100:
            print("Maximum PWM Reached")
        else:
            pwm_percent += 5
    else:
        if pwm_percent - 5 < 0:
            print("Minimum PWM Reached")
        else:
            pwm_percent -= 5
    print("PWM Frequency Updated: {}/{} : {}%".format((motor_controller.max_freq * pwm_percent) / 100, motor_controller.max_freq, pwm_percent))



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
        motor_controller.control(direction=False, power=pwm_percent)
    elif ch == 's':
        motor_controller.control(direction=True, power=pwm_percent)
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
