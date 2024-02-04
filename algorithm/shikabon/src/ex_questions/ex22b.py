# https://qiita.com/u2dayo/items/386142030a70d2db4e58#%E3%82%B3%E3%83%BC%E3%83%891

# from itertools import combinations_with_replacement as comb_rplcとは
# 数字の書いたボールが袋に入っているとします。
# "without replacement"な普通の『組み合わせ』では、取り出したボールを袋に戻しません。
#  "with replacement"な『重複組み合わせ』では、取り出したボールの数をメモしたあと、袋に戻します。
# つまり重複を許す

# 解法としてあり得る数列を全て作ってそれぞれの得点の計算する
# つまり総当たりで解くことになる

from itertools import combinations_with_replacement as comb_rplc

n, m, q = list(map(int, input().split()))
# reqは[[a1,b1,c1,d1],[a2,b2,c2,d2]……]が入ったリストのリストです
req = [list(map(int, input().split())) for _ in range(q)]

ans = 0
# seqは長さnのタプルです
# m=4,n=3の場合
# １から４までの整数を使って3つの要素からなるタプルを作る(昇順)
# (1,1,1),(1,1,2),(1,1,3),(1,2,2)...
# 
for seq in comb_rplc(range(1, m + 1), n):
    score = 0
    for a, b, c, d in req:
        # 問題文に書いてある数列のk番目は、インデックスだとk-1になるので注意
        if seq[b - 1] - seq[a - 1] == c:
            score += d
    # 前回の処理より高い場合、ansに格納
    # 作った数列の中で一番得点が高くなるものを求める
    ans = max(ans, score)

print(ans)
