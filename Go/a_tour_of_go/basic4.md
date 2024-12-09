## Methods

https://go-tour-jp.appspot.com/methods/1

Goにはクラスはないがメソッドは定義できる。メソッドは特別なレシーバーを引数に取る。レシーバーは`func`キーワードとメソッドの間に自身の引数リストを表現する。

>  Abs メソッドは v という名前の Vertex 型のレシーバを持つことを意味しています。
```go
package main

import (
	"fmt"
	"math"
)

type Vertex struct {
	X, Y float64
}

func (v Vertex) Abs() float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func main() {
	v := Vertex{3, 4}
	fmt.Println(v.Abs())
}
```

## Methods are functions

https://go-tour-jp.appspot.com/methods/2

上記の関数は以下のように定義できる

```go
func Abs(v Vertex) float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}
```

## Methods continued

`struct`型だけでなく他の型にもメソッドを宣言できる。
下記は`Abs`メソッドを持つ数値型の`MyFloat`型。
レシーバをも伴うメソッドの宣言は、レシーバ型が同じパッケージ内にある必要がある。

他のパッケージに定義している型に対してレシーバーを宣言できない(組み込みの int などの型も同様)

```go
package main

import (
	"fmt"
	"math"
)

type MyFloat float64

func (f MyFloat) Abs() float64 {
	if f < 0 {
		return float64(-f)
	}
	return float64(f)
}

func main() {
	f := MyFloat(-math.Sqrt2)
	fmt.Println(f.Abs())
}
```

## Pointer receivers

https://go-tour-jp.appspot.com/methods/4

ポインタレシーバでメソッドを宣言できる。
これはレシーバーの型が、ある型`T`への構文`*T`があることを示す。(なお`T`は`*int`のようにポインタ自体をとることはできない)



