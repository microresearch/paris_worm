# HOWTO : prepare text using pickletext.py, add worms, doallworms

import random
import math
import nltk
#import matplotlib.pyplot as plt
import pickle
import collections
import functools
import itertools
import sys, pygame


cmudict = nltk.corpus.cmudict.dict()
#plotter=[]

def rhyme(a, b):
    if a.lower() not in cmudict or b not in cmudict or a == b:
        return False
    wsa = list(reversed(cmudict[a.lower()][0]))
    wsb = list(reversed(cmudict[b.lower()][0]))
    return len(list(itertools.takewhile(lambda x: x[0] == x[1], zip(wsa, wsb)))) >= min(2, len(list(wsa)))

def recallpickle(where):
    out = open(where, 'rb')
    text=pickle.load(out) 
    out.close()
#    testtext(text)
    return text
    
def testtext(text):
    for line in text:
       for word in line:
          if len(word) != 2:
             print(word)

def randy(num):
    return random.randrange(0, num, 1)

def randyx(xnum,num):
    x= None
    while x==xnum or x is None:
        x= randy(num)
    return x

def rrr(ranger):
    r= (random.uniform(ranger/-2, ranger/2),random.uniform(ranger/-2, ranger/2)) 
    return r;

def normalize(tup):
    x=tup[0]
    y=tup[1]
    mag=math.sqrt(x*x + y*y)
    if mag!=0:
        x=x/mag
        y=y/mag
    return (x,y)

def limit(tup,limit):
    x=tup[0]
    y=tup[1]
#   (magSq() > max*max) { normalize(); mult(max); 
    if math.sqrt(x*x + y*y) > limit*limit:
        (x,y)=normalize(tup)
        x=x*limit
        y=y*limit
    return (x,y)

def matchonlyfirst(matchone,matchtwo): # just return the first word - also used for testing
    ll=matchone()
    return ll

def matchswop(matchone,matchtwo): # swop words
    if randy(100)>50:
        return matchone()
    else:
        return matchtwo()

#BUG FIX: otherpos and pos are not the same type (pos vs location)
def matchpos(matchone,matchtwo): # look for match
    count=0
    pos= matchone()[1] # [1] is pos
    otherpos=""
    while otherpos != pos and count<100: # TODO: redo with match function - match(this,that) eg use matchone()[0]
        count+=1
        other=matchtwo()
        otherpos=other[1]
    return other

#BUG FIX: wordone and wordtwo are not the same type
def matchrhyme(matchone,matchtwo): # look for match
    count=0
    wordone= matchone()[0] # [0] is word
    wordtwo="xxx"
    while (not rhyme(wordone,wordtwo)) and count<100: # TODO: redo with match function - match(this,that) eg use matchone()[0]
        count+=1
        other=matchtwo()
        wordtwo=other[0]
    return other

class worm():
    compost_stack = -1
    compost = []
    
    #list of full worms (worms that have partners)
    fullworms=[]
    simplecompost=[]

    def __init__(self, loc, speed, maxspeed, textpickle, wormtype, matchfunc, partner, partnerloc, partnerspeed, partnerpickle, partnertype):
        self.loc = loc
        self.speed = speed
        self.trail = 8 # set by type of worm
        self.acc=(0,0)
        self.vel=(0,0)
        #        self.ww = 2400 # or this is based on text/pickle but per line so...
        #self.wh = 2400 # or this is based on text/pickle but per line so...
        self.maxspeed = maxspeed
        self.tail = []
        self.equalized_tail = []  
        self.counter = 0
        self.tailcount=0
        self.dir=(7,-4) # change this
        self.SW=1
        self.target=(0,0)
        # dict of worm types with functions, what else?
        self.wormdict =  { 
            'basicworm': self.wander,
            'bookworm':self.reader,
            'straightworm':self.straight,
            'seeker':self.seek,
            'squiggler':self.squiggler
        }

        self.function=self.wormdict[wormtype]
        # also need holes, targets and so on TODO maybe as dictionary or as part of text itself
#        self.composter=0 #not in use
        self.matchfunc=matchfunc
#        for w in range(self.trail):
#            self.tail.append((self.loc[0],self.loc[1]-w))

        worm.compost_stack += 1
        self.stack=worm.compost_stack
        worm.compost.append([])
        if textpickle == "COMPOST":
