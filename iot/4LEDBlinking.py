import RPi.GPIO as GPIO
import datetime
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(40,GPIO.OUT)
GPIO.setup(38,GPIO.OUT)
GPIO.setup(36,GPIO.OUT)
GPIO.setup(32,GPIO.OUT)

while True:
	print ("LED on")
	GPIO.output(40,GPIO.HIGH)
	GPIO.output(38,GPIO.LOW)
	GPIO.output(36,GPIO.HIGH)
	GPIO.output(32,GPIO.LOW)
	time.sleep(1)
	print ("LED off")
	GPIO.output(40,GPIO.LOW)
	GPIO.output(38,GPIO.HIGH)
	GPIO.output(36,GPIO.LOW)
	GPIO.output(32,GPIO.HIGH)
	time.sleep(1)