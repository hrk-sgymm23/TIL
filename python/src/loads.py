import json

data = '{ "human": "hoge", "age": 23, "address": "shinjuku" }'

dicted_data = json.loads(data)

print(data['age'])
print(dicted_data['age'])
