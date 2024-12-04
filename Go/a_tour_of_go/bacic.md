# Packages

https://go-tour-jp.appspot.com/basics/1

## Exported names

https://go-tour-jp.appspot.com/basics/3

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Println(math.Pi)
}
```

## Functions

https://go-tour-jp.appspot.com/basics/4

関数は、0個以上の引数を取ることができます。
この例では、 add 関数は、 int 型の２つのパラメータを取ります。
変数名の 後ろ に型名を書くことに注意してください。

```go
package main

import "fmt"

func add(x int, y int) int {
	return x + y
}

func main() {
	fmt.Println(add(42, 13))
}
```

関数の２つ以上の引数が同じ型である場合には、最後の型を残して省略して記述できる。

```go
package main

import "fmt"

func add(x, y int) int {
	return x + y
}

func main() {
	fmt.Println(add(42, 13))
}
```

## Multiple results

https://go-tour-jp.appspot.com/basics/6

関数は複数の戻り値を返すことができる。

```go
package main

import "fmt"

func swap(x, y string) (string, string) {
	return y, x
}

func main() {
	a, b := swap("hello", "world")
	fmt.Println(a, b)
}
```

## Named return values

https://go-tour-jp.appspot.com/basics/7

```go
https://go-tour-jp.appspot.com/basics/7
```

Goでの戻り値となる変数に名前をつける( named return value )ことができます。戻り値に名前をつけると、関数の最初で定義した変数名として扱われます。
この戻り値の名前は、戻り値の意味を示す名前とすることで、関数のドキュメントとして表現するようにしましょう。
名前をつけた戻り値の変数を使うと、 return ステートメントに何も書かずに戻すことができます。これを "naked" return と呼びます。

以下の`(x, y int) `の部分

```go
package main

import "fmt"

func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}

func main() {
	fmt.Println(split(17))
}
```

## Variables
https://go-tour-jp.appspot.com/basics/8

var ステートメントは変数( variable )を宣言します。 関数の引数リストと同様に、複数の変数の最後に型を書くことで、変数のリストを宣言できます。

```go
package main

import "fmt"

var c, python, java bool

func main() {
	var i int
	fmt.Println(i, c, python, java)
}

// 0 false false false
```

## Variables with initializers

https://go-tour-jp.appspot.com/basics/9

var 宣言では、変数毎に初期化子( initializer )を与えることができる。
初期化子が与えられている場合、型を省略できます。その変数は初期化子が持つ型になる。

```go
package main

import "fmt"

var i, j int = 1, 2

func main() {
	var c, python, java = true, false, "no!"
	fmt.Println(i, j, c, python, java)
}
```

## Short variable declarations `:=`

`:=`を使い方宣言を省略できる。
**しかし使えるのは関数内のみ**

```go
package main

import "fmt"

func main() {
	var i, j int = 1, 2
	k := 3
	c, python, java := true, false, "no!"

	fmt.Println(i, j, k, c, python, java)
}
```

## Zero values

https://go-tour-jp.appspot.com/basics/12

変数に初期値を与えずに宣言すると、ゼロ値( zero value )が与えられます。

ゼロ値は型によって以下のように与えられます:

数値型(int,floatなど): 0
bool型: false
string型: "" (空文字列( empty string ))

```go
package main

import "fmt"

func main() {
	var i int
	var f float64
	var b bool
	var s string
	fmt.Printf("%v %v %v %q\n", i, f, b, s)
}
// 0 0 false ""
```

## Type conversions

https://go-tour-jp.appspot.com/basics/13

変数 v 、型 T があった場合、 T(v) は、変数 v を T 型へ変換します。

```go
var i int = 42
var f float64 = float64(i)
var u uint = uint(f)
```
上記は以下のように書くことができる
```go
i := 42
f := float64(i)
u := uint(f)
```





