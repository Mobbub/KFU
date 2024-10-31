nums = input().split()
num1 = int(nums[0])
num2 = int(nums[1])

sorted_digits1 = ''.join(sorted(str(num1)))
sorted_digits2 = ''.join(sorted(str(num2)))

if sorted_digits1 == sorted_digits2:
    print('YES')
else:
    print('NO')
