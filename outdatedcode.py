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

    def do_tail(self):
        self.tail[self.trail-1]=(self.loc[0],self.loc[1])
        for w in range(self.trail-1):
            self.tail[w]=self.tail[w+1]
            
#in class worm - outdated
        compost_stack = -1
        compost = []
#deleted initialization in worms - outdated
        worm.compost_stack += 1
        self.stack=worm.compost_stack
        worm.compost.append([])
        for w in range(self.trail):
            self.tail.append((self.loc[0],self.loc[1]-w))
        if textpickle == "COMPOST":
            self.composter=randyx(self.stack,worm.compost_stack) # but not itself #not in use
        self.composter=0


#OLD TEST
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