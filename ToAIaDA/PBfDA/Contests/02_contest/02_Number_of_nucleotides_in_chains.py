rnk_string = input()
stop_codons = ['UAA', 'UAG', 'UGA']

start = 0
codons = []
for _ in rnk_string:
    codons.append(rnk_string[start : start + 3])
    start += 3

result = []
count = 0
for codon in codons:
    if codon not in stop_codons:
        count += 3
    else:
        result.append(count if count > 0 else 0)
        count = 0

print(*result)