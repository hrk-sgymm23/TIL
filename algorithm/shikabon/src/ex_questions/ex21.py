# レベルNバーガーの長さをLN
# レベルNバーガーに含まれるパティをSN個とする

# レベルNバーガーの長さLNとパティの個数SNを求める方法
# 一般に
# - LN = 2LN-1+3 (L0=1)
# - SN = 2SN-1+1(S0=1)

# 参考
# https://scrapbox.io/esaka-sandbox/AtCoder_Beginner_Contest_115_-_D_-_Christmas
# https://blog.hamayanhamayan.com/entry/2018/12/09/101457

# X...層の数: パティまたはパン一枚で1層

# 入力例
# N X
# 2 7

def rec(N, X, L, S):
    # 終了条件を定義
    if N == 0:
        return 1
    
    # 再帰関数を用いるのは②と④のパーツ
    if X == 1:
        return 0
    # 層の厚さが②パーツ以上の時
    elif X <= L[N-1]+1:
        return rec(N-1, X-1, L, S)
    # 層の厚さが③パーツ以上の時
    # 7 == L[N-1]+2 = 5 + 2
    elif X == L[N-1]+2:
        return S[N-1] + 1
    # 層の厚さが④パーツ以上の時
    elif X <= L[N-1] * 2 + 2:
        return rec(N-1, X-L[N-1]-2, L, S) + S[N-1]+1
    # 層の厚さが⑤パーツの時
    else:
        return S[N-1] * 2 + 1
    


N, X = map(int, input().split())

L = [1] * (N + 1)
S = [1] * (N + 1)

# 1~3繰り返す
for n in range(1, N+1):
    # バーガーの長さ
    L[n] = L[n-1] * 2 + 3
    # パティの数
    S[n] = S[n-1] * 2 + 1

# [1, 5 ,13]
# レベル２(インデックス[1])の長さは5
print(L)

print(rec(N, X, L, S))


