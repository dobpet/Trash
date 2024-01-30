from machine import Pin
import utime
import uasyncio

class Servo:

    # Global Variables
    __ActualSpeed = 0
    __ReqSpeed = 0
    __Ramp = 5000 #time from 0% to 100% of speed in ms
    
    Freq = 50 #for PWM
    #range of duty value from0 to 65535
    BackSpeed    = 2457 
    StopSpeed    = 4915
    ForwardSpeed = 7372 
    
    __PinServo = None    #machine.PWM(machine.Pin(x))

    LimitForStart = 5 #in procent
    __RegP = 1000    # regulation parameter
    __RegT = 100    # ms regulation parameter
    
    def SetRamp(self, Ramp):
        self.__Ramp = Ramp
        temp = Ramp / self.__RegT
        self.__RegP = 100 / temp #100%
        print("Calculated regulator P: " + str(self.__RegP))
        
    def __init__(self, PinServo, Ramp):
        self.__PinServo = PinServo
        self.__PinServo.freq(self.Freq)
        self.SetRamp(Ramp)
        
        self.__com = uasyncio.create_task(self.SpeedUpdate())
    
    def SetSpeedProc(self, Proc):#in range -100 to 100%
        if ((Proc <= 100) and (Proc >= -100)):
            self.__ReqSpeed = Proc
           
    def GetActualSpeed(self):
        return(self.__ActualSpeed)
    
    def SpeedCalculate(self):
        if True:
            """ linear calculation of speed"""
            if (((self.__ActualSpeed - self.__ReqSpeed) < self.__RegP) and (abs(self.__ActualSpeed - self.__ReqSpeed) >= self.__RegP )):                
                self.__ActualSpeed = self.__ActualSpeed + self.__RegP
            elif (((self.__ActualSpeed - self.__ReqSpeed) > self.__RegP) and (abs(self.__ActualSpeed - self.__ReqSpeed) >= self.__RegP )):
                self.__ActualSpeed = self.__ActualSpeed - self.__RegP
            else:
                self.__ActualSpeed = self.__ReqSpeed
            
            #print("SpeedCalculate: actual " + str(self.ActualSpeed) + " request " + str(self.ReqSpeed))
       
    def MoveRun(self, Speed):
        mSpeed = Speed
        k = 0
        q = 0
        if mSpeed >= 0:            
            k = (self.ForwardSpeed - self.StopSpeed) / (100 - 0)
            q = self.ForwardSpeed - (k * 100)
        if mSpeed < 0:            
            k = (self.BackSpeed - self.StopSpeed) / (-100 - 0)
            q = self.BackSpeed - (k * - 100)
            
        duty = k * mSpeed + q
        print("actual duty: ", duty)      
        self.__PinServo.duty_u16(int(duty))
        
    def MoveStop(self):
        self.__PinServo.duty_u16(self.StopSpeed)
        
    async def SpeedUpdate(self):
        while True:
            self.SpeedCalculate()
            #print("Actual speed: " + str(self.__ActualSpeed))
            if (abs(self.__ActualSpeed) > self.LimitForStart):
                self.MoveRun(self.__ActualSpeed)
            else:
                self.MoveStop()
            
            await uasyncio.sleep_ms(self.__RegT)


# PinRight = machine.PWM(machine.Pin(15)) #4, 15
# Motor = ServoClass(PinRight, 5000)
# 
# PinLeft = machine.PWM(machine.Pin(4)) #4, 15
# MotorLeft = ServoClass(PinLeft, 5000)
# 
# speed = 100
# Motor.SetSpeedProc(speed)
# MotorLeft.SetSpeedProc(speed)
# async def main():    
#     
#     while True:
#         print("main")
#         if (Motor.GetActualSpeed() >= 100):
#             Motor.SetSpeedProc(-100)
#             MotorLeft.SetSpeedProc(-100)
#         elif (Motor.GetActualSpeed() <= -100):
#             Motor.SetSpeedProc(100)
#             MotorLeft.SetSpeedProc(100)
# 
#             
#         await uasyncio.sleep_ms(30000)
# 
# uasyncio.run(main())
