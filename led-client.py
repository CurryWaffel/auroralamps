#!/usr/bin/env python3
# Driver for AuroraLamp based on the NeoPixel library
# Author: Max Ruesch (xammaximus44@gmail.com)
#
# Uses a direct port of the Arduino Neopixel library created by Tony DiCola (tony@tonydicola.com)

import time
import json
import numpy
import threading
from neopixel import *

# LED strip configuration:
LED_COUNT = 281 # Number of LED pixels.
LED_PIN = 18 # GPIO pin connected to the pixels (18 uses PWM, has to be disabled before use).
LED_FREQ_HZ = 800000 # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10 # DMA channel to use for generating signal
LED_BRIGHTNESS = 255 # Set to 0 for darkest and 255 for brightest
LED_INVERT = False # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0 # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Initalization on global variables
settings = {}
dicty = {}
listThreads = []

debug = True

# Class to contain all methods that can be used for commands.
# Reason for contain is the dynamic method call in the thread start.
class StripMethods: # TODO More accurate timing (requires more calculating)
        @staticmethod
        def colorWipe(args):
                """Wipe color across display a pixel at a time"""
                leds_to_use = get_leds_to_use(args)

                for i in range(len(leds_to_use)):
                        if not getattr(threading.currentThread(), "change", False):
                                strip.setPixelColor(leds_to_use[i], args["color"])
                                strip.show()
                                time.sleep(args["wait_ms"]/1000.0)
                        else: return

        @staticmethod
        def theaterChase(args):
                """Movie theater light style chaser animation"""
                leds_to_use = get_leds_to_use(args)

                for j in range(args["iterations"]):
                        for q in range(3):
                                # Activate every 3rd led
                                for i in range(0, len(leds_to_use), 3):
                                        if not getattr(threading.currentThread(), "change", False):
                                                strip.setPixelColor(leds_to_use[i-q], args["color"])
                                        else: return

                                strip.show()
                                time.sleep(args["wait_ms"]/1000.0)

                                # Deactivate every 3rd led
                                for i in range(0, len(leds_to_use), 3):
                                        if not getattr(threading.currentThread(), "change", False):
                                                strip.setPixelColor(leds_to_use[i-q], 0)
                                        else: return

        @staticmethod
        def wheel(pos):
                """Generate rainbow colors across 0-255 positions"""
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
                """Set a certain color for all given leds"""
                leds_to_use = get_leds_to_use(args)

                for i in range(len(leds_to_use)):
                        if not getattr(threading.currentThread(), "change", False):
                                strip.setPixelColor(leds_to_use[i], args["color"])
                        else: return
                strip.show()
                        
        @staticmethod
        def rainbow(args):
                """Draw rainbow that fades across all pixels at once"""
                leds_to_use = get_leds_to_use(args)

                for j in range(256):
                        for i in range(len(leds_to_use)):
                                if not getattr(threading.currentThread(), "change", False):
                                        strip.setPixelColor(leds_to_use[i], StripMethods.wheel((i+j) & 255))
                                else: return
                        strip.show()
                        time.sleep(args['wait_ms']/1000.0)

        @staticmethod
        def rainbowStationary(args):
                """Draw rainbow that fades across all pixels at once and doesnt move"""
                leds_to_use = get_leds_to_use(args)

                for j in range(256):
                        for i in range(len(leds_to_use)):
                                if not getattr(threading.currentThread(), "change", False):
                                        strip.setPixelColor(leds_to_use[i], StripMethods.wheel(j & 255))
                                else: return
                        strip.show()
                        time.sleep(args["wait_ms"]/1000.0)

        @staticmethod
        def rainbowCycle(args): #TODO implement in app
                """Draw rainbow that uniformly distributes itself across all pixels"""
                leds_to_use = get_leds_to_use(args)

                for j in range(256*args["iterations"]):
                        for i in range(len(leds_to_use)):
                                if not getattr(threading.currentThread(), "change", False):
                                        strip.setPixelColor(i, StripMethods.wheel(((i * 256 // len(leds_to_use)) + j) & 255))
                                else: return
                        strip.show()
                        time.sleep(args["wait_ms"]/1000.0)

        @staticmethod
        def theaterChaseRainbow(args):
                """Rainbow movie theater light style chaser animation"""
                leds_to_use = get_leds_to_use(args)

                for j in range(256):
                        for q in range(3):
                                for i in range(0, len(leds_to_use), 3):
                                        if not getattr(threading.currentThread(), "change", False):
                                                strip.setPixelColor(leds_to_use[i-q], StripMethods.wheel((i+j) % 255))
                                        else:
                                                return
                                strip.show()
                                time.sleep(args["wait_ms"]/1000.0)
                                for i in range(0, len(leds_to_use), 3):
                                        if not getattr(threading.currentThread(), "change", False):
                                                strip.setPixelColor(leds_to_use[i-q], 0)
                                        else:
                                                return
        
        @staticmethod
        def interpolate(args):
                """Interpolation between two colors over given time"""

                # Show first color
                StripMethods.setColor(args)

                leds_to_use = get_leds_to_use(args)

                # Parse both colors to array
                parsedcol_1 = parseColor(args["color"])
                parsedcol_2 = parseColor(args["color2"])
                
                # Calc difference of colors to apply over time
                coldiff = [parsedcol_2[0] - parsedcol_1[0], parsedcol_2[1] - parsedcol_1[1], parsedcol_2[2] - parsedcol_1[2]]

                # Calc initial time difference
                now = int(round(time.time() * 1000))
                milli_sec = now + args["duration_ms"]
                diff = milli_sec - now

                # Update leds according to time
                while (diff > 0):
                        # Calc factor for color depending on how much time has passed
                        factor = (1.0 / float(args["duration_ms"])) * float(args["duration_ms"] - diff)

                        # Calc color to display at current time
                        col_to_render = Color(int(round(float(coldiff[1]) * factor + parsedcol_1[1])),
                                int(round(float(coldiff[0]) * factor + parsedcol_1[0])),
                                int(round(float(coldiff[2]) * factor + parsedcol_1[2])))

                        # Display current color on strip
                        for i in range(len(leds_to_use)):
                                if not getattr(threading.currentThread(), "change", False):
                                        strip.setPixelColor(leds_to_use[i], col_to_render)
                                else: return
                        strip.show()

                        # Calc new time difference
                        now = int(round(time.time() * 1000))
                        diff = milli_sec - now
                
                if args['goback']:
                        now = int(round(time.time() * 1000))
                        milli_sec = now + args["duration_ms"]
                        diff = milli_sec - now
                        
                        while (diff > 0):
                                # Calc factor for color depending on how much time has passed
                                factor = (1.0 / float(args["duration_ms"])) * float(args['duration_ms'] - diff)

                                # Calc color to display at current time
                                col_to_render = Color(int(round(float(-coldiff[1]) * factor + parsedcol_2[1])),
                                        int(round(float(-coldiff[0]) * factor + parsedcol_2[0])),
                                        int(round(float(-coldiff[2]) * factor + parsedcol_2[2])))

                                # Display current color on strip
                                for i in range(len(leds_to_use)):
                                        if not getattr(threading.currentThread(), "change", False):
                                                strip.setPixelColor(leds_to_use[i], col_to_render)
                                        else: return
                                strip.show()

                                # Calc new time difference
                                now = int(round(time.time() * 1000))
                                diff = milli_sec - now
        
        @staticmethod
        def wait(args):                
                now = int(round(time.time()*1000))
                milli_sec = now + args['duration_ms']
                diff = milli_sec - now

                while(diff > 0):
                        if not getattr(threading.currentThread(), "change", False):
                                time.sleep(0.01)
                        else:
                                return
                        
                        now = int(round(time.time() * 1000))
                        diff = milli_sec - now

# Parse colors from 24 bit format to array RGB format
def parseColor(color):
        # Format string number from decimal to binary
        stri = "{0:b}".format(color)

        # Add leading zeros until 24 bit width is reached
        for i in range(24 - len(stri)):
                stri = "0" + stri

        # Return array with numbers sliced and converted back to decimal
        return [int(stri[8:16], 2), int(stri[0:8], 2), int(stri[16:24], 2)]

# Load leds to use from the args delivered with command
def get_leds_to_use(args):
        # Get the lamps to use
        if not args.has_key('lamps'):
                args['lamps'] = [0,1,2,3,4,5,6]

        leds = []
        for i, e in enumerate(settings['led_config']):
                if i in args['lamps']:
                        leds = numpy.concatenate((leds, e))

        return leds.astype(int)

# Loading standard led config for the only lamp that exists (yet)
def load_led_config():
        led_config = []
        part = []
        for i in range(0, 33): # Lamp 1 - Part 1
                part.append(i)
        for i in range(275, 281): # Lamp 1 - Part 2
                part.append(i)
        led_config.append(part)
        part = []
        for i in range(33, 67): # Lamp 2 - Part 1
                part.append(i)
        for i in range(228, 234): # Lamp 2 - Part 2
                part.append(i)
        led_config.append(part)
        part = []
        for i in range(234, 275): # Lamp 3
                part.append(i)
        led_config.append(part)
        part = []
        for i in range(67, 87): # Lamp 3 - Part 1
                part.append(i)
        for i in range(208, 228): # Lamp 3 - Part 2
                part.append(i)
        led_config.append(part)
        part = []
        for i in range(87, 121): # Lamp 5 - Part 1
                part.append(i)
        for i in range(202, 208): # Lamp 5 - Part 2
                part.append(i)
        led_config.append(part)
        part = []
        for i in range(162, 202): # Lamp 6
                part.append(i)
        led_config.append(part)
        part = []
        for i in range(121, 162): # Lamp 7
                part.append(i)
        led_config.append(part)
        return led_config

# Main loop for changes and live modifications
def requestLoop():
        while True:
                global dicty
                global listThreads
                
                # Loading changes on both commands and settings
                command_change_f = open("/var/www/html/led-server/change.txt", "r")
                setting_change_f = open("/var/www/html/led-server/setting_change.txt", "r")
                try: command_change = json.load(command_change_f)['change']
                except ValueError: command_change = 0

                try: setting_change = json.load(setting_change_f)['change']
                except ValueError: setting_change = 0

                command_change_f.close()
                setting_change_f.close()

                # Change current command list if there is any change
                if command_change:
                        # Part from previous change for debug purposes
                        if debug: print("---------------------------------------------------------------------------------------------------------------------")
                        
                        # Loading new command list from php modified file
                        command_f = open("/var/www/html/led-server/befehl.txt", "r")
                        dicty = json.load(command_f)
                        if (debug): print(dicty)
                        command_f.close()

                        # Terminate the loop, eq. to "STOP" in the app
                        if len(dicty) == 0 or dicty[0][0]['command'] == "terminate": return

                        # Unmarking change in change file
                        command_change_f = open("/var/www/html/led-server/change.txt", "w")
                        json.dump({'change':0}, command_change_f)
                        command_change_f.close()
                        
                        # Stop old threads
                        for i in listThreads: i.change = True
                        listThreads = []

                        # Start new threads with the command loop, one thread for each of the partCommandLists
                        for cmdList in dicty:
                                listThread = threading.Thread(target=listloop, args=tuple([cmdList]))
                                listThread.daemon = True
                                listThread.start()
                                listThreads.append(listThread)
                
                # Change Settings if there is any change
                if setting_change:
                        isAlive = False

                        # Loading new settings from php modified file
                        setting_f = open("/var/www/html/led-server/setting.txt", "r")
                        try: dicti = json.load(setting_f)
                        except ValueError: dicti = {}
                        setting_f.close()

                        # Unmarking change in change file
                        setting_change_f = open("/var/www/html/led-server/setting_change.txt", "w")
                        json.dump({'change':0}, setting_change_f)
                        setting_change_f.close()

                        # Changing current settings live if there is any change
                        if dicti.has_key("brightness"):
                                strip.setBrightness(int(dicti["brightness"]))
                                settings['brightness'] = int(dicti["brightness"])
                        if dicti.has_key("led_count"):
                                settings['led_count'] = int(dicti["led_count"])

                        # Writing current settings including change to the setting file that isnt modified by php
                        settings_f = open("/var/www/html/led-server/settings.txt", "w")
                        settings_f.write(json.dumps(settings))
                        settings_f.close()

# Main loop for commands
def listloop(dictynum):
        # Iterating variable for the current command list
        befehlIter = 0
        
        commandThread = threading.Thread() # Command thread for this list

        # Repeat while no change is indicated
        while not getattr(threading.currentThread(), "change", False):
                # Only do something while the command thread for this list isnt active anymore
                if not commandThread.isAlive():                        
                        commandThread = threading.Thread(target=getattr(StripMethods, dictynum[befehlIter]['command']), args=tuple([dictynum[befehlIter]['args']]))
                        commandThread.daemon = True
                        commandThread.start()
                        
                        # Update the iterating variable
                        befehlIter += 1
                        # If the end of the list is reached reset the iterating variable
                        if befehlIter >= len(dictynum):
                                befehlIter = 0

        # Terminate any thread started from here asap, only reached when change is indicated
        commandThread.change = True

        if debug: print("Active Threads: " + str(threading.activeCount()))
        
        return

# Main program logic follows:
if __name__ == '__main__':
        # Reactivating last settings and command change, also loading settings from non php modified file
        command_change_f = open("/var/www/html/led-server/change.txt", "w")
        setting_change_f = open("/var/www/html/led-server/setting_change.txt", "w")
        settings_f = open("/var/www/html/led-server/settings.txt", "r")

        json.dump({'change':1}, command_change_f)
        json.dump({'change':1}, setting_change_f)
        settings = json.loads(settings_f.read())

        command_change_f.close()
        setting_change_f.close()
        settings_f.close()

        # Loading standard led config, is changed whenever more lamps are built
        settings['led_config'] = load_led_config()
        if debug: print(settings['led_config'])

        ############################################################################################################################################################################

        # Create NeoPixel object with appropriate configuration
        strip = Adafruit_NeoPixel(settings.get('led_count', LED_COUNT), LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, settings.get('brightness', LED_BRIGHTNESS), LED_CHANNEL)
        # Intialize the library (must be called once before other functions)
        strip.begin()

        # Include greetings from gf bc thats her wish
        if not debug: print('Becca said hi!')

        requestLoop()
        
        # This part is reached if the lamp is shut down via the app, rather than turning it off,
        # meaning it now defaults to a known working command, as seen below
        command_f = open("/var/www/html/led-server/befehl.txt", "w")
        json.dump([[{"command":"rainbow","args":{"wait_ms":0}}]], command_f)
        command_f.close()

        command_change_f = open("/var/www/html/led-server/change.txt", "w")
        json.dump({'change':1}, command_change_f)
        command_change_f.close()

        """
        f = open("/var/www/html/led-server/setting.txt", "w")
        json.dump({"brightness":50}, f)
        f.close()

        f = open("/var/www/html/led-server/setting_change.txt", "w")
        json.dump({'change':1}, f)
        f.close()
        """

        print("EndofProgramm!")
