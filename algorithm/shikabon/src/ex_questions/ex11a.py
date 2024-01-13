# 10000円札a、5000円札b、1000円札cとする
# a+b+c= N 10000a+5000b+1000c=Yとなる
# a+b+c= Nよりc=N-a-bがcの文の繰り返しが不要
# よってfor c in range(N+1):の繰り返しを消せる
# **動かしたい変数がある時は一つだけ動かして考える**
N, Y = map(int, input().split())

ares, bres, cres = -1, -1, -1

for a in range(N+1):
    for b in range(N+1):
        c = N - a - b
        # cが0以上N以下でない場合はスキップ
        if c < 0 or c > N:
            continue

        if a + b + c == N \
                and 10000 * a + 5000 * b + 1000 * c == Y:
                    ares, bres, cres = a, b, c

print(ares, bres, cres)