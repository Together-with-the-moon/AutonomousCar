import RPi.GPIO as GPIO
from time import sleep
import sys
import copy
import numpy as np

#=====================================================================
# using JMOD-Motor-Drive
# this version is able to control to four motor unsing 4CH
#============================================================================

# define Motor LIST
MOTOR1 = 1
MOTOR2 = 2
MOTOR3 = 3
MOTOR4 = 4

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
ENC = 12
END = 18

#GPIO PIN
#motor1 : Front Left Motor (Stearing and moving)
motor1IN1 = 19
motor1IN2 = 13

#motor2: Rear Right Motor  (it is only Moving)
motor2IN1 = 6
motor2IN2 = 5

#motor3: Front Left Motor  (Stearing and moving)
motor3IN1 = 9
motor3IN2 = 10

#Motor4: Rear Rihgt Motor  (it is only Moving)
motor4IN1 = 22
motor4IN2 = 27

#Output PIN settings
HIGH = 1       # enable
LOW = 0        # disenable

#import other codes
#==============================================================
#operation_array = np.empty((12,3), dtype =int)
#error_data = np.empty((6,1),dtype = int)
#=======================================================================

#test data
error = np.array([0,15,40,-15,-40,-40,-40,-40,-40,-40,-40,15,-40,0])
#error = np.array([0,15,40,-15,-40])
#print(error)


# sinit operation arrays
operation_array = np.zeros((1,3), dtype =int)
Movement = 0

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
        print(operation_array)
#         print("init_array",operation_array)
    else:
        operation_array = np.concatenate((operation_array,resultArray),axis = 0)
        print("Concatenate array",operation_array)
        
        #slilcing movement in the total array
        MovementArray = operation_array[0:,1:2]

#         print("Movement",MovementArray)
        length = MovementArray.shape[0] #maybe changed?
#         print("length",length)
        mask = np.full((len(operation_array),1),MovementArray[0])
#        print("mask_setting",MovementArray[(mask== MovementArray)])
#        print(len(MovementArray[(mask== MovementArray)]))
        
        if length == len(MovementArray[(mask== MovementArray)]):
            dutycycle = medianOfduty(operation_array[0:,2:3])
            operation_array[0:2,length-1:length] = dutycycle
#     print("return",operation_array)
    
    return operation_array

#this function is very fool I will be change it
def copyArray(operation_array):
    #define motor3 and motor4 control parallel
    operation_array_copy = copy.deepcopy(operation_array)
    operation_array_copy[0::2,0:1] =MOTOR3
    operation_array_copy[1::2,0:1] =MOTOR4    
    return operation_array_copy

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
   if error == 0:
       print("forward setting")
       Movement = Forward
       DutyCycle1 = 100
       DutyCycle2 = 100
       
   # Define of RC Car Right opreation (mirco moving)
   elif (error > 0 and error <= 15):
       print("Right setting")
       Movement = Right
       DutyCycle1 = 30
       DutyCycle2 = 0
       
   # Define of RC Car Right opreation (normal moving)
   elif (error >15  and error <= 30):
       Movement = Right
       DutyCycle1 = 50
       DutyCycle2 = 0
   
   # Define of RC Car Right opreation (large moving) 
   elif (error >30):
        Movement = Right
        DutyCycle1 = 70 
        DutyCycle2 = 0
   
   # Define of RC Car Left opreation (mirco moving) 
   elif (error < 0 and error > -15):
        Movement = Left
        DutyCycle1 = 0
        DutyCycle2 = 30
        
   # Define of RC Car Left opreation (normal moving)      
   elif (error >15  and error <= 30):
        Movement = Left
        DutyCycle1 = 0
        DutyCycle2 = 50
   
   # Define of RC Car Left opreation (Large moving)  
   elif (error <-30):
        Movement = Left
        DutyCycle1 = 0
        DutyCycle2 = 70
        
        
   resultArray = np.array([MOTOR1,Movement,DutyCycle1,MOTOR2,Movement,DutyCycle2]).reshape(2,3)
#    print(resultArray)
   operation_array = check_Array(operation_array,resultArray)
  
   # Delete old operation samples 
   if operation_array.shape[0] > 12 :
       operation_array = np.delete(operation_array,[0,1], axis = 0)
   
   
 # copy of Rear of motor operation 
   operation_array_copy = copyArray(operation_array)
   
   """
    print("operation array_output")
    print(operation_array)
    print("copy array_output")
    print(operation_array_copy)
   """
   return operation_array#,operation_array_copy       

# setting motor control pin in the Rc Car
# control PWM 100Khz JMOD-motordriver is okay!
def setPinConfig(ENable,INA,INB):
    GPIO.setup(ENable,GPIO.OUT)
    GPIO.setup(INA,GPIO.OUT)
    GPIO.setup(INB,GPIO.OUT)
    currentPWM = 0
    pwm = GPIO.PWM(INB,100)
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
    elif channel == MOTOR3:
        setMotorControl(motor3IN1,motor3IN2,pwm,DutyCycle,situation)
    else:
        setMotorControl(motor4IN1,motor4IN2,pwm,DutyCycle,situation)

if __name__ == "__main__":
    # motor control pin setting
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    pwm1 = setPinConfig(ENA, motor1IN1, motor1IN2)
    pwm2 = setPinConfig(ENB, motor2IN1, motor2IN2)
    pwm3 = setPinConfig(ENC, motor3IN1, motor3IN2)
    pwm4 = setPinConfig(END, motor4IN1, motor4IN2)
    terminatePoint= True
    
    # define import package 
    # if you import this codes, activate this code
    
    
    #Motor Control Main_method
    while(terminatePoint):
        op9Postion(error,operation_array)
    #        print(error_i)
        """
        print("Parameter setting")
        print("motor move duty")
    #        print(operation_array_left)     
           #prameter setting
        """
        length = len(operation_array_left)
        
        LeftMotor_front = operation_array_left[length-2:length-1,0:1][0][0]
        RightMotor_front = operation_array_left[length-1:length,0:1][0][0]
        LeftMotor_rear = operation_array_left_right[length-2:length-1,0:1][0][0]
        RightMotor_rear = operation_array_left_right[length-1:length,0:1][0][0]
        DutyCycle1 = operation_array_left[length-2:length-1,1:2][0][0]
        DutyCycle2 = operation_array_left[length-1:length,1:2][0][0]
        Movement1 = operation_array_left[length-2:length-1,2:3][0][0]
        Movement2 = operation_array_left[length-1:length-0,2:3][0][0]
        
        """
        print("LeftMotor_front:",LeftMotor_front)
        print("RightMotor_front:",RightMotor_front)
        print("LeftMotor_rear:",LeftMotor_rear)
        print("RightMotor_rear:",RightMotor_rear)
        print("LeftMovement:",Movement)
        print("RightMovement:",Movement)
        """
        
        setMotor(LeftMotor_front,pwm1,DutyCycle1,Movement)
        sleep(0.003)
        setMotor(RightMotor_front,pwm2,DutyCycle2,Movement)
        sleep(0.00)
        setMotor(LeftMotor_rear,pwm3,DutyCycle1,Movement)
        sleep(0.002)
        setMotor(RightMotor_rear,pwm4,DutyCycle2,Movement)
        sleep(0.002) 
        
        """
        #STOP
        print("Stop init")
        setMotor(MOTOR1,pwm1,80,Stop)
        setMotor(MOTOR2,pwm2,80,Stop)
        sleep(2)    
        terminatePoint = False      
        """
        #END
        GPIO.cleanup()
        sys.exit()
