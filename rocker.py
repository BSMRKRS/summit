import RoboPiLib as RPL
import sys,tty,termios,signal,setup,time

class Controller:
    def __init__(self, left_forward_pin, left_backward_pin, right_forward_pin=None, right_backward_pin=None):
        self.pwm = 10000
        self.motors = []

        if left_forward_pin != None and right_forward_pin != None:
            motorL = [left_forward_pin, left_backward_pin]
            self.motors.append(motorL)
        if right_forward_pin != None and right_backward_pin != None:
            motorR = [right_forward_pin, right_backward_pin]
            self.motors.append(motorR)



    def stop(self, motor=None):
        if motor == None:
            for motor in self.motors:
                RPL.servoWrite(motor[0],0)
                RPL.servoWrite(motor[1],0)
        else:
            RPL.servoWrite(self.motors[0][0],0)
            RPL.servoWrite(self.motors[0][1],0)



    def control(self, motor_num, direction, pwm=self.pwm):
        self.stop(motor_num)
        motor = self.motors[motor_num]
        pin = motor[direction]
        RPL.servoWrite(pin, pwm)


fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)


#controller = Controller(0,1,2,3) #pass in pin numbers
#controller.control(0,1) #The first 0 or 1 determines left or right, the second 0 or 1 determines forward or backward


def interrupted(signum, frame):
    stop()



def stop():





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

except:
    print("Connection Dropped")
    stop()
    exit()
