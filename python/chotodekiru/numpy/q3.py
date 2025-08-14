# 例題3：統計・データ分析の基礎
# 目的: NumPyを使った統計計算とマスク処理の理解。

# 問題:
# 平均50、標準偏差10の正規分布に従う乱数を1000個生成する。
# その配列の平均・中央値・標準偏差を計算する。
# 値が平均±1標準偏差の範囲にある要素だけを抽出する。
# 抽出したデータの個数と、その割合（%）を求める。

import numpy as np

# 1. 平均50, 標準偏差10の正規分布乱数を1000個
data = np.random.normal(50, 10, 1000)

# 2. 平均・中央値・標準偏差
mean = np.mean(data)
median = np.median(data)
std = np.std(data)
print("平均:", mean)
print("中央値:", median)
print("標準偏差:", std)

# 3. 平均±1標準偏差の範囲にあるデータ抽出
# ブロードキャストを利用して、平均±1標準偏差の範囲にあるデータを抽出する。
mask = (data >= mean - std) & (data <= mean + std)
filtered_data = data[mask]

print("抽出したデータの個数:", len(filtered_data))
print("抽出したデータの割合:", len(filtered_data) / len(data) * 100, "%")