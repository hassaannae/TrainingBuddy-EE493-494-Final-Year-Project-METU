import time
import RPi.GPIO as GPIO
import random
import threading
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

topmotor = GPIO.PWM(7, 50)
bottommotor = GPIO.PWM(12, 50)
feeder = GPIO.PWM(32, 50)
horizontalservo = GPIO.PWM(18, 50)
verticalservo = GPIO.PWM(37, 50)



#CONSTANTS
CCW_SLOW = 7.1
CCW_MEDIUM = 7.15
CCW_FAST = 7.2
CW_SLOW = 7.1
CW_MEDIUM = 7.15
CW_FAST = 7.2

CCW_SLIGHT = 7.1
CCW_HEAVY = 7.2
CW_SLIGHT = 7.1
CW_HEAVY = 7.2
SKEW = 0.1 # |CW_SLIGHT/HEAVY - SKEW| < 3

LEFT = 6
MID = 8
RIGHT = 10
UP = 9
DOWN = 7.5

STOP = 3
FirstServe = 5
SecondServe = 8
ThirdServe = 12


class PingPongLauncher:
    def __init__(self):
        self.launch_angle = "mid"
        self.spin_style = "no spin"
        self.serve_freq = "medium"
        self.ball_speed = "medium"
        self.power_on = False
        self.mode = "repetition"

    def set_launch_angle(self, angle):
        self.launch_angle = angle

        # control the motor to change the angle, only if power is on
        if self.power_on:
            if angle == "left":
                horizontalservo.ChangeDutyCycle(LEFT)
                pass
            elif angle == "mid":
                horizontalservo.ChangeDutyCycle(MID)
                pass
            elif angle == "right":
                horizontalservo.ChangeDutyCycle(RIGHT)
                pass

    def set_spin_style(self, style):
        # update the spin style
        self.spin_style = style

        # control the motor to change the spin style, only if power is on
        if self.power_on:
            if style == "no spin":
                topmotor.ChangeDutyCycle(CCW_MEDIUM)
                bottommotor.ChangeDutyCycle(CW_MEDIUM)
                print("no spin")
                pass
            elif style == "slight topspin":
                topmotor.ChangeDutyCycle(CCW_SLIGHT)
                bottommotor.ChangeDutyCycle(CCW_SLIGHT)
                print("slight topspin")
                pass
            elif style == "heavy topspin":
                topmotor.ChangeDutyCycle(CCW_HEAVY)
                bottommotor.ChangeDutyCycle(CCW_HEAVY)
                pass
            elif style == "slight backspin":
                topmotor.ChangeDutyCycle(CW_SLIGHT)
                bottommotor.ChangeDutyCycle(CW_SLIGHT)
                pass
            elif style == "heavy backspin":
                topmotor.ChangeDutyCycle(CW_HEAVY)
                bottommotor.ChangeDutyCycle(CW_HEAVY)
                pass

    def set_serve_freq(self, freq):
        # update the serve freq
        self.serve_freq = freq

        # control the motor to change the serve freq, only if power is on
        if self.power_on:
            if freq == "slow":
                while True:
                    feeder.ChangeDutyCycle(5)
                    time.sleep(2)
                    print("slow serve freq (feeder running in parallel)")
                    feeder.ChangeDutyCycle(7)
                    time.sleep(2)
                    if self.serve_freq != "slow":
                        break
                pass
            elif freq == "medium":
                while True:
                    feeder.ChangeDutyCycle(5)
                    time.sleep(1)
                    print("medium serve freq (feeder running in parallel)")
                    feeder.ChangeDutyCycle(7)
                    time.sleep(1)
                    if self.serve_freq != "medium":
                        break
                pass
            elif freq == "fast":
                while True:
                    feeder.ChangeDutyCycle(5)
                    time.sleep(0.5)
                    feeder.ChangeDutyCycle(7)
                    time.sleep(0.5)
                    if self.serve_freq != "fast":
                        break
                pass
            elif freq == "stop":
                feeder.ChangeDutyCycle(STOP)
                print("stopping feeder")
                pass

    def set_ball_speed(self, speed):
        # update the ball speed
        self.ball_speed = speed

        # control the motor to change the spin style, only if power is on
        if self.power_on:
            if self.spin_style == "no spin":
                if speed == "slow":
                    topmotor.ChangeDutyCycle(CCW_SLOW)
                    bottommotor.ChangeDutyCycle(CW_SLOW)
                    pass
                elif speed == "medium":
                    topmotor.ChangeDutyCycle(CCW_MEDIUM)
                    bottommotor.ChangeDutyCycle(CW_MEDIUM)
                    pass
                elif speed == "fast":
                    topmotor.ChangeDutyCycle(CCW_FAST)
                    bottommotor.ChangeDutyCycle(CW_FAST)
                    pass

            if self.spin_style == "slight topspin":
                if speed == "slow":
                    topmotor.ChangeDutyCycle(CCW_SLIGHT - SKEW)
                    bottommotor.ChangeDutyCycle(CCW_SLIGHT - SKEW)
                    pass
                elif speed == "medium":
                    topmotor.ChangeDutyCycle(CCW_SLIGHT)
                    bottommotor.ChangeDutyCycle(CCW_SLIGHT)
                    pass
                elif speed == "fast":
                    topmotor.ChangeDutyCycle(CCW_SLIGHT + SKEW)
                    bottommotor.ChangeDutyCycle(CCW_SLIGHT + SKEW)
                    pass
            if self.spin_style == "heavy topspin":
                if speed == "slow":
                    topmotor.ChangeDutyCycle(CCW_HEAVY - SKEW)
                    bottommotor.ChangeDutyCycle(CCW_HEAVY - SKEW)
                    pass
                elif speed == "medium":
                    topmotor.ChangeDutyCycle(CCW_HEAVY)
                    bottommotor.ChangeDutyCycle(CCW_HEAVY)
                    pass
                elif speed == "fast":
                    topmotor.ChangeDutyCycle(CCW_HEAVY + SKEW)
                    bottommotor.ChangeDutyCycle(CCW_HEAVY + SKEW)
                    pass


            if self.spin_style == "slight backspin":
                if speed == "slow":
                    topmotor.ChangeDutyCycle(CW_SLIGHT + SKEW)
                    bottommotor.ChangeDutyCycle(CW_SLIGHT + SKEW)
                    pass
                elif speed == "medium":
                    topmotor.ChangeDutyCycle(CW_SLIGHT)
                    bottommotor.ChangeDutyCycle(CW_SLIGHT)
                    pass
                elif speed == "fast":
                    topmotor.ChangeDutyCycle(CW_SLIGHT - SKEW)
                    bottommotor.ChangeDutyCycle(CW_SLIGHT - SKEW)
                    pass
            if self.spin_style == "heavy backspin":
                if speed == "slow":
                    topmotor.ChangeDutyCycle(CW_HEAVY + SKEW)
                    bottommotor.ChangeDutyCycle(CW_HEAVY + SKEW)
                    pass
                elif speed == "medium":
                    topmotor.ChangeDutyCycle(CW_SLIGHT)
                    bottommotor.ChangeDutyCycle(CW_HEAVY)
                    pass
                elif speed == "fast":
                    topmotor.ChangeDutyCycle(CW_SLIGHT - SKEW)
                    bottommotor.ChangeDutyCycle(CW_HEAVY - SKEW)
                    pass

    def set_mode(self, Mode):
        # update the mode
        self.mode = Mode

    def thread(self):
        # create a new thread for the set_serve_freq function
        t = threading.Thread(target=self.set_serve_freq, args=(self.serve_freq,))
        # start the thread
        t.start()

    def Sequence(self, s1s, s1a, s2s, s2a, s3s, s3a):
        self.serve_freq="stop"
        self.thread()
        feeder.ChangeDutyCycle(STOP)

        if self.power_on:
            self.set_spin_style(s1s)
            self.set_launch_angle(s1a)
            feeder.ChangeDutyCycle(FirstServe)
            time.sleep(5)

            self.set_spin_style(s2s)
            self.set_launch_angle(s2a)
            feeder.ChangeDutyCycle(SecondServe)
            time.sleep(5)

            self.set_spin_style(s3s)
            self.set_launch_angle(s3a)
            feeder.ChangeDutyCycle(ThirdServe)
            time.sleep(5)

    def SequenceRandom(self, s1s, s1a, s2s, s2a, s3s, s3a):
        self.serve_freq="stop"
        self.thread()
        feeder.ChangeDutyCycle(STOP)
        speed_options = ['slow','medium','fast']
        Rspeed = random.choice(speed_options)

        if self.power_on:
            self.set_spin_style(s1s)
            self.set_launch_angle(s1a)
            self.set_ball_speed(Rspeed)
            feeder.ChangeDutyCycle(FirstServe)
            time.sleep(5)

            self.set_spin_style(s2s)
            self.set_launch_angle(s2a)
            self.set_ball_speed(Rspeed)
            feeder.ChangeDutyCycle(SecondServe)
            time.sleep(5)

            self.set_spin_style(s3s)
            self.set_launch_angle(s3a)
            self.set_ball_speed(Rspeed)
            feeder.ChangeDutyCycle(ThirdServe)
            time.sleep(5)
    


    def turn_on(self):
        self.power_on = True
        # code to turn on the launcher
        topmotor.start(0)
        bottommotor.start(0)
        verticalservo.start(0)
        horizontalservo.start(0)
        feeder.start(0)
        print("starting 0")
        time.sleep(3)

        topmotor.ChangeDutyCycle(3)
        bottommotor.ChangeDutyCycle(3)
        verticalservo.ChangeDutyCycle(DOWN)
        horizontalservo.ChangeDutyCycle(MID)
        feeder.ChangeDutyCycle(3)
        print("start")
        time.sleep(5)
        

    def turn_off(self):
        self.power_on = False
        # code to turn off the launcher
        self.serve_freq="stop"
        self.thread()
        print("stopping")
        topmotor.stop()
        bottommotor.stop()
        verticalservo.stop()
        horizontalservo.stop()
        feeder.stop()

    def randomlaunch(self, spinstyle):
        if spinstyle == "no spin":
            swing_options = "no spin"
        else:
            swing_options = ['slight ' + spinstyle, 'heavy ' + spinstyle]
        angle_options = ['left','mid','right']
        speed_options = ['slow','medium','fast']
        serve_options = ['slow','medium','fast']

        Rswing = random.choice(swing_options)
        Rangle = random.choice(angle_options)
        Rspeed = random.choice(speed_options)
        Rserve = random.choice(serve_options)
        
        if self.power_on:
            self.set_spin_style(Rswing)
            self.set_launch_angle(Rangle)
            self.set_ball_speed(Rspeed)
            self.serve_freq = Rserve
            self.thread()

# Example usage:
print("this is from MotorControlRaw")
##launcher = PingPongLauncher()
##launcher.set_spin_style("no spin")
##launcher.thread()
##launcher.set_spin_style("no spin")
##time.sleep(10)
##launcher.set_spin_style("no spin")
##launcher.serve_freq="slow"
##launcher.thread()
##time.sleep(10)
##launcher.set_spin_style("no spin")
##launcher.turn_off()




