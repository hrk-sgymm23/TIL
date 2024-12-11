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

例では *Vertex に Scale メソッドが定義されている
ポインタレシーバを持つメソッド(ここでは`Scale`)はレシーバが指す変数を変更できる。
レシーバ自身を更新することが多いため、変数レシーバーよりポインタレシーバの方が一般的。

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

func (v *Vertex) Scale(f float64) {
	v.X = v.X * f
	v.Y = v.Y * f
}

func main() {
	v := Vertex{3, 4}
	v.Scale(10)
	fmt.Println(v.Abs())
}
```

# ポインタレシーバと変数レシーバの違いについて

## ポインタレシーバ

### コード

```go
func (v *Vertex) Scale(f float64) {
	v.X = v.X * f
	v.Y = v.Y * f
}
```

- `*Vertex`...`Scale`メソッドのレシーバはポインタ型レシーバ
- メソッド内部で`v.X`,`v.Y`を変更するとその元のオブジェクトが変更される。

### 実行結果
```go
v := Vertex{3, 4}
v.Scale(10)
fmt.Println(v.Abs())
```

- `v.Scale(10)`メソッド内にて`3*10`,`4*10`が行われる
- `v.Abs`メソッドにて`√(30² + 40²) = 50`が計算される。

## 変数レシーバ

### コード
```go
func (v Vertex) Scale(f float64) {
	v.X = v.X * f
	v.Y = v.Y * f
}
```

- `Vertex`...`Scale`メソッドのレシーバは変数型レシーバ
- メソッド内部で`v.X`,`v.Y`を変更するとその元のオブジェクトが変更されない。

### 実行結果
```go
v := Vertex{3, 4}
v.Scale(10)
fmt.Println(v.Abs())
```

- `v.Scale(10)`メソッド内にてのx,yの値の変更はなし
- `v.Abs`メソッドにて`√(3² + 4²) = 5`が計算される。

## Methods and pointer indirection

https://go-tour-jp.appspot.com/methods/6

下の2つの呼び出しを比べると、ポインタを引数に取る ScaleFunc 関数は、ポインタを渡す必要があることに気がつく

```go
var v Vertex
ScaleFunc(v, 5)  // Compile error!
ScaleFunc(&v, 5) // OK
```

メソッドがポインタレシーバである場合、呼び出し時に変数、または、ポインタのいずれかのレシーバとして受け取ることができる。
```go
var v Vertex
v.Scale(5)  // OK
p := &v
p.Scale(10) // OK
```
`v.Scale(5)`のステートメントでは`v`は変数でありポインタではない。メソッドでポインタレシーバが自動的に呼び出される。
`Scale`メソッドはポインタレシーバを持つ場合、Goは利便性を保つため、v.Scale(5) のステートメントを (&v).Scale(5) として解釈