#            self.composter=randyx(self.stack,worm.compost_stack) # but not itself #not in use
            self.text=worm.simplecompost
        else: 
            self.text = recallpickle(textpickle) 
        self.init_tail()   
        if partner==None:
            self.partner=worm(partnerloc,partnerspeed,maxspeed,partnerpickle,partnertype,None,"Some",0,0,0,0) 
            worm.fullworms.append(self)    

    #Initialize tail of worms and draw each worm on the screen
    def init_tail(self):
        for w in range(self.trail):
            self.tail.append((self.loc[0],self.loc[1]-w))
        self.equalized_tail = self.equalize_x_and_y()
        pygame.draw.lines(screen, black, False, self.equalized_tail, 1)
        pygame.display.update()

    #Equalize tail for display => change scale of x and y coordinates
    def equalize_x_and_y(self):
        equalized_tail = []
        for w in range(self.trail):
            if len(self.text) > 0:
                equalized_x = self.tail[w][0]*640/len(self.text[int(self.loc[1])])
                equalized_y = self.tail[w][1]*640/len(self.text)
                equalized_tail.append((equalized_x, equalized_y))
            else:
                equalized_tail.append((0,0))
            #returns empty array for empty compost
        return equalized_tail

    def checkdist(self):
        dis=(self.target[0]-self.loc[0],self.target[1]-self.loc[1]) 
        if dis[0]>self.ww/2: # need always to recalc this
            self.acc=(self.acc[0] * -1, self.acc[1])
        if dis[0]>self.wh/2:
            self.acc=(self.acc[0], self.acc[1]* -1)

    def do_tail(self):
        self.tail[self.trail-1]=(self.loc[0],self.loc[1])
        for w in range(self.trail-1):
            self.tail[w]=self.tail[w+1]

    #Move each worm on display according to current location => shift entire tail
    def move_worm(self):
        pygame.time.delay(100)
#        equalized_tail = self.equalize_x_and_y()
        pygame.draw.lines(screen, white, False, self.equalized_tail, 1)
        for w in range(self.trail-1):
            self.tail[w+1]=self.tail[w]
        self.tail[0]=(self.loc[0],self.loc[1])
        self.equalized_tail = self.equalize_x_and_y()
        pygame.draw.lines(screen, black, False, self.equalized_tail, 1)
        self.erase_gaps()
        pygame.display.update()

    def erase_gaps(self):
        #erase lines connecting gaps - for bookworm
        for w in range(self.trail-1):
            if abs(self.tail[w+1][1] - self.tail[w][1])>=len(self.text) or abs(self.tail[w+1][0] - self.tail[w][0])>=len(self.text[int(self.loc[1]-1)])-1:
                pygame.draw.lines(screen, white, False, [self.equalized_tail[w], self.equalized_tail[w+1]], 1)
            
    def word_at(self,loc):
        # check x and y for self.text
        wh = len(self.text)-1 # number of lines 
        if int(loc[1])>wh:
            loc=(loc[0],0)
        if loc[1]<0:
            loc=(loc[0],wh)
        line=self.text[int(loc[1])]
        ww=len(line)-1
        if ww>0:
            if int(loc[0])>ww:
                loc=(0,loc[1])
            if loc[0]<0:
                loc=(ww-1,loc[1])
        else:
            loc=(0,loc[1])
        word=line[int(loc[0])]
        return word

    def tailword(self):
        # runfunc/do_tail/cycle through word at tail
        self.tailcount+=1
        if self.tailcount>=self.trail-1:
            self.tailcount=0
        self.wander() # or another function - how to specify tail as on/off?
        self.do_tail()
        return self.word_at(self.tail[self.tailcount])

    def checky(self):
        self.wh = len(self.text)-1 # number of lines 
        if int(self.loc[1])>self.wh:
            if self.function == self.reader:
                self.loc=(self.loc[0],0) #reach bottom and appear at top
            else: #change direction
                self.acc=(self.acc[0],-self.acc[1])
                self.vel=(0,0)
                self.loc=(self.loc[0],self.wh)
        if self.loc[1]<0:
            if self.function == self.reader:
                self.loc=(self.loc[0],self.wh) #reach top and appear at bottom
            else: #change direction
                self.acc=(self.acc[0],-self.acc[1])
                self.vel=(0,0)
                self.loc=(self.loc[0],0)

    def checkx(self):
        if self.ww>0:
            if int(self.loc[0])>self.ww:
 #               self.loc=(0,self.loc[1])  #reach right and appear in left
                self.acc=(-self.acc[0],self.acc[1])
                self.vel=(0,0)
                self.loc=(self.ww,self.loc[1])
            if self.loc[0]<0:
 #              self.loc=(self.ww-1,self.loc[1])  #reach left and appear in right
                self.acc=(-self.acc[0],self.acc[1])
                self.vel=(0,0)
                self.loc=(0,self.loc[1])
        else:
            self.loc=(0,self.loc[1])
    
    def updatelocation(self):
        self.vel = (self.vel[0] + self.acc[0], self.vel[1] + self.acc[1])
        self.vel=limit(self.vel,self.maxspeed)
        self.loc = (self.loc[0]+self.vel[0], self.loc[1]+self.vel[1])
        self.checky()
        line=self.text[int(self.loc[1])]
        self.ww=len(line)-1
        self.checkx()
        return line[int(self.loc[0])]


    def doallworms(self):
        for worms in self.fullworms:
            word = ""
            pos = ""
            loc = (0,0)
            if len(worms.text)>1:
                #list for compost
                otherlist=[]
                while pos!="NL":
                    # match with otherother according to function eg. posmatch, rhyming 
                    word,pos,loc=worms.matchfunc(worms.function, worms.partner.function)
                    print (word, (int(loc[0]),int(loc[1])))
                    otherlist.append((word,pos))
                    #                worm.compost[self.stack].append(otherlist)
                worm.simplecompost.append(otherlist)
