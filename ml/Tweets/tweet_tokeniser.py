import pandas as pd
import numpy as np
import re
import nltk

list1 =open("covid_tweets.tsv").read().split('\n')
sentences = []

for i in list1 :
    print(nltk.word_tokenize(i))
    
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
    final.append(nltk.word_tokenize(i))


print(final)
# arr = []
# for sentence in sentences:
#     temp = sentence.split()
#     temp2 = []
#     for i in temp:
#         j = i.strip('\'').strip('\"').strip('#').strip('(').strip(')').strip('@').strip('.').strip(',').strip('?')
#         j = j.strip('\'').strip('\"').strip('#').strip('(').strip(')').strip('@').strip('.').strip(',').strip('?')
#         j = j.strip('\'').strip('\"').strip('#').strip('(').strip(')').strip('@').strip('.').strip(',').strip('?')
#         j = j.strip('\'').strip('\"').strip('#').strip('(').strip(')').strip('@').strip('.').strip(',').strip('?')
#         j = re.split('; |, |- |\? |: |\'',j)
#         for k in j:
#             ert = k
#             k = ""
#             for s in ert:
#                 if s=='.' :
#                     k += ' . '
#                 else :
#                     k += s

#             if k != "":
#                 temp2.append(k)

#     arr.append(' '.join(temp2))

# sentences = arr

# print(sentences)
