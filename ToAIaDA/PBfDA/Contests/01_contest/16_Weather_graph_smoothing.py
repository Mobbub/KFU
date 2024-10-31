temperatures = []
smoothed = []

num123123213 = int(input())
nums = input().split()

for num in nums:
	temperatures.append(int(num))

smoothed.append(float(temperatures[0]))

for i in range(1, len(temperatures)-1):
    avg = (temperatures[i-1] + temperatures[i] + temperatures[i+1]) / 3
    smoothed.append(avg)

smoothed.append(float(temperatures[-1]))

print(*smoothed)