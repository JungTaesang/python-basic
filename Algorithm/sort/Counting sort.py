


array = [7,5,9,0,3,1,6,2,9,1,4,8,0,5,2]

Count = [0] * (max(array)+1)

for i in range(len(array)):
    Count[array[i]] +=1

print(Count)
print(len(Count))
for i in range(len(Count)):
    for j in range(Count[i]):
        print(i, end=' ')

