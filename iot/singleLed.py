import RPi.GPIO as GPIO # Import Package import import time
import time
GPIO.setmode(GPIO.BOARD) # Set Mode BOARD or BCM
GPIO.setwarnings(False) # Disable Warnings
GPIO.setup(40,GPIO.OUT) #Set Pin 11 as Output
while True:
    print ("LED on") # 'on' Print Message
    GPIO.output(40,GPIO.HIGH) #Set GPIO pin High Turn on LED
    time.sleep(1) # wait for 1 Second
    print ("LED off") # 'off' Print Message
    GPIO.output(40,GPIO.LOW) #Set GPIO pin Low Turn off LED
    time.sleep(1)