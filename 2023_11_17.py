import pygame
import math
import RPi.GPIO as GPIO




def map_axis(val):
    val = round(val, 2)
    in_min = -1
    in_max = 1
    out_min = -100
    out_max = 100
    return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def ivent_check():
    joystick_data = {
        "joy_lx": map_axis(joystick.get_axis(0)),
        "joy_ly": map_axis(joystick.get_axis(1)),
        #"joy_rx": map_axis(joystick.get_axis(3)),
        #"joy_ry": map_axis(joystick.get_axis(4)),
    }
    print(joystick_data)
    return joystick_data

def ang_calc(data):
    radian = math.atan2(data["joy_lx"], data["joy_ly"])
    degree = radian * (180 / math.pi)
    print(degree)
    return degree


GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
GPIO.setup(13, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
#GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#l
GPIO.output(13, GPIO.LOW)
GPIO.output(11, GPIO.HIGH)
#r
GPIO.output(5, GPIO.HIGH)
GPIO.output(7, GPIO.LOW)
#c
GPIO.output(10, GPIO.LOW)
GPIO.output(12, GPIO.HIGH)

#PWMセットアップ
c = GPIO.PWM(8, 50)
r = GPIO.PWM(3, 50)
l = GPIO.PWM(15, 50)

r.start(0)
l.start(0)
c.start(0)

while True:
    if pygame.event.get():
        jd = ivent_check()
        deg = ang_calc(jd)
        if deg == 0 and jd["joy_ly"] == 0.0:
            print("停止")
            GPIO.output(13, GPIO.LOW)
            GPIO.output(11, GPIO.LOW)
            GPIO.output(5, GPIO.LOW)
            GPIO.output(7, GPIO.LOW)
            GPIO.output(10, GPIO.LOW)
            GPIO.output(12, GPIO.LOW)
            r.ChangeDutyCycle(0)
            l.ChangeDutyCycle(0)
            c.ChangeDutyCycle(0)
        elif deg == 180:
            print("前進")
            GPIO.output(13, GPIO.LOW)
            GPIO.output(11, GPIO.LOW)
            GPIO.output(5, GPIO.LOW)
            GPIO.output(7, GPIO.LOW)
            GPIO.output(10, GPIO.LOW)
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(5, GPIO.HIGH)
            GPIO.output(7, GPIO.LOW)
            r.ChangeDutyCycle(80)
            l.ChangeDutyCycle(80)
            c.ChangeDutyCycle(0)
        elif deg == 0:
            print("後退")
            GPIO.output(13, GPIO.LOW)
            GPIO.output(11, GPIO.LOW)
            GPIO.output(5, GPIO.LOW)
            GPIO.output(7, GPIO.LOW)
            GPIO.output(10, GPIO.LOW)
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(11, GPIO.LOW)
            GPIO.output(5, GPIO.LOW)
            GPIO.output(7, GPIO.HIGH)
            r.ChangeDutyCycle(80)
            l.ChangeDutyCycle(80)
            c.ChangeDutyCycle(0)
        #elif deg == 45:
            #print("右斜め後ろ")
        #elif deg == -45:
            #print("左斜め後ろ")
        elif deg == 90:
            print("右")
            GPIO.output(13, GPIO.LOW)
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(5, GPIO.LOW)
            GPIO.output(7, GPIO.HIGH)
            GPIO.output(10, GPIO.HIGH)
            GPIO.output(12, GPIO.LOW)
            r.ChangeDutyCycle(50)
            l.ChangeDutyCycle(50)
            c.ChangeDutyCycle(100)
        elif deg == -90:
            print("左")
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(11, GPIO.LOW)
            GPIO.output(5, GPIO.HIGH)
            GPIO.output(7, GPIO.LOW)
            GPIO.output(10, GPIO.LOW)
            GPIO.output(12, GPIO.HIGH)
            r.ChangeDutyCycle(50)
            l.ChangeDutyCycle(50)
            c.ChangeDutyCycle(100)
        #elif deg == 135:
            #print("右斜め前")
        elif deg == -135:
            print("左斜め前")
            GPIO.output(13, GPIO.LOW)
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(5, GPIO.HIGH)
            GPIO.output(7, GPIO.LOW)
            GPIO.output(10, GPIO.LOW)
            GPIO.output(12, GPIO.HIGH)
            r.ChangeDutyCycle(18.5)
            l.ChangeDutyCycle(68.5)
            c.ChangeDutyCycle(50)


class GPIOset:
    
    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        self.mode = [GPIO.IN, GPIO.OUT]
        self.on_off = [GPIO.LOW, GPIO.HIGH]
    
    def writeData(self, data, ch):
        GPIO.setup(ch, self.mode[data])
    
    #def IventRegistration(self, ch):
    #    GPIO.add_event_detect(ch, GPIO.RISING, callback=Motor_encode.callback)

    def on_offSet(self, ch, num):
        GPIO.output(ch, self.on_off[num])
    
    def pwmSet(self, ch, pwm_value):
        p_name = GPIO.PWM(ch, pwm_value)
        return p_name
    
    def dutySet(self, pwm, num):
        pwm.ChangeDutyCycle(num)

