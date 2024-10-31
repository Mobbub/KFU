def find_most_frequent(numbers):
    frequency = {}
    
    for num in numbers:
        if num in frequency:
            frequency[num] += 1
        else:
            frequency[num] = 1
    
    most_frequent = max(frequency, key=frequency.get)
    
    return most_frequent

trash = int(input())
my_list1 = input().split()
my_list = []
for i in my_list1:
    my_list.append(int(i))
print(find_most_frequent(my_list))
