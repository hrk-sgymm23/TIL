# 締め切りであるM日目から0日目へと遡るよう考える
# ヒープを用いる.ヒープは以下操作ができる
# - ヒープに要素を挿入する
# - ヒープに含まれる要素のうち最大値を取得する
# - ヒープに含まれる要素のうち最大のものを削除する

# i = M-1, M-2,...,0に対して
# - ヒープにAi =M-iである仕事を全て挿入する
# - ヒープからBiが最大のもを取り出す(ヒープから削除)ただしヒープがからの場合はスキップ

# N M
# A0 B0
# . .
# . .
# AN-1 BN-1

# 入力例
# 3 4
# 4 3
# 4 1
# 2 2

from heapq import heappush, heappop

N,M = map(int, input().split())

# AtoB...A[i]=vとなるiに対するB[i]の集合
AtoB = [[] for i in range(M+1)]

for i in range(N):
    # 仕事の入力
    A,B = map(int, input().split())

    # 仕事がM日を超える場合はパス
    if A > M:
        continue
    # 仕事データを登録
    AtoB[A].append(B)

# 報酬の最大値を格納
result = 0
# ヒープ格納用
que = []

# M日目から0日目へと遡る
# 入力例の場合
# [[], [], [2], [], [3, 1]]
for Bs in AtoB:
    # ヒープに遡った分の仕事を追加
    print(B)
    for B in Bs:
        # python3のヒープは小さい順のため符号反転して追加
        # 3回目のループBs=[2]
        # que=[-2]
        # 5回目のループBs=[3,1]
        # que=[-1,-2,-3]
        heappush(que, -B)
    # ヒープが空でなければ報酬最大の仕事を追加する
    # queがからのため-1は加算されない
    if que:
        result -= heappop(que)

print(result)

