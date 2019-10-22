'''
Company     : DiscoverTechnologies
Author      : Chetan Gupta
Date created: 14/7/2018
Description : This is python program written to read GPS information
              for GPGGA standard.            

'''


import serial
import time
import RPi.GPIO as GPIO
import sys
from threading import Thread


#############GPIO configuration#######
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
######################################


##################  Lcd defines  #################

# Define GPIO to LCD mapping
LCD_RS = 13   
LCD_E  = 19       
LCD_D4 = 6 
LCD_D5 = 5         
LCD_D6 = 21       
LCD_D7 = 26

#configure GPIO as output
GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT) # RS
GPIO.setup(LCD_D4, GPIO.OUT) # DB4
GPIO.setup(LCD_D5, GPIO.OUT) # DB5
GPIO.setup(LCD_D6, GPIO.OUT) # DB6
GPIO.setup(LCD_D7, GPIO.OUT) # DB7





# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

LCD_SCRL_DEL = 0.14529  #LCD scrolling delay




#LCD function to initialize, display character on it.

def lcd_init():
    # Initialise display
    lcd_byte(0x33,LCD_CMD) # 110011 Initialise
    lcd_byte(0x32,LCD_CMD) # 110010 Initialise
    lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
    lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
    lcd_byte(0x01,LCD_CMD) # 000001 Clear display
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character or False for command    

    GPIO.output(LCD_RS, mode) # RS
    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)
    if bits&0x20==0x20:
        GPIO.output(LCD_D5, True)
    if bits&0x40==0x40:
        GPIO.output(LCD_D6, True)
    if bits&0x80==0x80:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

def lcd_toggle_enable():
    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def lcd_string(message,line):
    # Send string to display
    message = message.ljust(LCD_WIDTH," ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)


def lcd_string_scroll(message, line, SCL_DELAY):
    string = message.strip()
    string = "               " + string
    #print "length = " + str(len(string))
    if line == 1:
        lcd_string("                ", line)
        for i in range(len(message)+1+16):
            lcd_string(string, line)
            time.sleep(SCL_DELAY)
            string = string[1:] + " " 
        pass
    else:
        lcd_string("                ", line)
        for i in range(len(message)+1+16):
            lcd_string(string, line)
            time.sleep(SCL_DELAY)
            string = string[1:] + " "
        pass


################## End of Lcd defines  #################
################## User function #######################
def delayms(time_in_msec):
    time.sleep( (time_in_msec/1000) )
    pass

def delaysec(time_in_sec):
    time.sleep(time_in_sec)
    

################# End of User function #################
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.050)
    pass
except:
    try:
        ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=0.050)
        pass
    except:
        try:
            ser = serial.Serial('/dev/ttyUSB2', 9600, timeout=0.050)
            pass
        except:
            try:
                ser = serial.Serial('/dev/ttyUSB3', 9600, timeout=0.050)
                pass
            except Exception as e:
                print "Error connecting to GPS module!\nerror:" + str(e)
                exit(0)
                pass
            pass
        pass
    pass    
        
def main():
    lcd_init() 
    while True:
        while ser.inWaiting():                            #Waiting here unless some string is recieve
            gps_str = str(ser.readline())
            gpgga = []
            if "$GPGGA" in gps_str:
                gps_str = gps_str.translate(None,"\n\r$")
                gpgga = gps_str.split(",")
                #print gpgga                       #print GPS whole string that is receiving

                
                standard = gpgga[0]
                utc = gpgga[1]
                lat = gpgga[2]
                lat_direction = gpgga[3]
                lon = gpgga[4] 
                lon_direction = gpgga[5]
                quality = gpgga[6]
                no_of_sats = gpgga[7]
                hdop = gpgga[8]
                alt = gpgga[9]
                a_units = gpgga[10]
                undulation = gpgga[11]
                u_units = gpgga[12]
                age = gpgga[13]
                stn_id = gpgga[14][:gpgga[14].find("*")]
                checksum = gpgga[14][(gpgga[14].find("*")+1):]

                
                print ("\n" * 50)
                print "Standard                         = " + standard
                print "UTC                              = " + utc
                print "Lattitude                        = " + lat
                print "Lattitude Direction              = " + lat_direction
                print "Longitude                        = " + lon
                print "Longitude Direction              = " + lon_direction
                print "Quality                          = " + quality
                print "Number of Satellites             = " + no_of_sats
                print "Horizontal Dilution of Precision = " + hdop
                print "Altitude                         = " + alt
                print "Units of Antenna Altitude        = " + a_units
                print "Undulation                       = " + undulation
                print "Units of Undulation              = " + u_units
                print "Age                              = " + age
                print "Station ID                       = " + stn_id
                print "Checksum                         = " + checksum
                lcd_string("Loc. Tracking                 ",LCD_LINE_1)
                #lcd_string(lat[:lat.find(".")] + " " + lat_direction + ", " + lon[:lon.find(".")] + " " + lon_direction, LCD_LINE_2)
                
                lcd_string(lat[:2] + str(chr(223)) + lat[2:4] + " " + lat_direction + ", " + lon[1:3] + str(chr(223)) + lon[3:5] + " " + lon_direction, LCD_LINE_2)

           
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_string("Program         ",LCD_LINE_1)
        lcd_string("Terminated...   ",LCD_LINE_2)
        GPIO.cleanup()
        print "\n\nProgram terminated..."
        
