import pandas as pd
import numpy as np
import re
import nltk

list1 =open("covid_tweets.tsv").read().split('\n')
sentences = []
    
charset = " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,-_()[]{}!?:;#'\"/\\%$`&=*+@^~|"

for i in list1 :
    sentences += i.split('    ')

ans = []
for sentence in sentences:
    newSentence = ""
    for i in sentence :
        if i in charset :
            newSentence += i
    ans.append(newSentence)

sentences = ans

final = []
for sentence in sentences :
    final.append(' '.join(nltk.word_tokenize(sentence)))

print(final)
