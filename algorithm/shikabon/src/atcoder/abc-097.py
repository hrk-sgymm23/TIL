# https://zenn.dev/hyperdb/articles/a7db6dec39811e
import math


def getInt():
    return int(input())


def main():
    x = getInt()

    r = 0
    if x == 1:
        r = 1
    else:
        for i in range(2, int(math.pow(x, 1 / 2)) + 1):
            y = i ** 2
            r = y if y > r else r
            while y <= x:
                y = y * i
                r = y if y > r and y <= x else r
    print(r)


if __name__ == "__main__":
    main()