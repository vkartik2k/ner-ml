import csv
import random
import string

f = open("new_data.tsv", "r")
curr = []
finalSentences = []
sentences = []

for x in f:
    finalSentences.append(x)
sentences = list(set(finalSentences))

print(sentences)

with open('acc.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(len(sentences)) :
        writer.writerow([sentences[i][:-2]])

print('DONE')