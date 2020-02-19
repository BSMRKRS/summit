import RoboPiLib as RPL
import sys,tty,termios,signal,setup,time

#maximum = 20k
dir_pin = 1
pwm_pin = 0
max_speed = 10000 #maximum frequency
back_speed = 12000
dir_speed = 10000
steering_pin = 3

#race_mode = False
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

def interrupted(signum, frame):
    stop()

def stop():
    RPL.servoWrite(pwm_pin, 0)
    RPL.servoWrite(steering_pin, 1500)

def forward():
    RPL.servoWrite(dir_pin, 0)
    RPL.servoWrite(pwm_pin, max_speed)
def backward():
    RPL.servoWrite(dir_pin, dir_speed)
    RPL.servoWrite(pwm_pin, back_speed)

def right():
    RPL.servoWrite(steering_pin, 2000)
def left():
    RPL.servoWrite(steering_pin, 1000)

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
        RPL.servoWrite(pin,max_speed / 2)
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
        print("Deus Halt")
        stop()


    elif ch == 'w':
        forward()
    elif ch == 's':
        backward()
    elif ch == 'a':
        left()
    elif ch == 'd':
        right()
