import csv
import numpy as np

def ratio(s, t, ratio_calc = False):
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        return distance[row][col]

sentences = open("../../Data/gali_tokenised.csv").read().split('\n')
areaList = open("delhi_local.csv").read().split('\n')

col1 = []
col2 = []
bcount = 0
icount = 0
counter = 0

for i in range(len(areaList)) :
    areaList[i] = areaList[i].split()

for i in range(len(sentences)):
    arr = sentences[i].split(',')
    col1.append(','.join(arr[0:len(arr)-1]))
    col2.append(arr[-1])

# print(len(col1))
# print(len(col2))

# for i in range(100) :
#     print(col1[i], col2[i])

for area in areaList :
    print(counter/len(areaList)*100 , ' %')
    counter+=1
    for i in range(len(area)) :
        for j in range(len(col1)) :
            a = (area[i].lower().strip()).strip('#').strip(',').strip('@')
            b = (col1[j].lower().strip()).strip('#').strip(',').strip('@')
            if (len(a)<= 4 and a==b) or (len(a) > 4 and a!='' and b!='' and ratio(a, b) < 2) :
                if i==0 :
                    if col2[j] == 'I-geo' or col2[j] == 'B-geo' :
                        pass
                    else :
                        bcount+=1
                        col2[j] = 'B-geo' 

                else :
                    if col2[j] == 'I-geo' or col2[j] == 'B-geo' :
                        pass
                    else :
                        icount+=1
                        col2[j] = 'I-geo' 

print("###############################################")
print("        Alert : Operation Successful           ")
print("###############################################")

with open('acc_output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(len(col1)) :
        writer.writerow([col1[i], col2[i]])