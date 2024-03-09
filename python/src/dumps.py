import json

data = { "human": "hoge", "age": 23, "address": "shinjuku" }

formatted_data = json.dumps(data)

# {"human": "hoge", "age": 23, "address": "shinjuku"}
print(formatted_data)
# <class 'str'>
print(type(formatted_data))
