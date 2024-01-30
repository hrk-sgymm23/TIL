# レベルNバーガーの長さをLN
# レベルNバーガーに含まれるパティをSN個とする

# レベルNバーガーの長さLNとパティの個数SNを求める方法
# 一般に
# - LN = 2LN-1+3 (L0=1)
# - SN = 2SN-1+1(S0=1)

# 参考
# https://scrapbox.io/esaka-sandbox/AtCoder_Beginner_Contest_115_-_D_-_Christmas
# https://blog.hamayanhamayan.com/entry/2018/12/09/101457

def rec(N, X, L, S):
    if N == 0:
        return 1
    
    # 再帰関数を用いるのは②と④のパーツ
    if X == 1:
        return 0
    # ②
    elif X <= L[N-1]+1:
        return rec(N-1, X-1, L, S)
    elif X == L[N-1]+2:
        return S[N-1] + 2
    # ④
    elif X <= L[N-1] * 2 + 2:
        return rec(N-1, X-L[N-1]-2, L, S) + S[N-1]+1
    else:
        return S[N-1] * 2 + 1
    


N, X = map(int, input().split())

L = [1] * (N + 1)
S = [1] * (N + 1)

for n in range(1, N+1):
    L[n] = L[n-1] * 2 + 3
    S[n] = S[n-1] * 2 + 1

print(rec(N, X, L, S))


