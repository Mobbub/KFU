num = int(input())
numbers = [int(x) for x in input().split()]
unique_numbers = set(numbers)
print(len(unique_numbers))