import serial
import time
import requests
import signal

MDEK_CNT = 4
TagEA = 3
acm=[None] * (MDEK_CNT)
connected_MDEK = [None] * (MDEK_CNT)
tagName = ['D720','8709','598D']
anchor = 0

"""
1st : 20
2nd : 23
3rd : 24
4th : 25
"""

acm[0] = serial.Serial("/dev/ttyACM0",115200,timeout=2)
acm[1] = serial.Serial("/dev/ttyACM1",115200,timeout=2)
acm[2] = serial.Serial("/dev/ttyACM2",115200,timeout=2)
acm[3] = serial.Serial("/dev/ttyACM3",115200,timeout=2)

#######################################################
def isAllSet(name):                                   #
    isSet = True;                                     #
    for i in range(MDEK_CNT):                         #
        if(len(name[i])<4):                           #
            isSet = False                             #
    return isSet                                      #
#######################################################

#######################################################
def SIGHandler(signum,frame):                         #
    	acm1.write('\r')                              #
	acm2.write('\r')                                  #
	acm3.write('\r')                                  #
	acm1.write('quit')                                #
	acm2.write('quit')                                #
	acm3.write('quit')                                #
	acm1.write('\n')                                  #
	acm2.write('\n')                                  #
	acm3.write('\n')                                  #
	print('System down...')                           #
	sys.exit()                                        #
#######################################################

#######################################################
def swap(tags,name):                                  #
    if(name[0]==tagName[0]):                          #
        if(name[1]==tagName[2]):                      #
            temp = tags[1]                            #
            tags[1] = tags[2]                         #
            tags[2] = temp                            #
    elif(name[0]==tagName[1]):                        #
        if(name[1]==tagName[0]):                      #
            temp = tags[1]                            #
            tags[1] = tags[0]                         #
            tags[0] = temp                            #
        elif(name[2]==tagName[0]):                    #
            temp = tags[2]                            #
            temp1 = tags[1]                           #
            tags[2] = tags[1]                         #
            tags[0] = temp                            #
            tags[1] = temp1                           #
    elif(name[0]==tagName[2]):                        #
        if(name[1] == tagName[0]):                    #
            temp = tags[1]                            #
            temp1 = tags[0]                           #
            tags[1] = tags[2]                         #
            tags[0] = temp                            #
            tags[2] = temp1                           #
        elif(name[2]==tagName[0]):                    #
            temp = tags[2]                            #
            tags[2] = tags[0]                         #
            tags[0] = temp                            #
    return tags                                       #
#######################################################

time.sleep(3)
print('This is time for get Status')

while True:
    
    for i in range(MDEK_CNT):
        acm[i].write('\r')
    time.sleep(0.5)

    for i in range(MDEK_CNT):
        acm[i].write('\r')
    time.sleep(1)

    for i in range(MDEK_CNT):
        acm[i].flushInput()
        acm[i].flushOutput()
    time.sleep(1)

    for i in range(MDEK_CNT):
        acm[i].write('si')
        acm[i].write('\n')
    time.sleep(1)

    for i in range(MDEK_CNT):
        for j in range(3):
            connected_MDEK[i] = acm[i].readline()
        connected_MDEK[i] = connected_MDEK[i][53:57]

    if(isAllSet(connected_MDEK)==True):
        for i in range(MDEK_CNT):
            print("CONNECTED MDEK ID is " + str(i+1) +":" + connected_MDEK[i])
        break

for i in range(0,len(connected_MDEK)):
    if connected_MDEK[i] in tagName:
        pass
    else:
        anchor = i

acm.remove(acm[anchor])
connected_MDEK.remove(connected_MDEK[anchor])

acm = swap(acm,connected_MDEK)
print(connected_MDEK)
print("--------------------------COMPLETE INIT SERIAL PORTS--------------------------")

for i in range(TagEA):
    acm[i].write('les')
time.sleep(0.3)

for i in range(TagEA):
    acm[i].write('\n')

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

while True:
    d0 = acm[0].readline()
    d1 = acm[1].readline()
    d2 = acm[2].readline()
    
    d0 = d0[21:25]
    d1 = d1[21:25]
    d2 = d2[21:25]

    print(" ")
    print(" ")
    print("distance 1 : " + d0)
    print(" ")
    print(" ")
    print("distance 2 : " + d1)
    print(" ")
    print(" ")
    print("distance 3 : " + d2)
    print(" ")
    print(" ")
    print("-----------------------------------------")

    data = {
            'ID' : 'First',
            'RA' : d0,
            'RB' : d1,
            'RC' : d2
        }
    headers = {'Content-Type' : 'application/json','Accept' : 'text/plain'}
    response = requests.post("http://192.168.0.4:3000/getData",data=json.dumps(data),headers=headers)
    print(response)

    
    signal.signal(signal.SIGTSTP,SIGHandler)