# バッグに入れないを0入れるを１として「0と1のみからなる長さNの数列」(2^N通り)を全て列挙できれば問題が解ける

N = 3

# 再帰関数を用いて0と1からのみなる長さNの数列を全列挙
def rec(A):
    if len(A) == N:
        print(A)
        return
    
    for v in range(2):
        A.append(v)
        rec(A)
        A.pop()

rec([])