# About InterLeaving

## インターリービングについて調べる

- [A/Bテストより10~100倍効率的なランキング評価手法　インターリービング（Interleaving）のまとめと実践](https://qiita.com/mpkato/items/99bd55cc17387844fd62#balanced-interleaving-joachims-2002a-2003)

## Balanced interleaving (Joachims 2002a, 2003)

https://qiita.com/mpkato/items/99bd55cc17387844fd62#balanced-interleaving-joachims-2002a-2003

```python
L = [] # 生成されるランキング  
k_A, k_B = 0, 0 # 各ランクキング中で参照している順位を表すポインタ
is_A_first = random_bit() # TrueかFalseをランダムで返す。最初にどちらのランキングの検索結果を利用するか決める。
while len(L) < k and k_A < len(A) and k_B < len(B):
    if k_A < k_B or (k_A == k_B and is_A_first):
        if not A[k_A] in L:
            L.append(A[k_A]) # A[k_A]がすでにLに含まれていなければ末尾に追加
        k_A += 1
    else:
        if not B[k_B] in L:
            L.append(B[k_B]) # B[k_B]がすでにLに含まれていなければ末尾に追加
        k_B += 1      
```

