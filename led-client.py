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
from neopixel import *
import argparse

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

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
        ct = threading.currentThread()
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
                if not getattr(ct, "change", False):
                        strip.setPixelColor(i, color)
                        strip.show()
                        time.sleep(wait_ms/1000.0)
                else:
                        print("Applying change now...")
                        return

def theaterChase(strip, color, wait_ms=50, iterations=10):
        ct = threading.currentThread()
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
                                if not getattr(ct, "change", False):
				        strip.setPixelColor(i+q, color)
                                else:
                                        print("Applying change now...")
                                        return
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
                                if not getattr(ct, "change", False):
				        strip.setPixelColor(i+q, 0)
                                else:
                                        print("Applying change now...")
                                        return

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

def rainbow(strip, wait_ms=20, iterations=1):
        ct = threading.currentThread()
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
                for i in range(strip.numPixels()):
                        if not getattr(ct, "change", False):
                                strip.setPixelColor(i, wheel((i+j) & 255))
                        else:
                                print("Applying change now...")
                                return
                strip.show()
                time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel(((i * 256 // strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def requestLoop():
	while True:
                global lastBefehl
                global befehl
                global t
                
		f = open("/var/www/html/led-server/befehl.txt", "r")
		befehl = ''.join(f.read().split('\n'))

		if befehl == "09":
                        break

                if not t.isAlive():
                                print("Starting LED\'s")
                                t.start()

		if befehl != lastBefehl:
			lastBefehl = befehl     
			print("Changing LED\'S")
			t.change = True
			

def ledLoop():
        global befehl
	try:
                while True:
                        if befehl == "01":
                                colorWipe(strip, Color(255, 0, 0)) # Red wipe
                                colorWipe(strip, Color(0, 255, 0)) # Blue wipe
                                colorWipe(strip, Color(0, 0, 255)) # Green wipe
                        elif befehl == "02":
                                theaterChase(strip, Color(127, 127, 127))
                                theaterChase(strip, Color(127, 0, 0))
                                theaterChase(strip, Color( 0, 0, 127))
                        elif befehl == "03":
                                rainbow(strip)
                        elif befehl == "04":
                                rainbowCycle(strip)
                        elif befehl == "05":
                                theaterChaseRainbow(strip)
                        else:
                                colorWipe(strip, Color(0,0,0), 10)

                        threading.currentThread().change = False

        except KeyboardInterrupt:
                if args.clear:
                        colorWipe(strip, Color(0,0,0), 10)


t = threading.Thread(target=ledLoop)
t.daemon = True
t.change = False

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

        print ('Press Ctrl-C to quit.')
        print('Uwu')
        if not args.clear:
                print('Use "-c" argument to clear LEDs on exit')

        print("whats this?")
        t2 = threading.Thread(target=requestLoop)
        print("Starting requestLoop")
        t2.start()
        t2.join()
        print("EndofProgramm!")
