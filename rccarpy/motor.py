import RPi.GPIO as GPIO
import time
import sys
import copy
import numpy as np


# motor encoder pin
"""
# interrupt_PIN define
interrupt_Flag = 26

#EncoderMotor_Pin define
MOTOR1encoPinA = 21
MOTOR1encoPinB = 20

MOTOR2encoPinA = 16
MOTOR2encoPinB = 12

MOTOR3encoPinA = 1
MOTOR3encoPinB = 7

MOTOR4encoPinA = 8
MOTOR4encoPinB = 25

#encoder Position init
encoderPos = 0
"""

#=====================================================================
# using JMOD-Motor-Drive
# this version is able to control to four motor unsing 4CH
#============================================================================

# define Motor LIST
MOTOR1 = 1
MOTOR2 = 2

#Situationa LIST
Stop =0
Forward = 1
Backword = 2
Left = 3
Right = 4
Break = 5

#PWM PIN LIST : using motor speed pin (pwm pin -> dutycycle -> motor speed)

ENA = 26
ENB = 0

#GPIO PIN
#Left Motors
motor1IN1 = 19
motor1IN2 = 13

#Right Motors
motor2IN1 = 6
motor2IN2 = 5

#Configuration Settings
HIGH = 1       # enable
LOW = 0        # disenable
OUTPUT = 1
INPUT = 0

# sinit operation arrays
operation_array_left = np.zeros((1,3), dtype =int)
Movement = 0

#=================================================================
# Encoder motor function 
#=================================================================
"""
def setEncoderConfig(encINA, encINB):
    GPIO.setup(MOTOR1encoPinA, IO.IN, pull_up_down=IO.PUD_UP)
    GPIO.setup(MOTOR1encoPinB, IO.IN, pull_up_down=IO.PUD_UP)
    
    GPIO.setup(MOTOR2encoPinA, IO.IN, pull_up_down=IO.PUD_UP)
    GPIO.setup(MOTOR2encoPinB, IO.IN, pull_up_down=IO.PUD_UP)
    
    GPIO.setup(MOTOR3encoPinA, IO.IN, pull_up_down=IO.PUD_UP)
    GPIO.setup(MOTOR3encoPinB, IO.IN, pull_up_down=IO.PUD_UP)
    
    GPIO.setup(MOTOR4encoPinA, IO.IN, pull_up_down=IO.PUD_UP)
    GPIO.setup(MOTOR4encoPinB, IO.IN, pull_up_down=IO.PUD_UP)
    
def encoderA(channel):
    global encoderPos
    if IO.input(encPinA) == IO.input(encPinB):
        encoderPos += 1
    else:
        encoderPos -= 1

def encoderB(channel):
    global encoderPos
    if IO.input(encPinA) == IO.input(encPinB):
        encoderPos -= 1
    else:
        encoderPos += 1

def setInterruptConfig():
    GPIO.setup(interrupt_Flag,GPIO.IN,pull_up_down=GPIO.PUD_UP) 
"""

def dutyCycle_adjust(radius):
    DutyCycle1 = 0
    DutyCycle2 = 0
    if -3.6<= radius and radius <=3.6 :
        DutyCycle1 = 40
        DutyCycle2 = 40
        
    elif 3.6<radius and radius<=  4.6:
        DutyCycle1 = 41
        DutyCycle2 = 32
        
    elif 4.6<radius and radius<=  6.5:
        DutyCycle1 = 41
        DutyCycle2 = 25
        
    elif 6.5< radius:
        DutyCycle1 = 41
        DutyCycle2 = 18
        
    elif -3.6>radius and radius >=-4.6 :
        DutyCycle1 = 30
        DutyCycle2 = 41
        
    elif -6.5<radius and radius >= -4.6:
        DutyCycle1 = 25
        DutyCycle2 = 81
        
    elif radius <= -6.5:
        DutyCycle1 = 20
        DutyCycle2 = 46
    return DutyCycle1,DutyCycle2

#=======================================================================
# filtering of dutycycle it is fit for RC car speed
# <Prametor>
# mask : check to be same data as other data
# median Cycle: filtering of noise error
#=======================================================================
def check_Array(operation_array,resultArray):

#     print("1",operation_array)
#     print("2",resultArray)

    if(operation_array[0][0] == 0):
        operation_array = operation_array+resultArray
        #print(operation_array)
#         print("init_array",operation_array)
    else:
        operation_array = np.concatenate((operation_array,resultArray),axis = 0)
        #print("Concatenate array",operation_array)
        
        #slilcing movement in the total array
        MovementArray = operation_array[0:,1:2]

#         print("Movement",MovementArray)
        length = MovementArray.shape[0] #maybe changed?
#         print("length",length)
        mask = np.full((len(operation_array),1),MovementArray[0])
#        print("mask_setting",MovementArray[(mask== MovementArray)])
#        print(len(MovementArray[(mask== MovementArray)]))
        
        if length == len(MovementArray[(mask== MovementArray)]):
            dutycycle1 = medianOfduty(operation_array[0::2,2:3])
            dutycycle2 = medianOfduty(operation_array[1::2,2:3])
            print("d",dutycycle1, dutycycle2)
            operation_array[length-2:length-1, 2:3] = dutycycle1
            operation_array[length-1:length, 2:3] = dutycycle2
            print(operation_array[length-2:length-1, 2:3], operation_array[length-1:length, 2:3])
            #     print("return",operation_array)
    
    return operation_array

# filtering to nose and return median of ducy cycle 
def medianOfduty(Duty_array):
    return np.median(Duty_array)

