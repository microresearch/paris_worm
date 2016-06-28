import textdata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from textclean.textclean import textclean
import pickle
import nltk
import re

def storepickle(text,where):
    out = open(where, 'wb')
    pickle.dump(text, out)
    out.close()

listy=[]
senslist=[]
# raw = open("../texts/conquerorworm").read()
raw = open("../texts/death_strip2").read()
cleaned = textclean.clean(raw)

listy=textdata.textlines(cleaned, noblanks=True, dedent=True, lstrip=False, rstrip=True, join=False)
#print listy, len(listy)

for lists in listy:
    if len(lists)>0: # no empty line
        lists=re.sub("\d+", "", lists) # remove numbers
        #    sens = [word.lower() 
        #            for word in nltk.sent_tokenize(lists)] 
        sens=nltk.sent_tokenize(lists)
        senslist.append(sens)

fullsentt=[]
for sensy in senslist:
    sentt=[]
    for sen in sensy:
	sentt += nltk.pos_tag(nltk.word_tokenize(sen))
    sentt.append(("\n","NL")) # adds newline POS!
    fullsentt.append(sentt)

#print fullsentt

storepickle(fullsentt,"death_pickle")

#for line in fullsentt:
#    print line
