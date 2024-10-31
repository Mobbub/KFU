seq = input().lower()
response = 'YES' if seq[::-1] == seq else 'NO'
print(response)