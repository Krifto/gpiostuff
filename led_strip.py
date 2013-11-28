
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


    def setColor(self, r, g, b):
        pass

    def __del__(self):
        RPIO.cleanup()
   
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
    RPIO.wait_for_interrupts()
except KeyboardInterrupt:
    pass



print "\nExiting.\n"
