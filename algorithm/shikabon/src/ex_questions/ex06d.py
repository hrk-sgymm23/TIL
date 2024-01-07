# 要素を一つずつ計算し、割り算できる回数を求める
def how_many_times(n):
    count = 0

    while n % 2 == 0:
        n //= 2
        count += 1

    return count

N = int(input())
A = list(map(int, input().split()))

# map関数の使い方: 
# 第1引数には一つ以上の引数を持つcallableなオブジェクト
# 第2引数以降には第一引数のcallableが求める引数の個数分、iterableなオブジェクト(listなどイテレータになれるオブジェクト)を指定する
# mapにてhow_many_timesをAの配列の要素分処理を行い、minにて一番最小の値を変数に格納する
# イテレータ...for文で回せるもの
# min関数の引数は配列
result = min(map(how_many_times, A))

print(result)

