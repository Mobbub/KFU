import csv

def load(name_file):
    dict_data = {}
    with open(name_file, mode='r') as file:
        spamreader = csv.DictReader(file, delimiter=';')
        schet = 0
        for row in spamreader:
            dict_data[schet] = {
                'salary': float(row['salary']),
                'request': float(row['request']),
                'repaid': float(row['repaid ']) 
            }
            schet+=1
            
    return dict_data

def train(data):
    ws = 0
    wr = 1
    b = 1
    k = 0.01
    
    flag = 1
    while flag != 0:
        flag=0
        for key, value in data.items():
            z = data[key]['salary'] * ws + data[key]['request'] * wr - b
            if z >= 0:
                y = 1
            else:
                y = 0
            if data[key]['repaid'] - y != 0:
                flag+=1
                ws = ws + data[key]['salary'] * (data[key]['repaid'] - y) * k
                wr = wr + data[key]['request'] * (data[key]['repaid'] - y) * k
                b = b + (-1) * (data[key]['repaid'] - y) * k
    
    return [ws, wr, b]

def predict(weight, client):
    z = client['salary'] * weight[0] + client['request'] * weight[1] - weight[2]
    if z >= 0:
        return True
    return False

client = dict(zip(['salary', 'request'], map(float, input().split())))
# Ваш код будет вставлен сюда
data = load('data.csv')
brain = train(data)
print('YES' if predict(brain, client) else 'NO')

# {
# 1:{a:0, b:1, r:1}
# 2:{a:0, b:1, r:1}
# 3:{a:0, b:1, r:1}
# 4:{a:0, b:1, r:1}
# 5:{a:0, b:1, r:1}
# 6:{a:0, b:1, r:1}
# 7:{a:0, b:1, r:1}
# 8:{a:0, b:1, r:1}
# 9:{a:0, b:1, r:1}
# 10:{a:0, b:1, r:1}
# 11:{a:0, b:1, r:1}
# 12:{a:0, b:1, r:1}
# 13:{a:0, b:1, r:1}
# }