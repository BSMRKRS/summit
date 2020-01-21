import RoboPiLib as RPL
import sys,tty,termios,signal,setup,time

foot_down = 5
foot_up = 4
right_backward = 3
right_forward  = 2
left_backward  = 1
left_forward   = 0
speed = 20000


fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

def interrupted(signum, frame):
    stop()

def extend():
    RPL.servoWrite(foot_down,0)
    RPL.servoWrite(foot_up,10000)

def retract():
    RPL.servoWrite(foot_up,0)
    RPL.servoWrite(foot_down,10000)

def left(direction):
    if direction == "forward":
        RPL.servoWrite(left_backward,0)
        RPL.servoWrite(left_forward,speed)
    elif direction == "backward":
        RPL.servoWrite(left_forward,0)
        RPL.servoWrite(left_backward,speed)
    else:
        print("Invalid input")
        stop()

def right(direction):
    if direction == "forward":
        RPL.servoWrite(right_backward,0)
        RPL.servoWrite(right_forward,speed)
    elif direction == "backward":
        RPL.servoWrite(right_forward,0)
        RPL.servoWrite(right_backward,speed)
    else:
        print("Invalid input")
        stop()

def stop():
    RPL.servoWrite(right_backward,0)
    RPL.servoWrite(right_forward,0)
    RPL.servoWrite(left_backward,0)
    RPL.servoWrite(left_forward,0)
    RPL.servoWrite(foot_up,0)
    RPL.servoWrite(foot_down,0)





signal.signal(signal.SIGALRM, interrupted)
tty.setraw(sys.stdin.fileno())
print("Press q to quit")
try:
    while True:
        DELAY = 0.5
        #key press delay is 0.5 seconds
        signal.setitimer(signal.ITIMER_REAL,DELAY)
        ch = sys.stdin.read(1)
        signal.setitimer(signal.ITIMER_REAL,0)
        if ch == 'q':
            stop()
            termios.tcsetattr(fd,termios.TCSADRAIN, old_settings)
            break
        elif ch == ' ':
            print("DEUS HALT")
            stop()
        elif ch == 'w':
            right("forward")
            left("forward")
        elif ch == 's':
            right("backward")
            left("backward")
        elif ch == 'd':
            left("forward")
            right("backward")
        elif ch == 'a':
            left("backward")
            right("forward")
        elif ch == 'z':
            extend()
        elif ch == 'x':
            retract()
except:
    print("Connection Dropped")
    stop()
    exit()
