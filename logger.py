#!/usr/bin/python3
"""
kilnlogger.py -i 420 -s 30
-i assigns id to log records
-s is interval to log

requires lcd display to watch data realtime



"""
import sys, getopt
from signal import *
import os
import time
import sqlite3
from Adafruit_GPIO import SPI
from Adafruit_MAX31856 import MAX31856
from display import display

def ts(seconds):
    H=divmod(seconds,3600)
    M=divmod(H[1],60)
    S=M[1]%60
    return (str(int(H[0]))+':'+str(int(M[0]))+':'+str(int(S)))
    #return ("%3.0f:%2.0f:%2.0f"%(H[0],M[0],S))


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:s:",["runid=","seconds="])
    except getopt.GetoptError:
        print('logger.py -i <RunID> -s <seconds>')
        sys.exit(2)
    for opt, arg in opts:
       if opt == '-h' or (opt != '-i' and opt != '-s'):
          print ('logger.py -i <RunID> -s <seconds>')
          sys.exit()
       elif opt in ("-i", "--RunID="):
          RunID = arg
          print ('RunID is ', RunID)
       elif opt in ("-s", "--seconds="):
          interval_seconds = int(arg)
          print ('interval_seconds is ', interval_seconds)

    # 3 lcd lines comment out to disable, on is in the while True loop
    lcd = display()
    lcd.clear()

    SQLDB = '/home/pi/kilnlog.sqlite3'
    SQLConn = sqlite3.connect(SQLDB)
    SQLConn.row_factory = sqlite3.Row
    SQLCur = SQLConn.cursor()

    sql="INSERT INTO firelog(RunID, datime, t)VALUES(?,?,?);"

    SPI_PORT = 0
    SPI_DEVICE = 0
    sensor = MAX31856(hardware_spi=SPI.SpiDev(SPI_PORT,SPI_DEVICE))
    t_now = sensor.read_temp_c()
    print('TC: {0:0.3F}*C'.format(t_now))
    temps=[t_now, t_now, t_now]
    starttime = time.time()
    lastTime = starttime - interval_seconds
    
    while True:
        datime = time.time()
        if lastTime + interval_seconds <= datime:
            t_now = sensor.read_temp_c()
            if temps.insert(0, t_now):
                temps.pop()
            p = (RunID, time.strftime('%Y-%m-%d %H:%M:%S'), t_now)
            # 3rd lcd line
            lcd.writeLog(RunID, ts(time.time()-starttime), temps[0], temps[1], temps[2])
            print('TC: {0:0.3F}*C'.format(t_now))
            try:
                SQLCur.execute(sql, p)
                SQLConn.commit()
            except:
                SQLConn.rollback()
                print("DB Update failed!")
            lastTime=datime;
            time.sleep(interval_seconds-1)

if __name__ == "__main__":
   main(sys.argv[1:])
