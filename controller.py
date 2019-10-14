import RoboPiLib as RPL
import sys,tty,termios,signal,setup,time

race_mode = False
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

def interrupted(signum, frame):
    RPL.servoWrite(0,0)
    RPL.servoWrite(1,1500)

def move(speed):
    print("Setting speed to %s" % (speed))
    RPL.servoWrite(2,speed)

def turn(direction):
    #1000 = left
    #1500 = straight
    #2000 = right
    RPL.servoWrite(1,direction)



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
        if race_mode:
            move(2000)
        else:
            move(1800)
    elif ch == 's':
        move(1300)
    elif ch == 'a':
        turn(1000)
    elif ch == 'd':
        turn(2000)
    elif ch == 'r':
        if race_mode:
            print("Cruise")
            race_mode = False
        else:
            print("Race mode activated")
            race_mode = True
