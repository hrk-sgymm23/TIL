hoge_a = {8, 66, 10, 11}
hoge_b = {4, 2, 66, 8, 11, 3}

result = hoge_a.intersection(hoge_b)

print(result) # {8, 66, 11}

result = hoge_a & hoge_b

print(result) # {8, 66, 11}