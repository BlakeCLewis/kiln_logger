# set:
#     recipient to you phone email address
#     gmail_sender to your gmail account (I set up a new account specifically for this purpose)
#     gmail_passwd
#     gmail account settings set "Less secure app access" to "on"

def send_email(subject,text):

    #your phone
    recipient = 'XXXXXXXXXXX@msg.fi.google.com'
    # Gmail Sign In
    gmail_sender = 'XXXXXXXXXX@gmail.com'
    gmail_passwd = 'XXXXXXXXXXX'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)
    msg = '\r\n'.join(['To: %s' % recipient, 'From: %s' % gmail_sender,'Subject: %s' % subject,'', text])

    try:
        server.sendmail(gmail_sender, recipient, msg)
        print ('email sent')
    except:
        print ('error sending mail')
        server.quit()

#object
class kiln_state(itp,otp):
#  track: 20 temp/timestamp/trend
#  event: STATE change|PEAK|+100C 
#       'PEAK'  if high is > 10 minutes old and trend < -15
#  state: CLIMB|HOLD|FALL
#       'HOLD'  if abs(trend) < 4
#       'CLIMB' if trend is > 6
#       'FALL'  if  trend is < -6

    def __init__(self):
        datime = time.time()
        tp = itp
        length = 20
        self.ti = deque(maxlen=length) #time
        self.ti.appendleft(datime)
        self.tp = deque(maxlen=length) #temp
        self.tp.appendleft(itp)
        self.td = deque(maxlen=length) #trend
        self.td.appendleft(0)
        self.state = 'HOLD'
        self.high = temp
        self.peak = 0
        self.peaked = False

        
    def _trending(self):
        return self.td.count(1) + self.td.count(-1)

    def _rate(self): #need to turn this into C/hour
        return (self.tp(0) - self.tp(-1)) / (self.ti(0)-self.ti(-1))

    def update(self,itp,otp):
        itp = round(itp)
        otp = round(otp)
        ti = time.time

        ddiiqq = itp - self.ti(0)
        if ddiiqq = 0:
            trend = 0
        elif ddiiqq < 0:
            trend = -1
        else:
            trend = 1
        self.tp.appendleft(itp)
        self.ti.appendleft(ti)
        self.td.appendleft(trend)

        if self.state == 'CLIMB':
            if self.high < itp:
                self.high = itp
                self.hightime = time.time
            if abs(trending()) < 4 and (self.tp(0)-self.tp(-1)) < 0 :
                self.state = 'HOLD'
                #notify
            elif (trending() < -4) and (self.tp(0) - self.tp(-1) < 0):
                self.state = 'FALL'
                #notify
            
        elif self.state == 'HOLD'
            if (trending() > 4) and (self.tp(0) - self.tp(-1) > 0):
                self.state = 'CLIMB'
                #notify
            elif (trending() < -4) and (self.tp(0) - self.tp(-1) < 0)::
                self.state = 'FALL'
                #notify

        else self.state == 'FALL'
            #need to turn this into minutes
            if 8 < (self.hightime - self.ti(0)) 
                    and (trending() < -10 
                    and ((!self.peaked) or (self.peak<self.high)):
                self.peak = self.high
                self.peaktime = self.hightime
                #report peak temp ?C @ timestamp
            if :
                self.state = 'CLIMB'
            elif :
                self.state = 'HOLD'


if __name__=='__main__':
    import smtplib
    import time
    from collections import deque
    #test msg
    send_email('rpi.kiln allgood','this is not the kiln you are looking for')