#==============================================================
# error to RC car operation prameter (DIR and speed)
# <Prametor>
# Movement : RC car Moving Direction (Forward Backward Right Left )
# Duty Cycle : RC car Moving speed (tuning of duty cycle)
#=======================================================================
def isvaildPostion(error,operation_array):
   global Movement
   DutyCycle1 = 0
   DutyCycle2 = 0
   
   # Define of RC Car Forward opreation     
   if error <5 and error >-5:
       print("forward setting")
       Movement = Forward
       DutyCycle1 = 41
       DutyCycle2 = 35
       
   # Define of RC Car Right opreation (mirco moving)
   elif (error > 5 and error <= 15):
       print("Right setting")
       Movement = Right
       DutyCycle1 = 41
       DutyCycle2 = 30
       
   # Define of RC Car Right opreation (normal moving)
   elif (error >15  and error <= 30):
       Movement = Right
       DutyCycle1 = 41
       DutyCycle2 = 25
   
   # Define of RC Car Right opreation (large moving) 
   elif (error >30):
        Movement = Right
        DutyCycle1 = 41 
        DutyCycle2 = 20
   
   # Define of RC Car Left opreation (mirco moving) 
   elif (error < -5 and error > -15):
        Movement = Left
        DutyCycle1 = 30
        DutyCycle2 = 41
        
   # Define of RC Car Left opreation (normal moving)      
   elif (error >15  and error <= 30):
        Movement = Left
        DutyCycle1 = 25
        DutyCycle2 = 41
   
   # Define of RC Car Left opreation (Large moving)  
   elif (error <-30):
        Movement = Left
        DutyCycle1 = 20
        DutyCycle2 = 41
        
        
   resultArray = np.array([MOTOR1,Movement,DutyCycle1,MOTOR2,Movement,DutyCycle2]).reshape(2,3)
#    print(resultArray)
   operation_array = check_Array(operation_array,resultArray)
  
   # Delete old operation samples 
   if operation_array.shape[0] > 12 :
       operation_array = np.delete(operation_array,[0,1], axis = 0)
   
   
   """
    print("operation array_output")
    print(operation_array)
    print("copy array_output")
    print(operation_array_copy)
   """
   return operation_array       

# setting motor control pin in the Rc Car
# control PWM 100Khz JMOD-motordriver is okay!
def setPinConfig(ENable,INA,INB):
    GPIO.setup(ENable,GPIO.OUT)
    GPIO.setup(INA,GPIO.OUT)
    GPIO.setup(INB,GPIO.OUT)
    currentPWM = 0
    pwm = GPIO.PWM(ENable,100)
    pwm.start(currentPWM)
    return pwm

def movingRCcar(INA,INB): # this operation is same(Forward, Right, Left)
    GPIO.output(INA,HIGH)
    GPIO.output(INB,LOW)

def setMotorControl(INA,INB,last_pwm,DutyCycle,situation):
    #global PWM_Changeable    #revised1
    PWM_Changeable = False
        # FORWARD
    if situation == Forward:
        print("situation is forward")
        movingRCcar(INA,INB)
        PWM_Changeable = True
        # BACKWORD
    elif situation == Backword:
        print("situation is Backword")
        GPIO.output(INA,LOW)
        GPIO.output(INB,HIGH)
        PWM_Changeable = True
        # STOP
    elif situation == Stop:
        GPIO.output(INA,LOW)
        GPIO.output(INB,LOW)
        PWM_Changeable = True
        # Right
    elif situation == Right:
#         print("situation is Right")
        movingRCcar(INA,INB)
        PWM_Changeable = True
        # Left
    elif situation == Left:
#         print("situation is Left")
        movingRCcar(INA,INB)
        PWM_Changeable = True
        """
        # Break
        elif situation == Break:
            print("situation is Break")
            GPIO.output(INA,HIGH)
            GPIO.output(INB,HIGH
            PWM_Changeable = True           
        """
        # setting Changed dutyCycle
    if PWM_Changeable == True:
        last_pwm.ChangeDutyCycle(DutyCycle)
        last_pwm = DutyCycle

#==============================================================
# motor control function
# use Rapping for simplely code?
#=======================================================================
def setMotor(channel,pwm,DutyCycle,situation):
    #print("setMotor prameter",channel,pwm,DutyCycle,situation)
    
    if channel == MOTOR1:
        setMotorControl(motor1IN1,motor1IN2,pwm,DutyCycle,situation)
    elif channel == MOTOR2:
        setMotorControl(motor2IN1,motor2IN2,pwm,DutyCycle,situation)

# PID control prameter
Kp = 0.3
Kd = 0.001
ki = 0
time_prev = 0.0
error_prev = 0.0
#dt_sleep = 0.01
#tolerance = 0.01
error_prev = 0 # in static?
time_prev = 0
dt = 0.0        
           
def PID_control(error):
    global time_prev
    global error_prev
    """
    global Integral
     """
    global ki
    global Kd
    
    if(time_prev == 0.):
        time_prev = time.time()
    time_current = time.time()
    print("error",error)
    Pout = (Kp*error)
    print("Pout",Pout)
    dt = time_current-time_prev
    print("dt",dt)
    de = error - error_prev
    Derivative = de/dt
    Dout = ((Kd/1000 )* Derivative)
    """
    Integral += (error * delta_time)
    if Integral>10:
        Integral=10
    if Integral<-10:
        Integral=-10
    Iout=((Ki/10) * Integral)
    """
    time_prev = time_current
    error_prev = error
    radius = Pout +Dout #+Iout
    print("radius",radius)
    return radius