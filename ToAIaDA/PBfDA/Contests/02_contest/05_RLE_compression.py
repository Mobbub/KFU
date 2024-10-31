def rle_encode(input_string):
    encoded_string = ""
    count = 1
    
    for i in range(len(input_string)):
        if i == len(input_string) - 1 or input_string[i] != input_string[i + 1]:
            encoded_string += input_string[i] + str(count) if count > 1 else input_string[i]
            count = 1
        else:
            count += 1
    
    return encoded_string

data = input()
print(rle_encode(data))