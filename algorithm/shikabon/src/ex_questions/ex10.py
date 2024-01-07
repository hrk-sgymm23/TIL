# 0:下,1:右,2:上,3:左,4:右下,5:右上,6:左上,7:左下
DX = [1, 0, -1, 0, 1, -1, -1, 1]
DY = [0, 1, 0, -1, 1, 1, -1, -1]

H, W = map(int, input().split())
S = [input() for i in range(H)]

# 答えを表す二次元配列を用意する('.'は0とする)
result = [[0 if v == '.' else '#' for v in row] for row in S]

# 各マスi,jを順に処理する
for i in range(H):
    for j in range(W):
        # 空きマス以外はそのままにする
        if S[i][j] != '.':
            continue

        # 周囲8マスの#の数を考える
        # zip関数は複数のiterable(リスト、タプル、セットなど)から要素を取り出し、対応する要素をペアとする
        for dx,dy in zip(DX, DY):
            # i,jの周りのますをni,njとする
            ni, nj = i + dx, j + dy
            # マスni,njが盤面外の場合はスキップ
            if ni < 0 or ni >= H or nj < 0 or nj >= W:
                continue
            # '#'であれば結果にインクリメント
            if S[ni][nj] == '#':
                result[i][j] += 1

# (*row, sep='')とすることで空白文字をなくす
for row in result:
    print(row)
    print(*row, sep='')