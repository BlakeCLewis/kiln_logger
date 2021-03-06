"""
this class is used in main program pilnfired.py
it can be run standalone 'python3 display.py' to test display w/ mock data 
"""

import sys
import RPi.GPIO as GPIO
import spidev
from RPLCD.i2c import CharLCD
from itertools import cycle

class display(CharLCD):
    def __init__(self):
        CharLCD.__init__(self,i2c_expander='PCF8574', address=0x27, port=1,
            cols=20, rows=4, dotsize=8, charmap='A02',
            auto_linebreaks=False, backlight_enabled=True
        )
        smile=(0b00000,0b01010,0b01010,0b00000,0b10001,0b10001,0b01110,0b00000)
        degre=(0b01100,0b10010,0b10010,0b01100,0b00000,0b00000,0b00000,0b00000)
        bksls=(0b00000,0b10000,0b01000,0b00100,0b00010,0b00001,0b00000,0b00000)
        self.create_char(0, smile) #\x00
        self.create_char(1, degre) #\x01
        self.create_char(2, bksls) #\x02
        self._wheeley = '-','\x02','|','/','\x00'
        self._wheel = cycle(self._wheeley)
        self.blank20 = '                    '

    def writeFire(self,State,ID,Seg,ReadT,TargT,RampT,ETR):

        line0 = str(State) + '                   '

        line1a = 'Pr ' + str(ID) + '      '
        line1b = 'Sg ' + str(Seg) + ' ' + str(next(self._wheel)) + '   '
        line1 = line1a[0:11] + line1b[0:9]

        line2a = 'Tm ' + str(int(ReadT)) + '\x01C  '
        line2b = 'Rp ' + str(int(RampT)) + '\x01  '
        line2 = line2a[0:11] + line2b[0:10]

        line3a = 'Tr ' + str(int(TargT)) + '\x01C   '
        line3b = ETR
        line3 = line3a[0:11] + line3b[0:8]

        self.cursor_pos = (0, 0)
        self.write_string(line0[0:19])
        self.cursor_pos = (1, 0)
        self.write_string(line1[0:19])
        self.cursor_pos = (2, 0)
        self.write_string(line2[0:19])
        self.cursor_pos = (3, 0)
        self.write_string(line3[0:19])

    def writeIdle(self,ReadT0,ReadI0,ReadT1,ReadI1):
        line0='IDLE: ' + next(self._wheel) + '             '
        line1='T0 ' + str(int(ReadT0)) + '\x01C  ' + str(int(ReadI0)) + '\x01C     '
        line2='T1 ' + str(int(ReadT1)) + '\x01C  ' + str(int(ReadI1)) + '\x01C     '
        #line3='T2 ' + str(int(ReadT2)) + '\x01C  ' + str(int(ReadI2)) + '\x01C     '

        self.cursor_pos = (0, 0)
        self.write_string(line0[0:19])
        self.cursor_pos = (1, 0)
        self.write_string(line1[0:19])
        self.cursor_pos = (2, 0)
        self.write_string(line2[0:19])
        #self.cursor_pos = (3, 0)
        #self.write_string(line3[0:19])

    def writeLog(self,RunID,dastrtime,temp0,temp1,temp2):
        line0='ID:' + str(RunID) + '  ' + dastrtime
        line1='Tnow ' + str(round(temp0,1)) + '\x01C     '
        line2='Tn-1 ' + str(round(temp1,1)) + '\x01C     '
        line3='Tn-2 ' + str(round(temp2,1)) + '\x01C     '

        self.cursor_pos = (0, 0)
        self.write_string(line0[0:19])
        self.cursor_pos = (1, 0)
        self.write_string(line1[0:19])
        self.cursor_pos = (2, 0)
        self.write_string(line2[0:19])
        self.cursor_pos = (3, 0)
        self.write_string(line3[0:19])


if __name__=='__main__':
    from signal import *
    import os
    import RPi.GPIO as GPIO
    from time import sleep
    #from display import display
    duh=display()

    def clean(*args):
        print('doing the cleanup')
        duh.close(clear=True)
        os._exit(0)
    for sig in (SIGABRT, SIGINT, SIGTERM):
        signal(sig, clean)

    for i in range(8):
        duh.writeFire('Running',19,2,556+i*4,1315,108,'10:00:10')
        print ('')
        sleep(3)

    for i in range(8):
        duh.writeIdle(1222+i*2,20,1225+1*2,20)
        print ('')
        sleep(3)

    duh.close(clear=True)

    clean()

