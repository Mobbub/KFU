n = int(input())
blocks = list(map(int, input().split()))
water = 0
left = 0
right = n - 1
max_left = blocks[left]
max_right = blocks[right]

while left < right:
    if max_left >= max_right:
        water += max_right - blocks[right]
        right -= 1
        max_right = max(max_right, blocks[right])
    else:
        water += max_left - blocks[left]
        left += 1
        max_left = max(max_left, blocks[left])

print(water)