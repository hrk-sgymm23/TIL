#　問題の言い換え
#　マス(0,0)からマス(H-1,W-1)へ至る経路が存在するよう残しつつ、
# できるだけ多くのマスを黒く塗る時、白色のまま残すマスの最大値を求めよ

# マス(0,0)からマス(H-1,W-1)へ至る経路(白マスのみでたどり着く経路)が存在しなければ、答えは-1となる
# マス(0,0)からマス(H-1,W-1)へ至る経路が存在する場合にはそのうちに最短経路をPとする(幅優先探索で求められる)

# この時、Pに含まれる白マスの個数が求める最小値になる
# なぜならば、もし白色のまま残す個数よりそれよりも小さくできると仮定するとPよりも短い経路が存在するため...Pが最短経路のため矛盾となる

# 入力例
# 5 6
# .....#
# ####..
# ......
# #.####
# ......

from queue import Queue

# 上下左右の移動を定義
DX = [1, 0, -1, 0]
DY = [0, 1, 0, -1]

H, W = map(int,input().split())
S = [input() for i in range(H)]

# キューの各要素はマス(x,y)を表すペアとする
# dist[x][y] = マス(x,y)への最短経路長
que = Queue()
dist = [[-1] * W for i in range(H)]

# 幅優先探索の初期条件
que.put((0, 0))
dist[0][0] = 0

# x,y: 現在キューから取り出したマスの座標 ex (1,0)
# dist[x][y]: そのマスまでの最短距離　ex 1
# x2,y2: 次に探索するマスの座標
# dist[x2][y2]: そのマスまでの最短距離

# 幅優先探索
while not que.empty():
    # キューから要素を取り出す
    # x,y = 0,0
    x, y = que.get()
    # 上下左右への移動を順に試す
    # 1,0 zip(1,0)
    for dx, dy in zip(DX, DY):
        # 2,0 = 1+1, 0,0 
        x2, y2 = x + dx, y + dy
        # 配列外参照はバツ
        if x2 < 0 or x2 >= H or y2 < 0 or y2 >= W:
            continue
        # 黒マスの時
        # S[2][0] == 
        if S[x2][y2] == "#":
            continue
        # 既に探索済みの場合
        if dist[x2][y2] != -1:
            continue
        # (x2, y2)をキューにpushして、distを更新
        que.put((x2, y2))
        dist[x2][y2] = dist[x][y] + 1

white = sum(line.count('.') for line in S)

if dist[H-1][W-1] != -1:
    # 黒く塗れるマスの個数 = 迷路の白マスの数　- ゴールまでの距離 - スタート地点
    print(white - dist[H-1][W-1] - 1)
else:
    print(-1)