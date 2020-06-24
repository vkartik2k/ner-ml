import csv
import numpy as np
def ratio(s, t, ratio_calc = True):
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
        return "The strings are {} edits away".format(distance[row][col])


sentences = open("acc_out.csv").read().split('\n')
areaList = open("delhi_local.csv").read().split('\n')

for i in range(len(areaList)) :
    areaList[i] = areaList[i].split()

col1 = []
col2 = []

for i in range(len(sentences)):
    arr = sentences[i].split(',')
    col1.append(','.join(arr[0:len(arr)-1]))
    col2.append(arr[-1])

# print(len(col1))
# print(len(col2))

# for i in range(100) :
#     print(col1[i], col2[i])

bcount = 0
icount = 0

for area in areaList :
    for i in range(len(area)) :
        for j in range(len(col1)) :
            if ratio(area[i], col1[j]) > 0.85 :
                if i==0 :
                    # B-geo
                    if col2[j] == 'I-geo' or col2[j] == 'B-geo' :
                        pass
                    else :
                        bcount+=1
                        col2[j] = 'B-geo' 

                else :
                    # I-geo
                    if col2[j] == 'I-geo' or col2[j] == 'B-geo' :
                        pass
                    else :
                        icount+=1
                        col2[j] = 'I-geo' 

print(bcount)
print(icount)

with open('acc_out_real.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(len(col1)) :
        writer.writerow([col1[i], col2[i]])