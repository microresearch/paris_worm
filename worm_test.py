# altered for earthboot serial stream 
# NgramModel is only in nltk=
# pip install https://pypi.python.org/packages/source/n/nltk/nltk-2.0.5.tar.gz

# how to convert to slow scan->
# worming slow scan?

# screen array - add next line -length=149
# refresh

# for worm crypt - re-do also based on word probabilities...

from nltk import *
from time import sleep
import math
import random
import time
#import serial
import codecs
import os
import subprocess as sp

f = codecs.open("/root/projects/worms_paris/chants","r","utf-8")
cry = f.read()
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
        #        line = ser.read(1)
        line = random.randint(0,255)
        try:
            #nummm = ord(line)/3 # how much to divide?
            nummm = line/3
        except:
            nummm = 1
        if nummm>=len(probb):
            nummm=len(probb)-1;
        letter=probb[random.randint(0,nummm)][1]
        result=result+letter
        probb=[]
        if letter=="\n":
            return result[0:-1]
    return result[0:-1]

inpt=time.time()
#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
seedletter='e'

fullon=[]
count=0
while True: # question of timings
    # how to convert to slow scan->
    # screen array - add next line -length=149
    x=genereate(up,bm,seedletter,149) # max length of line
    fullon.append(x)
    # refresh
    tmp = sp.call('clear',shell=True)
    time.sleep(0.1)
    for fills in fullon:
        print fills #slowly print line by line?
        time.sleep(0.1) 
       
    count+=1 
    # is full then start from zero adding
    if count==50: # how many lines
        count=0
        fullon=[]
    #print x
    time.sleep(1)


    
