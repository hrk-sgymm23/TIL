# 蓮長圧縮と同様の方法方法で解くことができる
# 添字iを先頭から動かしながら、次のように処理していく
# この時添字iは常に大文字を指すようになっている

# 大文字S[i]に対して、その次の大文字がどこにあるかを求める(その大文字をS[j]とする)
# S[i]からS[j]までの部分文字列を一つの単語として切り出す
# i=j+1と更新する(jは単語の終わりを表す添字のため、その次のj+1にiを移動させる)

# このように取り出した単語の列をソートして、連結して出力する
# 計算量はソートの部分い多く時間がかかるため、O(N log N)になる

# word.sort(key=str.lower)と実装することで、wordsの各単語を「大文字を全て小文字にした状態での辞書順比較」に基づいてソートするようにしている

# FisHDoGCaTAAaAAbCAC
S = input()

words = []
# 文字列Sを単語ごとに分解する
i = 0
# S文字数未満分処理を繰り返す
while i < len(S):
    # 初めてS[j]が大文字となる場所jを求める
    j = i + 1
    # S文字数未満分かつS[j]が小文字である時処理を繰り返す
    while j < len(S) and S[j].islower():
        j += 1
    
    # 見つかった単語を切り出してリストにする
    # i:j+1は単語の大文字から大文字まで
    words.append(S[i:j+1])
    # iをj+1のところへワープさせる(次の単語へ)
    i = j+1
# リスト化した単語を大文字小文字を無視した状態で辞書順にソート
words.sort(key=str.lower)
# 単語を連結して出力する
print("".join(words))