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





