import csv

f = open("Final/covid.csv", "r")
curr = []
finalSentences = []
for x in f:
    if "Sentence #" in x:
        if curr != [] :
            finalSentences.append(curr)
        curr = []
    else :
        y = x.split(',')
        curr.append(y)

col1 = []
col2 = []

count = 0
for i in finalSentences:
    col1.append('Sentence #'+ str(count))
    col2.append('')
    count +=1
    for j in i:
        if len(j) == 2:
            col1.append(j[0])
            col2.append(j[1][:-1])

with open('acc.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(len(col1)) :
        writer.writerow([col1[i], col2[i]])

print('DONE')