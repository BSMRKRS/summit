from cytron import Cytron
import RoboPiLib as RPL
import sys,tty,termios,signal,setup,time

controlling = False
inputs = ["stop"]

motor_controller = Cytron(max_pwm=20000, percent_power=25,
m1_pwm=1, m1_dir=0, m1_name="Linear Motor",
m2_pwm=3, m2_dir=2, m2_name="Turning Motor")

move = motor_controller.m1
turn = motor_controller.m2

race_mode = False
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

def power(percent):
    percentage = percent / 100.0
    freq = speed * percentage
    freq = int(freq)
    return freq


def interrupted(signum, frame):
    stop()

def stop():
    controlling = False
    inputs.append("stop")
    motor_controller.stop(motor=move)
    motor_controller.stop(motor=turn)


def forward():
    motor_controller.stop(motor=turn)
    motor_controller.control(motor=move, direction=True)
def backward():
    motor_controller.stop(motor=turn)
    motor_controller.control(motor=move, direction=False)

def right():
    motor_controller.stop(motor=move)
    motor_controller.control(motor=turn, direction=True)
def left():
    motor_controller.stop(motor=move)
    motor_controller.control(motor=turn, direction=False)




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
        print("Emergency stop")
        stop()

    else:
        direction_input = ch
        controlling = True


    if controlling:
        if direction_input != inputs[len(inputs) - 1]:
            inputs.append(direction_input)
            if direction_input == "w":
                forward()
            elif direction_input == "s":
                backward()
            elif direction_input == "a":
                left()
            elif direction_input == "d":
                right()



#0 back, 1 forward, 2 right 3 left
#20,000             #1700
