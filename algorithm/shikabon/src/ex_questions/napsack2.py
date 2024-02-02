# n:「0,1からなる数列A」の長さ
# sw: 現在の数列Aに対応する品物の重さの総和
# sv: 現在の数列Aに対応する品物の価値の総和

N, W = map(int, input().split())
w = list(map(int, input().split()))
v = list(map(int, input().split()))

def rec(n, sw, sv):
    if n == N:
        return sv
    
    result = 0

    score = rec(n+1, sw, sv)
    result = max(result, score)

    if sw + w[n] <= W:
        score = rec(n+1, sw+w[n], sv+v[n])
        result = max(result, score)
    return result

print(rec(0,0,0))