#                print worm.simplecompost
                #                print worms.function,
                # if worms.textpickle=="COMPOST":
                #     print " ".join([x[0] for x in otherlist]),
#                print " ".join([x[0] for x in list]),

    def wander(self):
        self.acc = (self.acc[0] + random.uniform(-2,2), self.acc[1] + random.uniform(-2,2))
        self.acc=normalize(self.acc)
        self.acc = (self.acc[0] * self.speed, self.acc[1] * self.speed)
        word,pos=self.updatelocation()
        self.move_worm()
        return (word,pos,self.loc) # returns word, POS and location

    def reader(self): # walk text at speed, without any acceleration
        self.checky()
        self.loc=(self.loc[0]+self.speed, self.loc[1])
        if self.loc[0]>=len(self.text[int(self.loc[1])]):
            self.loc=(0, self.loc[1]+1)
            if self.loc[1]>=self.wh:
                self.loc=(0, 0) # circulate back to start
        line=self.text[int(self.loc[1])]
        word,pos=line[int(self.loc[0])]
        self.move_worm()
        return (word,pos,self.loc) # returns word, POS and location

    def straight(self):
        self.acc = (self.dir[0],self.dir[1])
        rrrr=rrr(80)
        self.acc = (self.acc[0]+rrrr[0], self.acc[1]+rrrr[1])
        self.acc=normalize(self.acc)
        self.acc = (self.acc[0] * self.speed, self.acc[1] * self.speed)
        word,pos=self.updatelocation()
        self.move_worm()
        return (word,pos,self.loc) # returns word, POS and location

    def squiggler(self):
        self.counter = self.counter + 1;
        rot = math.sin(self.counter) * self.SW
        z = (self.acc[0] * math.cos(rot) - self.acc[1] * math.sin(rot), self.acc[0] * math.sin(rot) + self.acc[1] * math.cos(rot))
        self.acc = (self.dir[0],self.dir[1])
        self.acc = (self.acc[0] + z[0], self.acc[1] + z[1])
        word,pos=self.updatelocation()
        self.move_worm()
        return (word,pos,self.loc) # returns word, POS and location
    
    #BUG FIX: not indexing into tuple when comparing with forms of worm
    #BUG FIX: var names unaligned => not returning correct tuple form within first if statement
    def seek(self):
        if self.target == (0,0):
            word,pos,loc=self.wander()
            if word=="worm" or word=="Worm" or word=="WORM" or word=="worms" or word=="Worms":
                self.target=loc
            return (word,pos,loc) # returns word, POS and location
        else: # move towards target
            self.acc=(self.target[0]-self.loc[0], self.target[1]-self.loc[1])
            self.acc=normalize(self.acc)
            rrrr=rrr(2)
            self.acc = (self.acc[0]+rrrr[0], self.acc[1]+rrrr[1])
            self.acc=normalize(self.acc)
            line=self.text[int(self.loc[1])]
            self.ww=len(line)-1
            self.checkdist() ### ????
            self.acc = (self.acc[0] * self.speed, self.acc[1] * self.speed)
            word,pos=self.updatelocation()
            self.move_worm()
            return (word,pos,self.loc) # returns word, POS and location
 
