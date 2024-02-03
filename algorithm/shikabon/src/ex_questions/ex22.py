# 参考　https://qiita.com/u2dayo/items/386142030a70d2db4e58
# 条件に合った長さNの数列を作る

# N M Q
# a b c d
# a b c d
# a b c d

# 入力例
# 3 4 3
# 1 3 3 100
# 1 2 2 10
# 2 3 2 10

# A = [1,3,4]
# 1 3 3の時...4-1=3 なので100ポイント
# 1 2 2の時...3-1=2 なので10
# 2 3 2の時...4-3=2にはならないため得点にならない
# よって110

# 問題の解釈
# (作った数列のb番目)-(作った数列のa番目)=cの時　得点dをもらえる
# 全ての条件Qの中で一番最大得点をもらえるような数列Aを作り実際にもらえる特典を示せ
from itertools import combinations_with_replacement as combi

N, M, Q = map(int,input().split())

a = [0] * Q
b = [0] * Q
c = [0] * Q
d = [0] * Q

for q in range(Q):
    a[q], b[q], c[q], d[q] = map(int,input().split())
    # 数列Aの添字を0スタートにする
    a[q] -= 1
    b[q] -= 1

def calc_score(A):
    score = 0
    for ai, bi, ci, di in zip(a, b, c, d):
        print("############")
        print(A[bi] - A[ai])
        print(ci)
        print(di)
        print("############")
        if A[bi] - A[ai] == ci:
            score += di
        return score
    
result = 0

# >この問題で作る数列の条件は、次の数字が前の数字より小さくないことです。
# >入力を昇順にすれば、出力も昇順になるので、この条件は勝手に満たしてくれます
for A in combi(range(1, M+1), N):
    result = max(result, calc_score(A))

print(result)