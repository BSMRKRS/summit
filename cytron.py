import RoboPiLib as RPL
import setup

class Cytron:
    ############################################################################
    ###Initializing###
    ##################

    def __init__(self,
    max_pwm,
    m1_pwm,
    m1_dir,
    m1_name=None,
    m2_pwm=None,
    m2_dir=None,
    m2_name=None,
    name=None,
    percent_power=100):

        self.name = name
        self.m1 = {"pwm":m1_pwm,"dir":m1_dir,"name":m1_name}
        self.m2 = {"pwm":m2_pwm,"dir":m2_dir,"name":m2_name}


        #Identification for debugger
        if self.name == None:
            self.name = "Cytron Motor Controller"
        if self.m1["name"] == None:
            self.m1["name"] = "Motor 1"
        if self.m2["name"] == None:
            self.m2["name"] = "Motor 2"


        #setting the default power
        #power is a percentage
        self.max_freq = max_pwm
        if percent_power >= 100:
            self.dpower = 100
        elif percent_power <= 0:
            self.dpower = 0
        else:
            self.dpower = percent_power


    def __repr__(self):
        return self.name
   #############################################################################



    ############################################################################
    ###Functions###
    ###############
    def power(self, percent):
        percentage = percent / 100.0
        freq = self.max_freq * percentage
        freq = int(freq)
        return freq


    ###Moving the motors
    # def control(self, motor=self.m1, direction=True, power=self.dpower):
    def control(self, motor=None, direction=True, power=None):

        if motor == None:
            motor = self.m1
        if power == None:
            power = self.dpower

        dir = 10000
        if direction:
            dir = 0

        pwm = self.power(power)

        try:
            RPL.servoWrite(motor["dir"], dir)
            RPL.servoWrite(motor["pwm"], pwm)

        except Exception as error:
            print("{} failed to write motor {} at {} because: {}").format(self, motor["name"], pwm, error)
            try:
                RPL.servoWrite(motor["dir"], 0)
                RPL.servoWrite(motor["pwm"], 0)
            except:
                pass

    #stopping the motors
    def stop(self, motor=None):
        if motor == None:
            motor = self.m1
        self.control(motor=motor, power=0)
   #############################################################################



###EXAMPLE:
# motor_controller = Cytron(max_pwm=20000, m1_pwm=0, m1_dir=1)
# m1 = motor_controller.m1
# motor_controller.control(motor=m1,direction=True)
