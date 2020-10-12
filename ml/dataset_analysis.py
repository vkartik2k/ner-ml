list1 = []

f = open("Dataset/shuffled.csv", "r")
curr = []
for x in f:
    if "Sentence #" in x:
        if curr != [] :
            list1.append(curr)
        curr = []
    else :
        # x = x[0:len(x)-1]
        y = x.strip('\n').split(',')
        if y[1]!='':
            curr.append(y)

print("No. of sentences : ", len(list1))

sum = 0
for i in list1:
    sum += len(i)

print("Sum of tokens : ", sum)

l = []

for i in list1:
    count = 0
    for j in i:
        if j[1]=='B-LOC' or j[1]=='I-LOC':
            count+=1
        else :
            if count>0:
                l.append(count)
            count = 0

# print(l)

sum = 0
for i in l:
    sum += i
print("Avg. address length : ", sum/len(l))

l = []

for i in list1:
    count = 0
    for j in i:
        if j[1]=='I-LOC':
            count+=1
        elif j[1]=='B-LOC':
            if count>0: 
                l.append(count)
            count = 1
        else :
            if count>0: 
                l.append(count)
            count = 0


# print(l)
sum = 0
for i in l:
    sum += i
print("Avg. address length of small: ", sum/len(l))


# print(len(X))

sum = 0
for i in list1:
    sum += len(i)
print("Avg. len : ", sum/len(list1))