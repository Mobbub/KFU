words = input().split()

for i, item in enumerate(words):
    if item == 'end':
        words = words[:i]
        break

word_counts = {}
for word in words:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1
repeated_words = sorted([word for word, count in word_counts.items() if count > 1])

print(*repeated_words)