# 10000円札a、5000円札b、1000円札cとする
# a+b+c= N 10000a+5000b+1000c=Yとなる
N, Y = map(int, input().split())

ares, bres, cres = -1, -1, -1

for a in range(N+1):
    for b in range(N+1):
        for c in range(N+1):
            if a + b + c == N \
                and 10000 * a + 5000 * b + 1000 * c == Y:
                    ares, bres, cres = a, b, c

print(ares, bres, cres)