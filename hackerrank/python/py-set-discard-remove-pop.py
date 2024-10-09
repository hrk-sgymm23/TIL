# Sの配列の要素数を受け取る
n = int(input())
# Sの配列を受け取る
s = set(map(int, input().split()))
# コマンドの実行回数
N = int(input())

# コマンドの実行回数分繰り返し
for i in range(N):
    command = list(input().split())
    # コマンドの種類が何か判断
    match command[0]:
        case 'pop':
            s.pop()
        case 'remove':
            #　removeは指定した値がないとkeyerrorになるので事前確認
            if int(command[1]) in s:
                s.remove(int(command[1]))
        case 'discard':
            s.discard(int(command[1]))

print(sum(s))
