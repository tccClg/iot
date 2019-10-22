import sys
import time
import datetime
import RPi.GPIO as GPIO
import tm1637

Display=tm1637.TM1637(23,24,tm1637.BRIGHT_TYPICAL)
Display.Clear()
Display.SetBrightnes(1)
