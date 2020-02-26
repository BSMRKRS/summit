import RoboPiLib as RPL
import sys,tty,termios,signal,setup,time

move_pin = [1,0]
turn_pin = [3,2]

speed = 20000 #maximum frequency

race_mode = False
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

def power(percent):
    percentage = percent / 100.0
    freq = speed * percentage
    freq = int(freq)
    print(freq)
    return freq


def interrupted(signum, frame):
    stop()

def stop():
    RPL.servoWrite(turn_pin[0], 0)
    RPL.servoWrite(move_pin[0], 0)

def forward(percent):
    stop()
    RPL.servoWrite(move_pin[1], 0)
    RPL.servoWrite(move_pin[0], power(percent))
def backward(percent):
    stop()
    RPL.servoWrite(move_pin[1], 1)
    RPL.servoWrite(move_pin[0], speed * (percent / 100))


def right(percent):
    stop()
    RPL.servoWrite(turn_pin[1], 0)
    RPL.servoWrite(turn_pin[0], speed * (percent / 100))
def left(percent):
    stop()
    RPL.servoWrite(turn_pin[1], 1)
    RPL.servoWrite(turn_pin[0], speed * (percent / 100))

def calibrate():
    calibration = True
    while calibration:
        print("Enter the pin number you want to test")
        print("Enter q to quit calibration")
        pin = raw_input("")
        try:
            pin = int(pin)
        except:
            if pin == 'q':
                calibration = False
                signal.signal(signal.SIGALRM, interrupted)
                tty.setraw(sys.stdin.fileno())
                print("Press 1 to quit")
                print("Press c to calibrate")
            else:
                print("Error setting that pin")
        RPL.servoWrite(pin,speed)
        time.sleep(1)
        RPL.servoWrite(pin,0)



print("Press 1 to quit")
print("Press c to calibrate")
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
    elif ch == 'c':
        stop()
        termios.tcsetattr(fd,termios.TCSADRAIN, old_settings)
        calibrate()
    elif ch == ' ':
        print("Emergency stop")
        stop()
    elif ch == 'w':
        forward(20)
    elif ch == 's':
        backward(20)
    elif ch == 'a':
        left(15)
    elif ch == 'd':
        right(15)
    # elif ch == 'q':
    # elif ch == 'e':




#0 back, 1 forward, 2 right 3 left
#20,000             #1700
