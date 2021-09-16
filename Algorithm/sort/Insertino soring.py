array = [7,5,9,0,3,1,6,2,4,8]

for i in range(1, len(array)): #1~10
    for j in range(i,0,-1):  #1~0 , -1
        if array[j] < array[j-1]: #1 < 0 
            array[j],array[j-1] = array[j-1],array[j] #1과 0을 스왑
        else:
            break
print(array)

