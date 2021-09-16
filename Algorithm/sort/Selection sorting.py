#https://yeomylaoo.tistory.com/115
#sorted


array = [7,5,9,0,3,1,6,2,4,8]

for i in range(len(array)):#0~10 
    min_index = i#0
    for j in range(i+1, len(array)):#1~10
        if array[min_index] > array[j]:#0 > len(array)
            min_index = j #min_index = 3
    array[i], array[min_index] = array[min_index],array[i] #0과 3을 스왑
print(array)