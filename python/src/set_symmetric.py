hoge_a = {8, 66, 10, 11}
hoge_b = {4, 2, 66, 8, 11, 3}

result = hoge_a.symmetric_difference(hoge_b)

print(result) # {2, 3, 4, 10}

result = hoge_a ^ hoge_b

print(result) # {2, 3, 4, 10}