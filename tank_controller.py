import RoboPiLib as RPL
import sys,tty,termios,signal,setup,time

left1_pin = 0
left2_pin = 1

right1_pin = 2
right2_pin = 3


fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

def interrupted(signum, frame):
    stop()

def left(direction):
    RPL.servoWrite(left1_pin,0)
    RPL.servoWrite(left2_pin,0)
    if direction == "forward":
        RPL.servoWrite(left1_pin,2000)
    else:
        RPL.servoWrite(left2_pin,2000)

def right(direction):
    RPL.servoWrite(right1_pin,0)
    RPL.servoWrite(right2_pin,0)
    if direction == "forward":
        RPL.servoWrite(right1_pin,2000)
    else:
        RPL.servoWrite(right2_pin,2000)

def stop():
    RPL.servoWrite(left1_pin,0)
    RPL.servoWrite(left2_pin,0)
    RPL.servoWrite(right1_pin,0)
    RPL.servoWrite(right2_pin,0)




signal.signal(signal.SIGALRM, interrupted)
tty.setraw(sys.stdin.fileno())
print("Press q to quit")
while True:
    DELAY = 0.5
    #key press delay is 0.5 seconds
    signal.setitimer(signal.ITIMER_REAL,DELAY)
    ch = sys.stdin.read(1)
    signal.setitimer(signal.ITIMER_REAL,0)
    if ch == 'q':
        termios.tcsetattr(fd,termios.TCSADRAIN, old_settings)
        break
    elif ch == 'w':
        right("forward")
        left("forward")
    elif ch == 's':
        right("forward")
        left("backward")
    elif ch == 'a':
        right("backward")
        left("backward")
    elif ch == 'd':
        right("backward")
        left("forward")
