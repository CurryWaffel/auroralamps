#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Edited by: staticfloat.de
# Edit note: Extended the script by using an textfile to determine the current used function.
#
# Direct port of the Arduino NeoPixel library strandtest example. Showcases
# various animations on a strip of NeoPixels.

import time
import json
import numpy
import threading
import copy
from neopixel import *

# LED strip configuration:
LED_COUNT = 281 # Number of LED pixels.
LED_PIN = 18 # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN = 10 # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000 # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10 # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255 # Set to 0 for darkest and 255 for brightest
LED_INVERT = False # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0 # set to '1' for GPIOs 13, 19, 41, 45 or 53

settings = {}
befehlIterable = 0
dicty = {}

t2 = threading.Thread()
t3 = threading.Thread()

class StripMethods: # TODO Accurate timing (requires more calculating)
        # Define functions which animate LEDs in various ways.
        @staticmethod
        def colorWipe(args):
                if not args.has_key('lamps'):
                        args['lamps'] = [0,1,2,3,4,5,6]
                leds_to_use = get_leds_to_use(args['lamps'])

                """Wipe color across display a pixel at a time."""
                for i in range(len(leds_to_use)):
                        if not getattr(threading.currentThread(), "change", False):
                                strip.setPixelColor(leds_to_use[i], args["color"])
                                strip.show()
                                time.sleep(args["wait_ms"]/1000.0)
                        else: return

        @staticmethod
        def theaterChase(args):
                ct = threading.currentThread()

                if not args.has_key('lamps'):
                        args['lamps'] = [0,1,2,3,4,5,6]
                leds_to_use = get_leds_to_use(args['lamps'])

                """Movie theater light style chaser animation."""
                for j in range(args["iterations"]):
                        for q in range(3):
                                for i in range(0, len(leds_to_use), 3):
                                        if not getattr(ct, "change", False):
                                                strip.setPixelColor(leds_to_use[i-q], args["color"])
                                        else: return
                                strip.show()
                                time.sleep(args["wait_ms"]/1000.0)
                                for i in range(0, len(leds_to_use), 3):
                                        if not getattr(ct, "change", False):
                                                strip.setPixelColor(leds_to_use[i-q], 0)
                                        else: return

        @staticmethod
        def wheel(pos):
                """Generate rainbow colors across 0-255 positions."""
                if pos < 85:
                        return Color(pos * 3, 255 - pos * 3, 0)
                elif pos < 170:
                        pos -= 85
                        return Color(255 - pos * 3, 0, pos * 3)
                else:
                        pos -= 170
                        return Color(0, pos * 3, 255 - pos * 3)

        @staticmethod
        def setColor(args):
                if not args.has_key('lamps'):
                        args['lamps'] = [0,1,2,3,4,5,6]
                leds_to_use = get_leds_to_use(args['lamps'])

                for i in range(len(leds_to_use)):
                        if not getattr(threading.currentThread(), "change", False):
                                strip.setPixelColor(leds_to_use[i], args["color"])
                        else: return
                strip.show()
                        
        @staticmethod
        def rainbow(args):
                if not args.has_key('lamps'):
                        args['lamps'] = [0,1,2,3,4,5,6]
                leds_to_use = get_leds_to_use(args['lamps'])

                """Draw rainbow that fades across all pixels at once."""
                for j in range(256):
                        for i in range(len(leds_to_use)):
                                if not getattr(threading.currentThread(), "change", False):
                                        strip.setPixelColor(leds_to_use[i], StripMethods.wheel((i+j) & 255))
                                else: return
                        strip.show()
                        time.sleep(args['wait_ms']/1000.0)

        @staticmethod
        def rainbowStationary(args):
                if not args.has_key('lamps'):
                        args['lamps'] = [0,1,2,3,4,5,6]
                leds_to_use = get_leds_to_use(args['lamps'])

                """Draw rainbow that fades across all pixels at once."""
                for j in range(256):
                        for i in range(len(leds_to_use)):
                                if not getattr(threading.currentThread(), "change", False):
                                        strip.setPixelColor(leds_to_use[i], StripMethods.wheel(j & 255))
                                else: return
                        strip.show()
                        time.sleep(args["wait_ms"]/1000.0)

        @staticmethod
        def rainbowCycle(args): #TODO implent
                if not args.has_key('lamps'):
                        args['lamps'] = [0,1,2,3,4,5,6]
                leds_to_use = get_leds_to_use(args['lamps'])

                """Draw rainbow that uniformly distributes itself across all pixels."""
                for j in range(256*args["iterations"]):
                        for i in range(len(leds_to_use)):
                                if not getattr(threading.currentThread(), "change", False):
                                        strip.setPixelColor(i, StripMethods.wheel(((i * 256 // len(leds_to_use)) + j) & 255))
                                else: return
                        strip.show()
                        time.sleep(args["wait_ms"]/1000.0)

        @staticmethod
        def theaterChaseRainbow(args):
                ct = threading.currentThread()

                if not args.has_key('lamps'):
                        args['lamps'] = [0,1,2,3,4,5,6]
                leds_to_use = get_leds_to_use(args['lamps'])

                """Rainbow movie theater light style chaser animation."""
                for j in range(256):
                        for q in range(3):
                                for i in range(0, len(leds_to_use), 3):
                                        if not getattr(ct, "change", False):
                                                strip.setPixelColor(leds_to_use[i-q], StripMethods.wheel((i+j) % 255))
                                        else:
                                                return
                                strip.show()
                                time.sleep(args["wait_ms"]/1000.0)
                                for i in range(0, len(leds_to_use), 3):
                                        if not getattr(ct, "change", False):
                                                strip.setPixelColor(leds_to_use[i-q], 0)
                                        else:
                                                return
        
        @staticmethod
        def interpolate(args):
                ct = threading.currentThread()

                """Interpolation between two colors"""

                StripMethods.setColor(args) # Show first color

                if not args.has_key('lamps'):
                        args['lamps'] = [0,1,2,3,4,5,6]
                leds_to_use = get_leds_to_use(args['lamps'])

                # Parse both colors to array
                parsedcol = parseColor(args["color"])
                parsedcol2 = parseColor(args["color2"])
                coldiff = [parsedcol2[0] - parsedcol[0], parsedcol2[1] - parsedcol[1], parsedcol2[2] - parsedcol[2]]

                now = int(round(time.time() * 1000))
                milli_sec = now + args["duration_ms"]
                diff = milli_sec - now

                while (diff > 0):
                        factor = (float(1)/float(args["duration_ms"])) * float(args["duration_ms"] - diff)

                        coltorender = Color(int(round(float(coldiff[1])*factor + parsedcol[1])),
                                int(round(float(coldiff[0])*factor + parsedcol[0])),
                                int(round(float(coldiff[2])*factor + parsedcol[2])))

                        for i in range(len(leds_to_use)):
                                if not getattr(ct, "change", False):
                                        strip.setPixelColor(leds_to_use[i], coltorender)
                                else:
                                        return
                        strip.show()

                        now = int(round(time.time() * 1000))
                        diff = milli_sec - now
                
                if args['goback']:
                        now = int(round(time.time() * 1000))
                        milli_sec = now + args["duration_ms"]
                        diff = milli_sec - now
                        
                        while (diff > 0):
                                factor = (float(1)/float(args["duration_ms"])) * float(args['duration_ms'] - diff)

                                coltorender = Color(int(round(float(-coldiff[1])*factor + parsedcol2[1])),
                                        int(round(float(-coldiff[0])*factor + parsedcol2[0])),
                                        int(round(float(-coldiff[2])*factor + parsedcol2[2])))

                                for i in range(len(leds_to_use)):
                                        if not getattr(ct, "change", False):
                                                strip.setPixelColor(leds_to_use[i], coltorender)
                                        else:
                                                return
                                strip.show()

                                now = int(round(time.time() * 1000))
                                diff = milli_sec - now
        
        @staticmethod
        def wait(args):
                ct = threading.currentThread()
                
                now = int(round(time.time()*1000))
                milli_sec = now + args['duration_ms']
                diff = milli_sec - now

                while(diff > 0):
                        if not getattr(ct, "change", False):
                                time.sleep(0.01)
                        else:
                                return
                        
                        now = int(round(time.time() * 1000))
                        diff = milli_sec - now

def parseColor(color):
        stri = "{0:b}".format(color)

        for i in range(24 - len(stri)):
                stri = "0" + stri

        return [int(stri[8:16], 2), int(stri[0:8], 2), int(stri[16:24], 2)]

def get_leds_to_use(lamps):
        a = []
        for i, e in enumerate(settings['led_config']):
                if i in lamps:
                        a = numpy.concatenate((a, e))

        a = a.astype(int)
        return a
def load_led_config():
        led_config = []
        part = []
        for i in range(0, 33): #1-1
                part.append(i)
        for i in range(275, 281): #1-2
                part.append(i)
        led_config.append(part)
        part = []
        for i in range(33, 67): #2-1
                part.append(i)
        for i in range(228, 234): #2-2
                part.append(i)
        led_config.append(part)
        part = []
        for i in range(234, 275): #3
                part.append(i)
        led_config.append(part)
        part = []
        for i in range(67, 87): #4-1
                part.append(i)
        for i in range(208, 228): #4-2
                part.append(i)
        led_config.append(part)
        part = []
        for i in range(87, 121): #5-1
                part.append(i)
        for i in range(202, 208): #5-2
                part.append(i)
        led_config.append(part)
        part = []
        for i in range(162, 202): #6
                part.append(i)
        led_config.append(part)
        part = []
        for i in range(121, 162): #7
                part.append(i)
        led_config.append(part)
        return led_config

def requestLoop():
        while True:
                global dicty
                global befehlIterable
                global t2
                
                f = open("/var/www/html/led-server/change.txt", "r")

                try:
                        change = json.load(f)['change']
                except ValueError:
                        change = 0
                f.close()

                if change:
                        #print("---------------------------------------------------------------------------------------------------------------------")
                        
                        f = open("/var/www/html/led-server/befehl.txt", "r")
                        dicty = json.load(f)
                        f.close()

                        t2.change = True

                        if dicty[0][0]['command'] == "terminate":
                                return

                        f = open("/var/www/html/led-server/change.txt", "w")
                        json.dump({'change':0}, f)
                        f.close()

                        befehlIterable = 0
                        
                        t2 = threading.Thread(target=listloop, args=tuple([dicty[0]]))
                        t2.daemon = True
                        t2.start()
def listloop(dictynum):
        befehlIter = 0
        #print("::::::::::::::::::::::::::::::::::::::::::::")
        #print("Would do first column now!")
        #print(dictynum)
        #print("::::::::::::::::::::::::::::::::::::::::::::")

        
        t4 = threading.Thread()
        t5 = threading.Thread()

        finished = False

        while not getattr(threading.currentThread(), "change", False):
                if not t4.isAlive():
                        if finished:
                                break
                        if dictynum[befehlIter]['command'] == "split":
                                t5 = threading.Thread(target=listloop, args=tuple([dicty[dictynum[befehlIter]['args']['newList']]]))
                                t5.loop = dictynum[befehlIter]['args']['looplist']
                                t5.daemon = True
                                t5.start()
                        elif dictynum[befehlIter]['command'] == "join":
                                if not dictynum[befehlIter]['args']['waitlist']:
                                        t5.change = True
                                elif t5.loop:
                                        t5.finsignal = True
                                t5.join()
                        else:
                                t4 = threading.Thread(target=getattr(StripMethods, dictynum[befehlIter]['command']), args=tuple([dictynum[befehlIter]['args']]))
                                t4.daemon = True
                                t4.start()
                        
                        befehlIter += 1
                        
                        if befehlIter >= len(dictynum):
                                if getattr(threading.currentThread(), "loop", True) and not getattr(threading.currentThread(), "finsignal", False):
                                        befehlIter = 0
                                else:
                                        finished = True

        t4.change = True
        t5.change = True
                
        print("Active Threads: " + str(threading.activeCount()))
        
        return
def brightnessLoop():
        try:
                isAlive = False
                while True:
                        global befehlIterable
                        global t3

                        if getattr(threading.currentThread(), "terminate", False): return
                        
                        f = open("/var/www/html/led-server/setting_change.txt", "r")
                        try:
                                change = json.load(f)['change']
                        except ValueError:
                                change = 0
                        f.close()
                        
                        if change:
                                t3.change = True
                                isAlive = False

                                f = open("/var/www/html/led-server/setting.txt", "r")
                                try: dicti = json.load(f)
                                except ValueError: dicti = {}
                                f.close()

                                f = open("/var/www/html/led-server/setting_change.txt", "w")
                                json.dump({'change':0}, f)
                                f.close()

                                if dicti.has_key("brightness"):
                                        strip.setBrightness(int(dicti["brightness"]))
                                        settings['brightness'] = int(dicti["brightness"])
                                if dicti.has_key("led_count"):
                                        settings['led_count'] = int(dicti["led_count"])

                                f = open("/var/www/html/led-server/settings.txt", "w")
                                f.write(json.dumps(settings))
                                f.close()
                        
                        

        except KeyboardInterrupt:
                print("Terminating programm")

# Main program logic follows:
if __name__ == '__main__':
        f = open("/var/www/html/led-server/change.txt", "w")
        json.dump({'change':1}, f)
        f.close()

        f = open("/var/www/html/led-server/setting_change.txt", "w")
        json.dump({'change':1}, f)
        f.close()

        f = open("/var/www/html/led-server/settings.txt", "r")
        settings = json.loads(f.read())
        f.close()

        settings['led_config'] = load_led_config()
        
        ##################################################################################################################################################################

        # Create NeoPixel object with appropriate configuration.
        strip = Adafruit_NeoPixel(settings.get('led_count', LED_COUNT), LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, settings.get('brightness', LED_BRIGHTNESS), LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        strip.begin()

        print('Becca said hi!')

        t = threading.Thread(target=requestLoop)
        t.start()
        t1 = threading.Thread(target=brightnessLoop)
        t1.start()
        t.join()
        t1.terminate = True
        
        f = open("/var/www/html/led-server/befehl.txt", "w")
        f.write('[[{"command":"rainbow","args":{"wait_ms":0}}]]')
        f.close()

        f = open("/var/www/html/led-server/change.txt", "w")
        json.dump({'change':1}, f)
        f.close()

        """
        f = open("/var/www/html/led-server/setting.txt", "w")
        json.dump({"brightness":50}, f)
        f.close()

        f = open("/var/www/html/led-server/setting_change.txt", "w")
        json.dump({'change':1}, f)
        f.close()
        """

        print("EndofProgramm!")
