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
import argparse
import inspect

# LED strip configuration:
LED_COUNT = 281 # Number of LED pixels.
LED_PIN = 18 # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN = 10 # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000 # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10 # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255 # Set to 0 for darkest and 255 for brightest
LED_INVERT = False # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0 # set to '1' for GPIOs 13, 19, 41, 45 or 53

LEDS = []
settings = {}
befehlIterable = 0
lastBefehle = []
lastArgss = []
lastParsed = []
isParsed = False # TODO Implement check for parses with Array to reduce cpu usage on the long run

t2 = threading.Thread()
t3 = threading.Thread()

class StripMethods: # TODO Accurate timing (requires more calculating)
        # Define functions which animate LEDs in various ways.
        @staticmethod
        def colorWipe(strip, color, wait_ms=50):
                ct = threading.currentThread()

                global lastParsed
                global isParsed
                parsedArgs = []
                if (isParsed):
                        parsedArgs = lastParsed
                else:
                        parsedArgs = parseArguments([color, wait_ms], [Color, int], ["color", "wait_ms"])
                        lastParsed = parsedArgs
                        isParsed = True

                """Wipe color across display a pixel at a time."""
                for i in range(strip.numPixels()):
                        if not getattr(ct, "change", False):
                                strip.setPixelColor(LEDS[i], parsedArgs["color"])
                                strip.show()
                                time.sleep(parsedArgs["wait_ms"]/1000.0)
                        else:
                                #print("Applying change now...")
                                return

        @staticmethod
        def theaterChase(strip, color, wait_ms=50, iterations=10):
                ct = threading.currentThread()

                global lastParsed
                global isParsed
                parsedArgs = []
                if (isParsed):
                        parsedArgs = lastParsed
                else:
                        parsedArgs = parseArguments([color, wait_ms, iterations], [Color, int, int], ["color", "wait_ms", "iterations"])
                        lastParsed = parsedArgs
                        isParsed = True

                """Movie theater light style chaser animation."""
                for j in range(parsedArgs["iterations"]):
                        for q in range(3):
                                for i in range(0, strip.numPixels(), 3):
                                        if not getattr(ct, "change", False):
                                                strip.setPixelColor(i+q, parsedArgs["color"])
                                        else:
                                                #print("Applying change now...")
                                                return
                                strip.show()
                                time.sleep(parsedArgs["wait_ms"]/1000.0)
                                for i in range(0, strip.numPixels(), 3):
                                        if not getattr(ct, "change", False):
                                                strip.setPixelColor(i+q, 0)
                                        else:
                                                #print("Applying change now...")
                                                return

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
        def setColor(strip, color):
                ct = threading.currentThread()

                global lastParsed
                global isParsed
                parsedArgs = []
                if (isParsed):
                        parsedArgs = lastParsed
                else:
                        parsedArgs = parseArguments([color], [Color], ["color"])
                        lastParsed = parsedArgs
                        isParsed = True

                for i in range(strip.numPixels()):
                        if not getattr(ct, "change", False):
                                strip.setPixelColor(i, parsedArgs["color"])
                        else:
                                #print("Applying change now...")
                                return
                strip.show()
                        
        @staticmethod
        def rainbow(strip, wait_ms=1, iterations=1):
                ct = threading.currentThread()

                global lastParsed
                global isParsed
                parsedArgs = []
                if (isParsed):
                        parsedArgs = lastParsed
                else:
                        parsedArgs = parseArguments([wait_ms, iterations], [int, int], ["wait_ms", "iterations"])
                        lastParsed = parsedArgs
                        isParsed = True

                """Draw rainbow that fades across all pixels at once."""
                for j in range(256*parsedArgs["iterations"]):
                        #print("Bruh")
                        for i in range(strip.numPixels()):
                                if not getattr(ct, "change", False):
                                        #print("Setting Pixel #" + str(i))
                                        strip.setPixelColor(LEDS[i], StripMethods.wheel((i+j) & 255))
                                else:
                                        #print("Applying change now...")
                                        return
                        #print("This that")
                        strip.show()
                        #print("After show")
                        time.sleep(parsedArgs["wait_ms"]/1000.0)
                        #print("After wait")

        @staticmethod
        def rainbowStationary(strip, wait_ms=1, iterations=1):
                ct = threading.currentThread()

                global lastParsed
                global isParsed
                parsedArgs = []
                if (isParsed):
                        parsedArgs = lastParsed
                else:
                        parsedArgs = parseArguments([wait_ms, iterations], [int, int], ["wait_ms", "iterations"])
                        lastParsed = parsedArgs
                        isParsed = True

                """Draw rainbow that fades across all pixels at once."""
                for j in range(256*parsedArgs["iterations"]):
                        #print("Bruh")
                        for i in range(strip.numPixels()):
                                if not getattr(ct, "change", False):
                                        #print("Setting Pixel #" + str(i))
                                        strip.setPixelColor(i, StripMethods.wheel(j & 255))
                                else:
                                        #print("Applying change now...")
                                        return
                        strip.show()
                        time.sleep(parsedArgs["wait_ms"]/1000.0)

        @staticmethod
        def rainbowCycle(strip, wait_ms=20, iterations=5): #TODO Apply Change

                global lastParsed
                global isParsed
                parsedArgs = []
                if (isParsed):
                        parsedArgs = lastParsed
                else:
                        parsedArgs = parseArguments([wait_ms, iterations], [int, int], ["wait_ms", "iterations"])
                        lastParsed = parsedArgs
                        isParsed = True

                """Draw rainbow that uniformly distributes itself across all pixels."""
                for j in range(256*parsedArgs["iterations"]):
                        for i in range(strip.numPixels()):
                                strip.setPixelColor(i, StripMethods.wheel(((i * 256 // strip.numPixels()) + j) & 255))
                        strip.show()
                        time.sleep(parsedArgs["wait_ms"]/1000.0)

        @staticmethod
        def theaterChaseRainbow(strip, wait_ms=50):
                ct = threading.currentThread()
                global lastParsed
                global isParsed
                parsedArgs = []
                if (isParsed):
                        parsedArgs = lastParsed
                else:
                        parsedArgs = parseArguments([wait_ms], [int], ["wait_ms"])
                        lastParsed = parsedArgs
                        isParsed = True

                """Rainbow movie theater light style chaser animation."""
                for j in range(256):
                        for q in range(3):
                                for i in range(0, strip.numPixels(), 3):
                                        if not getattr(ct, "change", False):
                                                strip.setPixelColor(LEDS[i+q], StripMethods.wheel((i+j) % 255))
                                        else:
                                                return
                                strip.show()
                                time.sleep(parsedArgs["wait_ms"]/1000.0)
                                for i in range(0, strip.numPixels(), 3):
                                        if not getattr(ct, "change", False):
                                                strip.setPixelColor(LEDS[i+q], 0)
                                        else:
                                                return
        
        @staticmethod
        def interpolate(strip, color, color2, duration_ms):
                ct = threading.currentThread()
                global lastParsed
                global isParsed
                parsedArgs = []
                if (isParsed):
                        parsedArgs = lastParsed
                else:
                        parsedArgs = parseArguments([color, color2, duration_ms], [Color, Color, int], ["color", "color2", "duration_ms"])
                        lastParsed = parsedArgs
                        isParsed = True

                """Interpolation between two colors"""

                StripMethods.setColor(strip, parsedArgs["color"]) # Show first color

                # Parse both colors to array
                parsedcol = parseColor(parsedArgs["color"])
                parsedcol2 = parseColor(parsedArgs["color2"])
                coldiff = [parsedcol2[0] - parsedcol[0], parsedcol2[1] - parsedcol[1], parsedcol2[2] - parsedcol[2]]

                now = int(round(time.time() * 1000))
                milli_sec = now + parsedArgs["duration_ms"]

                diff = milli_sec - now

                while (diff > 0):
                        #print("Now: " + str(now))
                        #print("Diff: " + str(diff))
                        #print("Factor: " + str(1/parsedArgs["duration_ms"]))
                        #print("X: " + str(parsedArgs['duration_ms'] - diff))
                        factor = (float(1)/float(parsedArgs["duration_ms"])) * float(parsedArgs['duration_ms'] - diff)
                        #print(factor)

                        coltorender = Color(int(round(float(coldiff[1])*factor + parsedcol[1])),
                                int(round(float(coldiff[0])*factor + parsedcol[0])),
                                int(round(float(coldiff[2])*factor + parsedcol[2])))

                        #print(coltorender)

                        for i in range(strip.numPixels()):
                                if not getattr(ct, "change", False):
                                        strip.setPixelColor(i, coltorender)
                                else:
                                        #print("Applying change now...")
                                        return
                        strip.show()

                        now = int(round(time.time() * 1000))
                        diff = milli_sec - now
                
                now = int(round(time.time() * 1000))
                milli_sec = now + parsedArgs["duration_ms"]

                diff = milli_sec - now
                
                while (diff > 0):
                        #print("Now: " + str(now))
                        #print("Diff: " + str(diff))
                        #print("Factor: " + str(1/parsedArgs["duration_ms"]))
                        #print("X: " + str(parsedArgs['duration_ms'] - diff))
                        factor = (float(1)/float(parsedArgs["duration_ms"])) * float(parsedArgs['duration_ms'] - diff)
                        #print(factor)

                        coltorender = Color(int(round(float(-coldiff[1])*factor + parsedcol2[1])),
                                int(round(float(-coldiff[0])*factor + parsedcol2[0])),
                                int(round(float(-coldiff[2])*factor + parsedcol2[2])))

                        #print(coltorender)

                        for i in range(strip.numPixels()):
                                if not getattr(ct, "change", False):
                                        strip.setPixelColor(i, coltorender)
                                else:
                                        #print("Applying change now...")
                                        return
                        strip.show()

                        now = int(round(time.time() * 1000))
                        diff = milli_sec - now

def parseArguments(argsarray, classarray, namesarray):
        output = dict()
        for e, c, n in zip(argsarray, classarray, namesarray):
                if c is Color:
                        #print("------------------------")
                        #print("Parsing Color now")
                        color = e.replace('[', '').replace(']', '').split(",")
                        color = [ int(x) for x in color ]
                        colorr = Color(color[1], color[0], color[2])
                        output[n] = colorr
                        #print("Finished parsing Color: %s %s %s" % (color[1], color[0], color[2]))
                elif c is int:
                        #print("------------------------")
                        #print("Parsing Int now")
                        output[n] = int(e)
                        #print("Finished parsing Int: %s" % (output[n]))
        
        return output

def parseColor(color):
        stri = "{0:b}".format(color)

        for i in range(24 - len(stri)):
                stri = "0" + stri

        return [int(stri[8:16], 2), int(stri[0:8], 2), int(stri[16:24], 2)]

def LED_Init():
        for i in range(0, 33): #1-1
                LEDS.append(i)
        for i in range(275, 281): #1-2
                LEDS.append(i)

        for i in range(33, 67): #2-1
                LEDS.append(i)
        for i in range(228, 234): #2-2
                LEDS.append(i)
        
        for i in range(234, 275): #3
                LEDS.append(i)

        for i in range(67, 87): #4-1
                LEDS.append(i)
        for i in range(208, 228): #4-2
                LEDS.append(i)
        
        for i in range(87, 121): #5-1
                LEDS.append(i)
        for i in range(202, 208): #5-2
                LEDS.append(i)

        for i in range(162, 202): #6
                LEDS.append(i)

        for i in range(121, 162): #7
                LEDS.append(i)

        #######################################################################

        for i in range(0, 33): #1-1
                LEDS.append(i)
        for i in range(275, 281): #1-2
                LEDS.append(i)

        for i in range(33, 67): #2-1
                LEDS.append(i)
        for i in range(228, 234): #2-2
                LEDS.append(i)
        
        for i in range(234, 275): #3
                LEDS.append(i)

        for i in range(67, 87): #4-1
                LEDS.append(i)
        for i in range(208, 228): #4-2
                LEDS.append(i)
        
        for i in range(87, 121): #5-1
                LEDS.append(i)
        for i in range(202, 208): #5-2
                LEDS.append(i)

        for i in range(162, 202): #6
                LEDS.append(i)

        for i in range(121, 162): #7
                LEDS.append(i)

def requestLoop():
        try:
                isAlive = False
                while True:
                        global lastBefehle
                        global lastArgss
                        global befehlIterable
                        global isParsed
                        global t2
                        
                        f = open("/var/www/html/led-server/befehl.txt", "r")

                        sub = f.readline().split("\n")
                        try:
                                change = int(sub[0])
                        except ValueError:
                                #print("Caught ValueError--------------------------------------------------------------------")
                                change = 0
                        f.close()

                        if change:
                                print("Change detected!")

                                t2.change = True
                                isAlive = False

                                f = open("/var/www/html/led-server/befehl.txt", "r")
                                #lines = list(f)
                                wholefile = f.read()
                                lines = wholefile.split("\n")
                                f.close()

                                lines[0] = "00"

                                #print("______________________________________ENTERING EXPERIMENTAL ZONE______________________________________")
                                #print(wholefile)

                                parts = wholefile.split("---\n")
                                parts = parts[1:]
                                #print(parts)
                                 
                                lastBefehle = [ x.split("\n")[0] for x in parts ]
                                #print("---------Last Befehle:---------------")
                                #print(lastBefehle)

                                lastArgss = [ x.split("\n")[1:] for x in parts ]
                                for a in lastArgss:
                                        a.insert(0, strip)
                                        while "" in a:
                                                a.remove("")
                                #print("---------Last Args:---------------")
                                #print(lastArgss)

                                if lastBefehle[0] == "terminate":
                                        return

                                isParsed = False

                                f = open("/var/www/html/led-server/befehl.txt", "w")
                                f.writelines("\n".join(lines))
                                f.close()

                                befehlIterable = 0

                                t2 = threading.Thread(target=getattr(StripMethods, lastBefehle[befehlIterable]), args=tuple(lastArgss[befehlIterable]))

                                #befehlIterable += 1

                                t2.daemon = True
                                t2.start()
                                
                                isAlive = True

                        elif not t2.isAlive() and isAlive:
                                #print("Thread not alive anymore, starting again")
                                befehlIterable += 1
                                if befehlIterable >= len(lastBefehle):
                                        befehlIterable = 0

                                t2 = threading.Thread(target=getattr(StripMethods, lastBefehle[befehlIterable]), args=tuple(lastArgss[befehlIterable]))
                                isParsed = False
                                t2.daemon = True
                                t2.start()

        except KeyboardInterrupt:
                print("Terminating programm")

def brightnessLoop():
        try:
                isAlive = False
                while True:
                        global lastBefehle
                        global lastArgss
                        global befehlIterable
                        global isParsed
                        global t3
                        
                        f = open("/var/www/html/led-server/brightness.txt", "r")
                        sub = f.readline().split("\n")
                        f.close()
                        try:
                                change = int(sub[0])
                        except ValueError:
                                #print("Caught ValueError--------------------------------------------------------------------")
                                change = 0
                        
                        if change:
                                print("BRIGHTChange detected!")

                                t3.change = True
                                isAlive = False

                                f = open("/var/www/html/led-server/brightness.txt", "r")
                                wholefile = f.read()
                                lines = wholefile.split("\n")
                                f.close()

                                lines[0] = "00\n"

                                parts = wholefile.split("---\n")
                                parts = parts[1:]

                                lastSep = [ x.split("\n")[0] for x in parts ]
                                #print("---------Last Befehle:---------------")
                                #print(lastBefehle)

                                lastSepArgs = [ x.split("\n")[1:] for x in parts ]
                                for a in lastSepArgs:
                                        a.insert(0, strip)
                                        while "" in a:
                                                a.remove("")
                                #print("---------Last Args:---------------")
                                #print(lastArgss)

                                if len(lastSep) >= 1:
                                        if lastSep[0] == "terminate":
                                                return

                                isParsed = False

                                f = open("/var/www/html/led-server/brightness.txt", "w")
                                f.writelines(lines)
                                f.close()

                                for idx, sep in enumerate(lastSep):
                                        if (sep == "brightness"):
                                                #print("hey")
                                                #brightness = float(lastSepArgs[idx][1])
                                                strip.setBrightness(int(lastSepArgs[idx][1]))
                                                #print(strip.getBrightness())
                                                settings['brightness'] = int(lastSepArgs[idx][1])
                                        elif (sep == "led_count"):
                                                settings['led_count'] = int(lastSepArgs[idx][1])

                                #print(settings)
                                #print(json.dumps(settings))

                                f = open("/var/www/html/led-server/settings.txt", "w")
                                f.write(json.dumps(settings))
                                f.close()

        except KeyboardInterrupt:
                print("Terminating programm")

# Main program logic follows:
if __name__ == '__main__':
        # Process arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
        args = parser.parse_args()

        

        ##########################################################################################################################################################

        f = open("/var/www/html/led-server/befehl.txt", "r")
        wholefile = f.read()
        #print(wholefile)
        lines = wholefile.split("\n")
        f.close()

        f = open("/var/www/html/led-server/befehl.txt", "w")
        lines[0] = "01"
        f.writelines("\n".join(lines))
        f.close()

        f = open("/var/www/html/led-server/brightness.txt", "r")
        wholefile = f.read()
        lines = wholefile.split("\n")
        f.close()

        f = open("/var/www/html/led-server/brightness.txt", "w")
        lines[0] = "01"
        f.writelines("\n".join(lines))
        f.close()

        LED_Init()

        f = open("/var/www/html/led-server/settings.txt", "r")
        #print(f.read())
        settings = json.loads(f.read())

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

        settings['led_config'] = led_config

        concatarray = []
        for e in settings['led_config']:
                concatarray = numpy.concatenate((concatarray, e))

        LEDS = concatarray.astype(int)
        print(LEDS)

        #print(settings)
        #print(settings['led_config'])
        f.close()








        ##################################################################################################################################################################

        # Create NeoPixel object with appropriate configuration.
        strip = Adafruit_NeoPixel(settings.get('led_count', LED_COUNT), LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, settings.get('brightness', LED_BRIGHTNESS), LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        strip.begin()

        

        print('Becca said hi!')

        #print("whats this?")
        t = threading.Thread(target=requestLoop)
        print("Starting requestLoop")
        t.start()

        t1 = threading.Thread(target=brightnessLoop)
        print("Starting brightnessLoop")
        t1.start()

        t.join()
        t1.join()

        f = open("/var/www/html/led-server/befehl.txt", "w")
        f.write("01\n---\nrainbow\n50")
        f.close()

        f = open("/var/www/html/led-server/brightness.txt", "w")
        f.write("01\n---\nbrightness\n50")
        f.close()

        print(threading.activeCount())
        
        print("EndofProgramm!")
