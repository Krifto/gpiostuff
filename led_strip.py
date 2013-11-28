
import time
import RPIO
import RPIO.PWM

RED = 23
GREEN = 25
BLUE = 4
colorPins = [RED, GREEN, BLUE]
dmaChannels = [0, 1, 3]

class RGBStrip():

    def __init__(self):
        RPIO.cleanup()
        RPIO.setmode(RPIO.BCM)
        RPIO.setup(BLUE, RPIO.OUT)
        RPIO.setup(GREEN, RPIO.OUT) 
        RPIO.setup(RED, RPIO.OUT)
        RPIO.output(BLUE, False)
	RPIO.PWM.setup()
        for index, colorPin in enumerate(colorPins):
            RPIO.PWM.init_channel(dmaChannels[index], 10000)
            RPIO.PWM.add_channel_pulse(dmaChannels[index], colorPin, 0, 0)


    def setColor(self, r, g, b):
        pass

    def __del__(self):
        for index in enumerate(colorPins):
            RPIO.PWM.clear_channel(dmaChannels[index])
        
        RPIO.cleanup()
   
    def socket_callback(self, socket, val):
        print("socket %s: '%s'" % (socket.fileno(), val))
        socket.send("echo: %s\n" % val)
        for index, colorString in enumerate(val.split()):
            try:
                color = int(colorString)
                RPIO.PWM.clear_channel_gpio(dmaChannels[index], colorPins[index])
                RPIO.PWM.add_channel_pulse(dmaChannels[index], colorPins[index], 0, color)
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
