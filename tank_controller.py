import RoboPiLib as RPL
import sys,tty,termios,signal,setup,time

Lmotor_pin = 0
Rmotor_pin = 1


fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

def interrupted(signum, frame):
    stop()

def forward():
    RPL.servoWrite(Lmotor_pin,2000)
    RPL.servoWrite(Rmotor_pin,1000)
def backward():
    RPL.servoWrite(Rmotor_pin,2000)
    RPL.servoWrite(Lmotor_pin,1000)
def left():
    RPL.servoWrite(Lmotor_pin,2000)
    RPL.servoWrite(Rmotor_pin,2000)
def right():
    RPL.servoWrite(Lmotor_pin,1000)
    RPL.servoWrite(Rmotor_pin,1000)
def stop():
    RPL.servoWrite(Lmotor_pin,0)
    RPL.servoWrite(Rmotor_pin,0)


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
        forward()
    elif ch == 's':
        backward()
    elif ch == 'a':
        left()
    elif ch == 'd':
        right()
