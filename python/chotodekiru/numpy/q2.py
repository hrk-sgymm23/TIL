# 例題2：ベクトル・行列計算
# 目的: NumPyの高速な行列演算やブロードキャストの仕組みを理解。

# 問題:
# 2x3の行列Aと、3x2の行列Bを乱数で作成する（値は0〜9の整数）。
# AとBの行列積を計算する。
# Aの各要素に10を足した配列を作成する（ブロードキャスト利用）。
# 行列積の結果から、最大値と最小値を求める。

import numpy as np

A = np.random.randint(0, 10, (2, 3))
B = np.random.randint(0, 10, (3, 2))
print("行列A:\n", A)
print("\n行列B:\n", B)

C = np.dot(A, B)
print("\n行列積C:\n", C)

D = A + 10
print("\nAの各要素に10を足した配列D:\n", D)

max_val = np.max(C)
min_val = np.min(C)
print("\n行列積Cの最大値:", max_val)
print("\n行列積Cの最小値:", min_val)