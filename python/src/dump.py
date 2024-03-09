import json

data = { "name": "hoge", "age": 23, "address": "shinjuku" }

with open('../result/index.json', 'w') as f:
    json.dump(data, f, indent=2)



