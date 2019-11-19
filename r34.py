import RoboPiLib as RPL
import sys,tty,termios,signal,setup,time

race_mode = False
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
global initial
initial = True

def interrupted(signum, frame):
    global initial
    initial = True
    move(0)
    turn(1420)

def stop():
    global initial
    initial = True
    move(0)
    print("Deus Halt")

def move(speed):
    global initial
    if speed == 0 or speed == 1500:
        RPL.servoWrite(2,0)
    else:
        RPL.servoWrite(2,speed)

def turn(direction):
    #1000 = left
    #1420 = straight
    #2000 = right
    RPL.servoWrite(1,direction)



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
        stop()
    elif ch == 'w':
        move(2000)
    elif ch == 's':
        move(1000)
    elif ch == 'a':
        turn(1000)
    elif ch == 'd':
        turn(2000)
    elif ch == 'q':
        turn(1260)
    elif ch == 'e':
        turn(1560)


    elif ch == 'r':
        if race_mode:
            print("Cruise")
            race_mode = False
        else:
            print("Race mode activated")
            race_mode = True
