# N個の文字列S0,S1...Sn-1をそれぞれあらかじめソートする
# 連想配列を用いて各文字列の個数を求める
# 各文字列についてその個数をnとしてn(n-1)/2を合算する
from collections import defaultdict

N = int(input())
# num[s]: 文字列sは何個あるか
num = defaultdict(int)
for i in range(N):
    # 入力も文字列をそーとしておく
    s = "".join(sorted(input()))

    num[s] += 1
# 集計
result = 0
for s in num:
    # 文字列sがn個ある
    n = num[s]
    # nC2を足していく
    result += n*(n-1)//2

print(n)
print(result)

