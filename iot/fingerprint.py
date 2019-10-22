


import time
import RPi.GPIO as GPIO
import sys
from threading import Thread
from pyfingerprint.pyfingerprint import PyFingerprint



GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

try:
    fingerprint_module = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    if ( fingerprint_module.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')
except:
    try:
        fingerprint_module = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)
        if ( fingerprint_module.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')
    except:
        try:
            fingerprint_module = PyFingerprint('/dev/ttyUSB2', 57600, 0xFFFFFFFF, 0x00000000)
            if ( fingerprint_module.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')
        except:
            try:
                fingerprint_module = PyFingerprint('/dev/ttyUSB3', 57600, 0xFFFFFFFF, 0x00000000)
                if ( fingerprint_module.verifyPassword() == False ):
                    raise ValueError('The given fingerprint sensor password is wrong!')
            except Exception as e:
                print('Exception message: ' + str(e))
                exit(1)
                pass
            pass
        pass
    pass    

'''
try:
    fingerprint_module = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    if ( fingerprint_module.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')
except Exception as e:
    print('Exception message: ' + str(e))
    exit(1)
'''



LCD_RS = 13   
LCD_E  = 19       
LCD_D4 = 6 
LCD_D5 = 5         
LCD_D6 = 21       
LCD_D7 = 26


GPIO.setup(LCD_E, GPIO.OUT)  
GPIO.setup(LCD_RS, GPIO.OUT) 
GPIO.setup(LCD_D4, GPIO.OUT) 
GPIO.setup(LCD_D5, GPIO.OUT) 
GPIO.setup(LCD_D6, GPIO.OUT) 
GPIO.setup(LCD_D7, GPIO.OUT) 


LCD_WIDTH = 16   
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 
LCD_LINE_2 = 0xC0 


E_PULSE = 0.0005
E_DELAY = 0.0005

LCD_SCRL_DEL = 0.14529  



def lcd_init():
    
    lcd_byte(0x33,LCD_CMD) 
    lcd_byte(0x32,LCD_CMD) 
    lcd_byte(0x06,LCD_CMD) 
    lcd_byte(0x0C,LCD_CMD) 
    lcd_byte(0x28,LCD_CMD) 
    lcd_byte(0x01,LCD_CMD) 
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
     

    GPIO.output(LCD_RS, mode) 
   
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

   
    lcd_toggle_enable()

    
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

    
    lcd_toggle_enable()

def lcd_toggle_enable():
    
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def lcd_string(message,line):
    
    message = message.ljust(LCD_WIDTH," ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)

def lcd_string_scroll(message, line, SCL_DELAY):
    string = message.strip()
    string = "               " + string
   
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


def delayms(time_in_msec):
    time.sleep( (time_in_msec/1000) )
    pass

def delaysec(time_in_sec):
    time.sleep(time_in_sec)

def enrollFingerInDB():
    print "Enroll your Finger into Fingerprint Database"
    
    
    try:
        print('Keep your finger...')

        
        while ( fingerprint_module.readImage() == False ):
            pass

       
        fingerprint_module.convertImage(0x01)

        
        result = fingerprint_module.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('This fingerprint template already exists at position number = ' + str(positionNumber))

        print('Remove your finger...')
        delaysec(2)

        print('Keep your finger again...')

        
        while ( fingerprint_module.readImage() == False ):
            pass

        
        fingerprint_module.convertImage(0x02)

       
        if ( fingerprint_module.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')

       
        fingerprint_module.createTemplate()

       
        positionNumber = fingerprint_module.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))

    except Exception as e:
        print('Enrollment fail.')
        print('Error : ' + str(e))      


   
    
    pass

def searchFingerInDB():
    print "Search your Finger into Fingerprint Database"
    
    try:
        print('Keep your finger...')

        
        while ( fingerprint_module.readImage() == False ):
            pass

        
        fingerprint_module.convertImage(0x01)

        
        result = fingerprint_module.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No fingerprint template match found.')
        else:
            print('Fingerprint found at position number = ' + str(positionNumber))
            
    except Exception as e:
        print('Searching fail.')
        print('Error : ' + str(e))

   
    pass

def deleteFingerInDB():
    print "Delete your Finger data from Fingerprint Database"
    
    try:
        positionNumber = input('Please enter the template position you want to delete (in range 0 to 1000): ')
        positionNumber = int(positionNumber)

        if ( fingerprint_module.deleteTemplate(positionNumber) == True ):
            print('Template deleted successfully.')

    except Exception as e:
        print('Deletion fail.')
        print('Error : ' + str(e))       

   
    pass

def getFingerPrintImage():
    print "Generate finger print image"
    
    try:
        print('Keep your finger... and wait for seconds')

        
        while ( fingerprint_module.readImage() == False ):
            pass
        
        fingerprint_module.downloadImage('fingerprint.bmp')
        print('The image is available in current program directory.')

    except Exception as e:
        print('Image generation fail.')
        print('Error : ' + str(e))

   
    pass

 
def helpMe():
    print "\nHelp documentation for R305 finger print module uses on Raspberry pi."

    print "\n\n\n\n\n\n\nPress any key to get out from here."
    exi = raw_input()
    print "\n"
    pass

def clearscreen():
    for i in range(50):
        print "\n"
        pass
    pass


def clearscreen(no_of_line):
    for i in range(no_of_line):
        print "\n"
        pass
    pass


def getFingerprintTemplateCount():
    clearscreen(25)
    print('Fingerprint template , in database =  ' + str(fingerprint_module.getTemplateCount()) +'/'+ str(fingerprint_module.getStorageCapacity()))
    pass

def testOnLCD():
    
    lcd_init()                
    
    try:
        lcd_string("Keep your finger          ",LCD_LINE_1)
        lcd_string("on sensor...              ",LCD_LINE_2)

        
        while ( fingerprint_module.readImage() == False ):
            pass

        
        fingerprint_module.convertImage(0x01)

        
        result = fingerprint_module.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            lcd_string("Unauthorized              ",LCD_LINE_1)
            lcd_string("person...                 ",LCD_LINE_2)
        else:
            lcd_string("Authorized                ",LCD_LINE_1)
            lcd_string("person...                 ",LCD_LINE_2)
        delaysec(3)
    except Exception as e:
        lcd_string("Failure                  ",LCD_LINE_1)
        lcd_string("searching...             ",LCD_LINE_2)
        print('Error : ' + str(e))
    lcd_string("Choose option in              ",LCD_LINE_1)
    lcd_string("Menu...                       ",LCD_LINE_2)
    




def main():
    
    clearscreen(25)
    
    choice = 0                  
    global fingerprint_module   
    
    print "Initialization done...Starting program"
    delaysec(1)
    
    while True:  
        clearscreen(25)
        print " Program to demonstrate use of fingerprint module R305 on LCD"
        print "\n\n Choose option in Menu below.\n 1.Enroll Fingerprint.\n 2.Search Fingerprint.\n 3.Delete Fingerprint.\n 4.Get Fingerprint Image.\n 5.Run Fingerprint on LCD."
        print " 6.Get fingerprint record count in Database.\n 7.Help.\n 8.Exit Program.\n\n"
        print " Enter choice: " 
        choice = int(raw_input())

        
        if choice == 1:
            enrollFingerInDB()
            pass
        
        
        if choice == 2:
            searchFingerInDB()
            pass
        
          
        if choice == 3:
            deleteFingerInDB()
            pass
        
        
        if choice == 4:
            getFingerPrintImage()
            pass
        
         
        if choice == 5:
            testOnLCD()  
            pass   
        
        
        if choice == 6:
            getFingerprintTemplateCount()
            pass
        
        
        if choice == 7:
            helpMe()
            pass

        if choice == 8:
            exit(0)
            pass

        delaysec(0.5) 
        pass     
    pass

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
