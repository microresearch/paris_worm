# altered for earthboot serial stream 

# for worm crypt - re-do also based on word probabilities...

from nltk import *
from time import sleep
import math
import random
import time
import serial
import codecs
import unicodedata

def storepickle(dc):
    out = open("death_tagged.pickle", 'wb')
    pickle.dump(dc, out)
    out.close()

def recallpickle():
    out = open("death_tagged.pickle", 'rb')
    dc=pickle.load(out) 
    out.close()
    return dc

def convert_accents(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')



#f = open("/root/projects/earthcode/worm/death_strip1.bak")
f = codecs.open("/root/Downloads/chants","r","utf-8")
cry = f.read()
#m=[y.lower() for y in cry]
#m=[convert_accents(word) for word in cry]
uf=FreqDist(l for l in cry)
up=DictionaryProbDist(uf,normalize=True)
bm=NgramModel(2,cry)

def genereate(dct,model,letter,n):
    probb=[]
    result=''
    total=''
    line=''
    for x in range(n):
        for l in dct.samples():
            prob=model.prob(l,letter)
            probb.append((prob,l))
        probb.sort()
        probb.reverse()
#        for pr in probb:
#            print codecs.encode(pr[1],"utf-8")
#        print len(probb)
        #        while len(line)<3:
        line = ser.read(1)
#        time.sleep(0.1)
 #       lline = ser.read(1)
        #        line = random.randint(0,255)
        #numm = int(line)/1000
        try:
            nummm = ord(line)/3
        except:
            nummm = 1
  #      lastnumm=ord(lline)
   #     nummm=math.fabs(lastnumm-numm)
        #        numm=random.randint(0,25)
        if nummm>=len(probb):
            nummm=len(probb)-1;
#        print numm
        letter=probb[random.randint(0,nummm)][1]
        result=result+letter
#        total=total+letter
        probb=[]
        if letter==' ':
            print result[0:-1],
            result=''
#            time.sleep(1)
        f.write("%s" % codecs.encode(letter,"utf-8"))

#    print "\r\nSaving to '%s_results.txt'" % inpt
#    f.close()

inpt=time.time()
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
#seedletter = up.samples()[random.randint(0,len(up.samples())-1)]
seedletter='e'
#print "seedletter %c" % seedletter
# ftp biz

#upappend(ftp, "worms.txt")

while True:
    randy=str(random.randint(0,12345678))
    print "xxxxxxWRiTING", randy
    f = file("/root/worms/wormy/"+randy, 'w')
    genereate(up,bm,seedletter,1024)
    f.close()
    time.sleep(4)
