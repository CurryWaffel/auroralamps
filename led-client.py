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
import threading
import copy
from neopixel import *
import argparse
import inspect

# LED strip configuration:
LED_COUNT = 300 # Number of LED pixels.
LED_PIN = 18 # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN = 10 # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000 # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10 # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255 # Set to 0 for darkest and 255 for brightest
LED_INVERT = False # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0 # set to '1' for GPIOs 13, 19, 41, 45 or 53
befehl = ""
lastBefehl = ""
lastArgs = []
lastParsed = []
isParsed = False
t2 = threading.Thread()
t3 = threading.Thread()


class StripMethods:
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
                                strip.setPixelColor(i, parsedArgs["color"])
                                strip.show()
                                time.sleep(parsedArgs["wait_ms"]/1000.0)
                        else:
                                print("Applying change now...")
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
                                                print("Applying change now...")
                                                return
                                strip.show()
                                time.sleep(parsedArgs["wait_ms"]/1000.0)
                                for i in range(0, strip.numPixels(), 3):
                                        if not getattr(ct, "change", False):
                                                strip.setPixelColor(i+q, 0)
                                        else:
                                                print("Applying change now...")
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
                                print("Applying change now...")
                                return
                strip.show()
                        
        @staticmethod
        def rainbow(strip, wait_ms=1, iterations=1):
                ct = threading.currentThread()
                """Draw rainbow that fades across all pixels at once."""
                for j in range(256*iterations):
                        #print("Bruh")
                        for i in range(strip.numPixels()):
                                if not getattr(ct, "change", False):
                                        #print("Setting Pixel #" + str(i))
                                        strip.setPixelColor(i, StripMethods.wheel((i+j) & 255))
                                else:
                                        print("Applying change now...")
                                        return
                        #print("This that")
                        strip.show()
                        #print("After show")

                        #time.sleep(wait_ms/1000.0)

                        #print("After wait")

        @staticmethod
        def rainbowStationary(strip, wait_ms=1, iterations=1):
                ct = threading.currentThread()
                """Draw rainbow that fades across all pixels at once."""
                for j in range(256*iterations):
                        #print("Bruh")
                        for i in range(strip.numPixels()):
                                if not getattr(ct, "change", False):
                                        #print("Setting Pixel #" + str(i))
                                        strip.setPixelColor(i, StripMethods.wheel(j & 255))
                                else:
                                        print("Applying change now...")
                                        return
                        strip.show()

        @staticmethod
        def rainbowCycle(strip, wait_ms=20, iterations=5):
                """Draw rainbow that uniformly distributes itself across all pixels."""
                for j in range(256*iterations):
                        for i in range(strip.numPixels()):
                                strip.setPixelColor(i, StripMethods.wheel(((i * 256 // strip.numPixels()) + j) & 255))
                        strip.show()
                        time.sleep(wait_ms/1000.0)

        @staticmethod
        def theaterChaseRainbow(strip, wait_ms=50):
                """Rainbow movie theater light style chaser animation."""
                for j in range(256):
                        for q in range(3):
                                for i in range(0, strip.numPixels(), 3):
                                        strip.setPixelColor(i+q, StripMethods.wheel((i+j) % 255))
                                strip.show()
                                time.sleep(wait_ms/1000.0)
                                for i in range(0, strip.numPixels(), 3):
                                        strip.setPixelColor(i+q, 0)

def parseArguments(argsarray, classarray, namesarray):
        output = dict()
        for e, c, n in zip(argsarray, classarray, namesarray):
                if c is Color:
                        print("------------------------")
                        print("Parsing Color now")
                        color = e.replace('[', '').replace(']', '').split(",")
                        color = [ int(x) for x in color ]
                        colorr = Color(color[1], color[0], color[2])
                        output[n] = colorr
                        print("Finished parsing Color: %s %s %s" % (color[1], color[0], color[2]))
                elif c is int:
                        print("------------------------")
                        print("Parsing Int now")
                        output[n] = int(e)
                        print("Finished parsing Int: %s" % (output[n]))
        
        return output

def requestLoop():
        try:
                isAlive = False
                while True:
                        global lastBefehl
                        global lastArgs
                        global isParsed
                        global befehl
                        global t2
                        
                        f = open("/var/www/html/led-server/befehl.txt", "r")
                        #befehl = ''.join(f.read().split('\n'))

                        sub = f.readline().split("\n")
                        #print("SUB: " + sub[0])
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
                                lines = list(f)
                                f.close()

                                #print(lines)
                                lines[0] = "00\n"

                                lastBefehl = lines[1].split("\n")[0]
                                print("Last Befehl: " + lastBefehl)

                                if lastBefehl == "terminate":
                                        return

                                '''
                                lastArgsSub = lines[2]
                                #print("Last Args: " + lastArgsSub)
                                colors = lastArgsSub.replace('[', '').replace(']', '').split(",")
                                colors = [ int(x) for x in colors ]
                                #print("Red: %s Green: %s Blue: %s" % (colors[0], colors[1], colors[2]))
                                '''
                                if lastBefehl == "off":
                                        lastBefehl = "setColor"
                                        lastArgs = ["[0,0,0]"]
                                else:
                                        lastArgs = lines[2:]

                                #lastArgs.append(lines[2])
                                #lastArgs.append(lines[3])

                                lastArgs.insert(0, strip)

                                isParsed = False

                                #print("Hey")
                                #print(lastArgs)
                                #print("There")

                                f = open("/var/www/html/led-server/befehl.txt", "w")
                                f.writelines(lines)
                                f.close()

                                t2 = threading.Thread(target=getattr(StripMethods, lastBefehl), args=tuple(lastArgs))
                                t2.daemon = True
                                t2.start()
                                
                                isAlive = True

                                #print(lines)
                                #f.writelines(lines)
                        elif not t2.isAlive() and isAlive:
                                #print("Thread not alive anymore, starting again")
                                t2 = threading.Thread(target=getattr(StripMethods, lastBefehl), args=tuple(lastArgs))
                                t2.daemon = True
                                t2.start()
                                #isAlive = False
        except KeyboardInterrupt:
                print("Terminating programm")

# Main program logic follows:
if __name__ == '__main__':
        # Process arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
        args = parser.parse_args()

        # Create NeoPixel object with appropriate configuration.
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        strip.begin()

        print ('Press Ctrl-C to quit.\r\n Becca said hi!')
        #print('Uwu')
        if not args.clear:
                print('Use "-c" argument to clear LEDs on exit')

        #print("whats this?")
        t = threading.Thread(target=requestLoop)
        print("Starting requestLoop")
        t.start()
        t.join()

        f = open("/var/www/html/led-server/befehl.txt", "w")
        f.write("01\ncolorWipe\n[114,0,171]\n1\n")
        f.close()

        print(threading.activeCount())
        
        print("EndofProgramm!")
