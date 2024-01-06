K, A, B = map(int, input().split())

l = (A - 1) / K
a = B / K

if a - l >= 1:
    print("OK")
else:
    print("NG")