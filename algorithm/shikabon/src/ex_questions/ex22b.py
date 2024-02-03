# https://qiita.com/u2dayo/items/386142030a70d2db4e58#%E3%82%B3%E3%83%BC%E3%83%891
from itertools import combinations_with_replacement as comb_rplc

n, m, q = list(map(int, input().split()))
# reqは[[a1,b1,c1,d1],[a2,b2,c2,d2]……]が入ったリストのリストです
req = [list(map(int, input().split())) for _ in range(q)]

ans = 0
# seqは長さnのタプルです
for seq in comb_rplc(range(1, m + 1), n):
    score = 0
    for a, b, c, d in req:
        # 問題文に書いてある数列のk番目は、インデックスだとk-1になるので注意
        if seq[b - 1] - seq[a - 1] == c:
            score += d
    ans = max(ans, score)

print(ans)
