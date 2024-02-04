from queue import Queue

# グラフGに対して頂点sを始点とした幅優先探索を行う
# 返り値: 各頂点への頂点sからの最短距離を表す配列
def bfs(G, s):
    # todoを表すキュー
    que = Queue()

    # dist[v]は始点sから頂点vへの最短経路長
    dist = [-1] * len(G)

    # 最初に始点sをtodoリストにセットする
    que.put(s)
    dist[s] = 0

    # todoリストが空になるまで探索
    while not que.empty():
        # todoリストから頂点vを取り出す
        v = que.get()
        # vに直接つながる頂点を探索
        for v2 in G[v]:
            # v2が既に探索済みの場合はスキップする
            if dist[v2] != -1:
                continue
            # v2を新たにtodoに追加
            que.put(v2)
            # v2のdistの値を更新
            dist[v2] = dist[v] + 1
    # 最短距離を表す配列
    return dist
# bfs([[頂点0と隣接している頂点],[頂点1と隣接している頂点],...],始点)
result = bfs([[1, 2], [0, 3, 4], [0, 4], [1], [1, 2]], 0)

# [0, 1, 1, 2, 2]
# 返される各要素は各頂点への始点からの最短の辺の数
# [頂点0から0の最短辺の数, 頂点0から1の最短辺の数, 頂点0から2の最短辺の数,...]
print(result)
