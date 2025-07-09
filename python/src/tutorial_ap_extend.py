a = [1, 2, 3]
a.append([4, 5, 6])  # appendを使用
print(a)  # 出力: [1, 2, 3, [4, 5, 6]]

a = [1, 2, 3]
a.extend([4, 5, 6])  # extendを使用
print(a)  # 出力: [1, 2, 3, 4, 5, 6]