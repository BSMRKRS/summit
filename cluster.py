import RoboPiLib as RPL
import sys,tty,termios,signal,setup,time

backward_pin = 0
forward_pin  = 1
right_pin    = 2
left_pin     = 3
speed = 20000 #maximum frequency

race_mode = False
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

def interrupted(signum, frame):
    stop()

def stop():
    RPL.servoWrite(backward_pin,0)
    RPL.servoWrite(forward_pin,0)
    RPL.servoWrite(right_pin,0)
    RPL.servoWrite(left_pin,0)

def forward():
    RPL.servoWrite(backward_pin,0)
    RPL.servoWrite(forward_pin,speed)
def backward():
    RPL.servoWrite(forward_pin,0)
    RPL.servoWrite(backward_pin,speed)

def right():
    RPL.servoWrite(left_pin,0)
    RPL.servoWrite(right_pin,17000)
def left():
    RPL.servoWrite(right_pin,0)
    RPL.servoWrite(left_pin,17000)



signal.signal(signal.SIGALRM, interrupted)
tty.setraw(sys.stdin.fileno())
print("Press 1 to quit")
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
    elif ch == 'w':
        forward()
    elif ch == 's':
        backward()
    elif ch == 'a':
        left()
    elif ch == 'd':
        right()
    # elif ch == 'q':
    # elif ch == 'e':




#0 back, 1 forward, 2 right 3 left
#20,000             #1700