# TODO diff movements -> move randomly then towards targetsDONE, move
# away from targets, up and then down=reflect, establish wormholes ->
# how these work - through to different worms, texts///stack of texts, compost buffer

# below example which rewrites straight read text with wormed POS
# how to make more generic - worm interaction?

SCREEN_DIM=640
random.seed()
loc=(randy(20),randy(20))
loc2=(randy(20),randy(20))
speed=1
maxspeed=2

# 'basicworm': self.wander,
# 'bookworm':self.reader,
# 'straightworm':self.straight,
# 'seeker':self.seek,
# 'squiggler':self.squiggler

# firstworm=worm(loc,speed,maxspeed, "conqueror_pickle", 'bookworm',matchonlyfirst, None, loc,speed,"lusus_serius_maier_pickle","bookworm")
# firstworm.doinit()

# for x in xrange(10):
#     firstworm.doallworms()

# for x in xrange(400):
#     print firstworm.tailword()[0],

# test random worm 

# TESTING: list of texts, list of worms, list of functions
def test_worms():
    textlist=["fullblake_pickle","conqueror_pickle","lusus_serius_maier_pickle","beddoesvoll_pickle","prematureburial_pickle","usher_pickle","death_pickle","COMPOST"]
    wormlist=['basicworm','bookworm','straightworm', 'seeker', 'squiggler']
    funclist=[matchonlyfirst,matchpos,matchrhyme,matchswop]

    wormyy=[]
    for x in range(5):
        loc=(randy(20),randy(20))
#        wormyy.append(worm(loc,speed,maxspeed, random.choice(textlist), random.choice(wormlist),random.choice(funclist),None,loc,speed,random.choice(textlist), random.choice(wormlist)))
        wormyy.append(worm(loc,speed,maxspeed, "fullblake_pickle", random.choice(wormlist),random.choice(funclist),None,loc,speed,"conqueror_pickle", random.choice(wormlist)))

    for x in range(100):
        wormyy[0].doallworms()

screen = pygame.display.set_mode((SCREEN_DIM,SCREEN_DIM))
white = (255,255,255)
black = (0,0,0)
screen.fill(white)
pygame.display.update()
test_worms()


####///////////////////////////////////////////////////////////////////

#glowworm.do_tail()
#for x in xrange(1000):
#    print glowworm.function()[0][0],

# testing plot of movements - seems okayyy...

# xx=[]
# yy=[]
# for x in xrange(1000):
#     pp=firstworm.function()
#     xx.append(pp[1][0])
#     yy.append(pp[1][1])
# plt.plot(xx,yy)
# plt.show()
# print test

####///////////////////////////////////////////////////////////////////

# TODO: different types of worms - menagerie each with its emblem

# wormholes, wormholes on POS and words

# worm ideas - rising up and descending, worm-holes,
# glowing=what, segmented worms drag words, other worms make holes

# annotate with wormholes and targets/escapes

# emblems as part of text?

####///////////////////////////////////////////////////////////////////

# ideas/TODO...

# 5/4: 

# re-worm markov chain probabilities or subject wormed movement text to markov chains
# movement of worms on rhymes

# 6/4 fixes for lengths and so on, random selections

# could maybe have simpler compost as can't write to own compost, or how to move between layers -> simplecompost implemented

# TODO: wormholes, rising/descending worms, move by rhymes, markov functions/reworking, segmented word worms-done but how to do for each function
# wormhole jumps to different position - wormhole OVERLAY// concept of overlays

# seperate out partners... DONE

# 13/4 - TODO as above // tests as seems all a bit OFF and add tailed functions, also syllabic matching and how to _and_ matches like pos and ryhmes

#CHANGES BY MARIE

#Decompose / style changes

#1. Remove doinit and initialize self.text when creating the new worm

#2. Remove self.wormlist => only need to use self.fullworms

#3. Change (word, loc) in worm type functions to (word, pos, loc) => better readability in matchfunctions

#4. Add Updatelocation as helper function to worm functions

#Bug Fixes (see above functions)

#posmatch: otherpos and pos are not the same type (pos vs location)

#rhymematch: wordone and wordtwo are not the same type

#seek: not indexing into tuple when comparing with forms of worm

#seek: var names unaligned => not returning correct tuple form within first if statement