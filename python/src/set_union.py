hoge_a = {8, 66, 10, 11}
hoge_b = {4, 2, 66, 8, 11, 3}

result = hoge_a.union(hoge_b)

print(result) # {66, 2, 3, 4, 8, 10, 11}

result = hoge_a | hoge_b

print(result) # {66, 2, 3, 4, 8, 10, 11}