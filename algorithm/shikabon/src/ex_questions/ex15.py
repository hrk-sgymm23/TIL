# 入力例
# 3 2 3 #頂点数　辺数　クエリの数
# 1 2 #2点間の2頂点番号
# 2 3 #2点間の2頂点番号
# 5 10 5 #頂点1,2,3のそれぞれの色番号
# 1 2 #クエリ1 現在の頂点２の値を出力し、頂点2に隣接されるすべての色が10になる
# 2 1 20 #クエリ2 現在の頂点1の値を出力し、頂点1の色が20に上書きされる
# 1 1 #クエリ1 現在の頂点1の値を出力し、頂点1に隣接されるすべての色が10になる

# 問題としてクエリにより出力された値を出力する必要がある
# 1 2 ...10
# 2 1 20...10
# 1 1...20

N, M, Q = map(int, input().split()) 

# 頂点数Nのグラフを定義
G = [[] for i in range(N)]

# M本の辺を受け取る
for i in range(M):
    u, v = map(int, input().split())

    # 繰り返しの添字に合わせるため、頂点番号を0始まりにする
    u -= 1
    v -= 1
    # グラフに辺を追加
    # 頂点隣接リストの作成
    # uとの隣接リストにvを追加
    G[u].append(v)
    # vとの隣接リストにリストにuを追加
    G[v].append(u)

    print('u' + str(u))
    print('v' + str(v))

    print('G[u]' + str(G[u]))
    print('G[V]' + str(G[v]))

# 初期状態の各頂点の色を入力
col = list(map(int, input().split()))

# 各クエリへ回答
for i in range(Q):
    t, x, *y = map(int, input().split())
    # 頂点番号を0始まりにする
    x -= 1

    # 頂点xの色を出力
    print(col[x])

    if t == 1:
        print(G[x])
        for v in G[x]:
            col[v] = col[x]
    else:
        # 頂点xの色をyに更新
        col[x] = y[0]