# Pointers

Goはポインタを利用する。ポインタは値のメモリアドレスを指す。
変数`T`のポインタは、`*T`型で、ゼロ値は`nil`。

```go
var p *int
```

`&`オペレータは、そのオペランド(`operand`)へのポインタを引き出す。
```go
i := 42
p = &i
```

`*`オペレータは、ポインタの指す先の変数を示す。

```go
fmt.Println(*p) // ポインタpを通してiから値を読みだす
*p = 21         // ポインタpを通してiへ値を代入する
```

```go
package main

import "fmt"

func main() {
	i, j := 42, 2701

	p := &i         // point to i
	fmt.Println(*p) // read i through the pointer
	*p = 21         // set i through the pointer
	fmt.Println(i)  // see the new value of i

	p = &j         // point to j
	*p = *p / 37   // divide j through the pointer
	fmt.Println(j) // see the new value of j
}
// 42
// 21
// 73
```

## Structs

https://go-tour-jp.appspot.com/moretypes/2

`struct`構造体はフィールドの集まり。

```go
package main

import "fmt"

type Vertex struct {
	X int
	Y int
}

func main() {
	fmt.Println(Vertex{1, 2})
}

// {1 2}
```

## Struct Fields

https://go-tour-jp.appspot.com/moretypes/3

structのフィールドは、ドット( . )を用いてアクセス

```go
package main

import "fmt"

type Vertex struct {
	X int
	Y int
}

func main() {
	v := Vertex{1, 2}
	v.X = 4
	fmt.Println(v.X)
}
// 4
```

## Pointers to structs

https://go-tour-jp.appspot.com/moretypes/4

`struct`のフィールドは、`struct`のポインタを通してアクセスすることもできる。
> フィールド X を持つstructのポインタ p がある場合、フィールド X にアクセスするには (*p).X のように書くことができます。 しかし、この表記法は大変面倒ですので、Goでは代わりに p.X と書くこともできます。

```go
package main

import "fmt"

type Vertex struct {
	X int
	Y int
}

func main() {
	v := Vertex{1, 2}
	p := &v
	p.X = 1e9
	fmt.Println(v)
}
// {1000000000 2}
```

## Struct Literals

https://go-tour-jp.appspot.com/moretypes/5

```go
package main

import "fmt"

type Vertex struct {
	X, Y int
}

var (
	v1 = Vertex{1, 2}  // has type Vertex
	v2 = Vertex{X: 1}  // Y:0 is implicit
	v3 = Vertex{}      // X:0 and Y:0
	p  = &Vertex{1, 2} // has type *Vertex
)

func main() {
	fmt.Println(v1, p, v2, v3)
}

// {1 2} &{1 2} {1 0} {0 0}
```

## Arrays

https://go-tour-jp.appspot.com/moretypes/6

以下は、intの10個の配列を宣言している。
```go
var a [10]int
```

配列の長さは型の一部。

```go
package main

import "fmt"

func main() {
	var a [2]string
	a[0] = "Hello"
	a[1] = "World"
	fmt.Println(a[0], a[1])
	fmt.Println(a)

	primes := [6]int{2, 3, 5, 7, 11, 13}
	fmt.Println(primes)
}
// Hello World
// [Hello World]
// [2 3 5 7 11 13]
```

## Slices

https://go-tour-jp.appspot.com/moretypes/7

配列は固定長である。一方でスライスは可変調である。
型 []T は 型 T のスライスを表す。

コロンで区切られた二つのインデックス low と high の境界を指定することによってスライスが形成される。

```go
a[low : high]
```

次の式は a の要素の内 1 から 3 を含むスライスを作る。

```go
a[1:4]
```

```go
package main

import "fmt"

func main() {
	primes := [6]int{2, 3, 5, 7, 11, 13}

	var s []int = primes[1:4]
	fmt.Println(s)
}
// [3 5 7]
```

## Slices are like references to arrays

https://go-tour-jp.appspot.com/moretypes/8

スライスは配列の参照。スライスはどんなデータも保持しておらず、単に元の配列の部分裂を指し示している。
スライスの要素を変更すると、その元となる配列の対応する要素も変更になる。

```go
package main

import "fmt"

func main() {
	names := [4]string{
		"John",
		"Paul",
		"George",
		"Ringo",
	}
	fmt.Println(names)

	a := names[0:2]
	b := names[1:3]
	fmt.Println(a, b)

	b[0] = "XXX"
	fmt.Println(a, b)
	fmt.Println(names)
}
// [John Paul George Ringo]
// [John Paul] [Paul George]
// [John XXX] [XXX George]
// [John XXX George Ringo]
```

## Slice literals

https://go-tour-jp.appspot.com/moretypes/9

スライスのリテラルは長さのない配列リテラルのようなもの

```go
[3]bool{true, true, false}
```
下記は配列を作成しそれを参照するスライスを作成する
```go
[]bool{true, true, false}
```

```go
package main

import "fmt"

func main() {
	q := []int{2, 3, 5, 7, 11, 13}
	fmt.Println(q)

	r := []bool{true, false, true, true, false, true}
	fmt.Println(r)

	s := []struct {
		i int
		b bool
	}{
		{2, true},
		{3, false},
		{5, true},
		{7, true},
		{11, false},
		{13, true},
	}
	fmt.Println(s)
}
// [2 3 5 7 11 13]
// [true false true true false true]
// [{2 true} {3 false} {5 true} {7 true} {11 false} {13 true}]
```

## Slice defaults

https://go-tour-jp.appspot.com/moretypes/10

スライスするときは、それらの既定値を代わりに使用することで上限または下限を省略することができる。

```go
var a [10]int
```

上記配列において以下は等価

```go
a[0:10]
a[:10]
a[0:]
a[:]
```

上記コードはスライスを段階的に切り出す処理
```go
package main

import "fmt"

func main() {
	s := []int{2, 3, 5, 7, 11, 13}

	s = s[1:4]
	fmt.Println(s)

	s = s[:2]
	fmt.Println(s)

	s = s[1:]
	fmt.Println(s)
}
// [3 5 7]
// [3 5]
// [5]
```

## Slice length and capacity

https://go-tour-jp.appspot.com/moretypes/11

スライスは長さ( length )と容量( capacity )の両方を持っている。

スライスの長さは、それに含まれる要素の数。
スライスの容量は、スライスの最初の要素から数えて、元となる配列の要素数。

```go
package main

import "fmt"

func main() {
	s := []int{2, 3, 5, 7, 11, 13}
	printSlice(s)

	// Slice the slice to give it zero length.
	s = s[:0]
	printSlice(s)

	// Extend its length.
	s = s[:4]
	printSlice(s)

	// Drop its first two values.
	s = s[1:]
	printSlice(s)
}

func printSlice(s []int) {
	fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)
}
// len=6 cap=6 [2 3 5 7 11 13]
// len=0 cap=6 []
// len=4 cap=6 [2 3 5 7]
// len=3 cap=5 [3 5 7]
```

## Nil slices

https://go-tour-jp.appspot.com/moretypes/12

スライスのゼロ値は`nil`
`nil`スライスは0の長さと容量を持っている。配列自体は持っていない。

```go
package main

import "fmt"

func main() {
	var s []int
	fmt.Println(s, len(s), cap(s))
	if s == nil {
		fmt.Println("nil!")
	}
}
// [] 0 0
// nil!
```




