N = int(input())

# set()に関して
# set型を作成できる...set型には値の重複が存在しない
S = set(input() for i in range(N))

print(S)
print(len(S))