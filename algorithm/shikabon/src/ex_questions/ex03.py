H, A = map(int, input().split())
# "%"はあまりを出力
if H % A == 0:
    # "//"は商を出力
    print(H // A)
else:
    print(H // A + 1)