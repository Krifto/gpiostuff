
import time
import RPIO
import RPIO.PWM

RED = 23
GREEN = 25
BLUE = 4

colorNames = [RED, GREEN, BLUE]
class RGBStrip():

    def __init__(self):
        RPIO.cleanup()
        RPIO.setmode(RPIO.BCM)
        RPIO.setup(BLUE, RPIO.OUT)
        RPIO.setup(GREEN, RPIO.OUT) 
        RPIO.setup(RED, RPIO.OUT)
        RPIO.output(BLUE, False)
	RPIO.PWM.setup(100)
        for i in (0,1,2):
            RPIO.PWM.init_channel(i)
            RPIO.PWM.add_channel_pulse(i, colorNames[i], 0, 0)

        # Add some pulses to the subcycle
        #RPIO.PWM.add_channel_pulse(0, GREEN, 50, 50)
        #RPIO.PWM.add_channel_pulse(0, BLUE, 100, 50)
        #RPIO.PWM.add_channel_pulse(0, RED, 20, 30)

        self.count = 0
        self.green = 0
        self.red = 0
        self.blue = 0
        self.freq = 100
        #self.greenPWM=RPIO.PWM(25,self.freq)
        #self.greenPWM.start(10)
        #self.bluePWM=RPIO.PWM(4, self.freq)
        #self.bluePWM.start(50)
        #self.redPWM=RPIO.PWM(23,self.freq)
        #self.redPWM.start(10)

    def setColor(self, r, g, b):
        pass
        #self.redPWM.ChangeDutyCycle(self.red)
        #self.greenPWM.ChangeDutyCycle(self.green)
        #self.bluePWM.ChangeDutyCycle(self.blue)

    def __del__(self):
        RPIO.cleanup()
        #self.redPWM.stop()
        #self.bluePWM.stop()
        #self.greenPWM.stop()
   
    def socket_callback(self, socket, val):
        print("socket %s: '%s'" % (socket.fileno(), val))
        socket.send("echo: %s\n" % val)
        for index, colorString in enumerate(val.split()):
            try:
                color = int(colorString)
                RPIO.PWM.clear_channel_gpio(index, colorNames[index])
                RPIO.PWM.add_channel_pulse(index, colorNames[index], 0, color)
                #RPIO.PWM.init_channel(0, 20000+color)
            except ValueError:
                pass

            except Exception as e:
                error = "Unexpected error in socket callback: "+ str(e) +"\n"
                socket.send(error)
                print(error)


strip = RGBStrip()

#TCP socket server callback on port 8080
RPIO.add_tcp_callback(8080, strip.socket_callback)

try:
#    strip = RGBStrip()
#    while True:
#        time.sleep(1)
#
    # Blocking main epoll loop
    RPIO.wait_for_interrupts()
except KeyboardInterrupt:
    pass



print "\nExiting.\n"
#greenPWM.stop()
#redPWM.stop()
#bluePWM.stop()
#RPIO.cleanup()
