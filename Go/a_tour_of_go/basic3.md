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



