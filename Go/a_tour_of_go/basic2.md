# For

https://go-tour-jp.appspot.com/flowcontrol/1

基本的に、 for ループはセミコロン ; で3つの部分に分かれている。

初期化ステートメント: 最初のイテレーション(繰り返し)の前に初期化が実行される
条件式: イテレーション毎に評価される
後処理ステートメント: イテレーション毎の最後に実行される
初期化ステートメントは、短い変数宣言によく利用する。その変数は for ステートメントのスコープ内でのみ有効。

```go
package main

import "fmt"

func main() {
	sum := 0
	for i := 0; i < 100; i++ {
		sum += i
	}
	fmt.Println(sum)
}
// 4950
```

## For continued

https://go-tour-jp.appspot.com/flowcontrol/2

初期化と後処理ステートメントの記述は任意になる。

```go
package main

import "fmt"

func main() {
	sum := 1
	for ; sum < 100; {
		sum += sum
	}
	fmt.Println(sum)
}
// 128
```

## For is Go's "while"

https://go-tour-jp.appspot.com/flowcontrol/3

セミコロン(;)を省略することもできる。つまり、C言語などにある`while`は、Goでは`for`だけを使う。

```go
package main

import "fmt"

func main() {
	sum := 1
	for sum < 1000 {
		sum += sum
	}
	fmt.Println(sum)
}
// 1024
```

## If
https://go-tour-jp.appspot.com/flowcontrol/5

Go言語の`if`ステートメントは、先ほどの`for`ループと同様に、括弧`( )`は不要で、中括弧`{ }`は必要。

```go
package main

import (
	"fmt"
	"math"
)

func sqrt(x float64) string {
	if x < 0 {
		return sqrt(-x) + "i"
	}
	return fmt.Sprint(math.Sqrt(x))
}

func main() {
	fmt.Println(sqrt(3), sqrt(-4))
}
// 1.7320508075688772 2i
```

## If with a short statement

`if`ステートメントは、`for`のように、条件の前に、評価するための簡単なステートメントを書くことができる。
ここで宣言された変数は、 if のスコープ内だけで有効。

```go
package main

import (
	"fmt"
	"math"
)

func pow(x, n, lim float64) float64 {
	if v := math.Pow(x, n); v < lim {
		return v
	}
	return lim
}

func main() {
	fmt.Println(
		pow(3, 2, 10),
		pow(3, 3, 20),
	)
}
// 9 20
```

## If and else

https://go-tour-jp.appspot.com/flowcontrol/7

`if`ステートメントで宣言された変数は、`else`ブロック内でも使うことができる。
`main`の`fmt.Println`は`pow`が実行された後に実行される。

```go
package main

import (
	"fmt"
	"math"
)

func pow(x, n, lim float64) float64 {
	if v := math.Pow(x, n); v < lim {
		return v
	} else {
		fmt.Printf("%g >= %g\n", v, lim)
	}
	// can't use v here, though
	return lim
}

func main() {
	fmt.Println(
		pow(3, 2, 10),
		pow(3, 3, 20),
	)
}
```

## WIP/Exercise: Loops and Functions

https://go-tour-jp.appspot.com/flowcontrol/8

解説: https://exmedia.jp/blog/a-tour-of-go%E3%81%AE%E7%B7%B4%E7%BF%92%E5%95%8F%E9%A1%8C%E3%82%92%E8%A7%A3%E8%AA%AC%E3%81%99%E3%82%8B%E3%82%B7%E3%83%AA%E3%83%BC%E3%82%BA1-11-exercise-loops-and-functions/

`Sqrt`メソッドの作成
```go
func Sqrt(x float64) float64 {
	z := 1.0
	for i := 0; i < 10; i++ {
		z -= (z*z - x) / (2 * z)
		fmt.Println(z)
	}
	return z
}
```

## Switch

https://go-tour-jp.appspot.com/flowcontrol/9

```go
package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Print("Go runs on ")
	switch os := runtime.GOOS; os {
	case "darwin":
		fmt.Println("OS X.")
	case "linux":
		fmt.Println("Linux.")
	default:
		// freebsd, openbsd,
		// plan9, windows...
		fmt.Printf("%s.\n", os)
	}
}
// Go runs on Linux.
```

## Switch evaluation order

https://go-tour-jp.appspot.com/flowcontrol/10

`switch case`は、上から下へ`case`を評価。 `case`の条件が一致すれば、そこで停止(自動的に`break`)する。

```go
switch i {
case 0:
case f():
}
```

`i==0`であれば、 `case 0`で`break`されるため`f`は呼び出されない

## Switch with no condition

https://go-tour-jp.appspot.com/flowcontrol/11

条件のないswitchは、 switch true と書くことと同じ。

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	t := time.Now()
	switch {
	case t.Hour() < 12:
		fmt.Println("Good morning!")
	case t.Hour() < 17:
		fmt.Println("Good afternoon.")
	default:
		fmt.Println("Good evening.")
	}
}
// Good evening.
```

## Defer

https://go-tour-jp.appspot.com/flowcontrol/12

defer ステートメントは、 defer へ渡した関数の実行を、呼び出し元の関数の終わり(returnする)まで遅延させるもの。
defer へ渡した関数の引数は、すぐに評価されるが、その関数自体は呼び出し元の関数がreturnするまで実行されない。

```go
package main

import "fmt"

func main() {
	defer fmt.Println("world")

	fmt.Println("hello")
}
// hello
// world
```

## Stacking defers

https://go-tour-jp.appspot.com/flowcontrol/13

deferへ渡した関数が複数ある場合はスタックされる。
呼び出し元関数がreturnするとき、deferへ渡した関数がLIFOの順で実行される

```go
package main

import "fmt"

func main() {
	fmt.Println("counting")

	for i := 0; i < 10; i++ {
		defer fmt.Println(i)
	}

	fmt.Println("done")
}

// counting
// done
// 9
// 8
// 7
// 6
// 5
// 4
// 3
// 2
// 1
// 0
```









