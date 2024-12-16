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

```go
package main

import "fmt"

type Vertex struct {
	X, Y float64
}

func (v *Vertex) Scale(f float64) {
	v.X = v.X * f
	v.Y = v.Y * f
}

func ScaleFunc(v *Vertex, f float64) {
	v.X = v.X * f
	v.Y = v.Y * f
}

func main() {
	v := Vertex{3, 4}
	v.Scale(2)
	ScaleFunc(&v, 10)

	p := &Vertex{4, 3} // ポインタ型として宣言
	p.Scale(3)
	ScaleFunc(p, 8)

	fmt.Println(v, p)
}
// {60 80} &{96 72}
```

## Methods and pointer indirection (2)

https://go-tour-jp.appspot.com/methods/7

例のコード
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

func AbsFunc(v Vertex) float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func main() {
	v := Vertex{3, 4}
	fmt.Println(v.Abs())
	fmt.Println(AbsFunc(v))

	p := &Vertex{4, 3}
	fmt.Println(p.Abs())
	fmt.Println(AbsFunc(*p))
}
// 5
// 5
// 5
// 5
```

変数の引数を取る関数は、特定の型の引数を取る必要がある。
```go
var v Vertex
fmt.Println(AbsFunc(v))  // OK
fmt.Println(AbsFunc(&v)) // Compile error!
```

メソッドが変数レシーバである場合、呼び出し時に、変数、またはポインタのいずれかのレシーバとしてとることができる。
```go
var v Vertex
fmt.Println(v.Abs()) // OK
p := &v
fmt.Println(p.Abs()) // OK
```

## Choosing a value or pointer receiver

https://go-tour-jp.appspot.com/methods/8

ポインタレシーバを使う理由は2つある。
- 一つはメソッドがレシーバが指す先の変数を変更するため。
- 二つ目は、メソッドの呼び出し毎に変数のコピーを避けるため。例えばレシーバがおおきな構造体である場合に効率的。


`Abs`メソッドはレシーバ自身を変更する必要はありませんが、`Scale`と`Abs`は両方とも`*Vertex`型のレシーバです。
> 一般的には、値レシーバ、または、ポインタレシーバのどちらかですべてのメソッドを与え、混在させるべきではありません。

```go
package main

import (
	"fmt"
	"math"
)

type Vertex struct {
	X, Y float64
}

func (v *Vertex) Scale(f float64) {
	v.X = v.X * f
	v.Y = v.Y * f
}

func (v *Vertex) Abs() float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func main() {
	v := &Vertex{3, 4}
	fmt.Printf("Before scaling: %+v, Abs: %v\n", v, v.Abs())
	v.Scale(5)
	fmt.Printf("After scaling: %+v, Abs: %v\n", v, v.Abs())
}
// Before scaling: &{X:3 Y:4}, Abs: 5
// After scaling: &{X:15 Y:20}, Abs: 25
```

## Interfaces/Interfaces are implemented implicitly

https://go-tour-jp.appspot.com/methods/9
https://go-tour-jp.appspot.com/methods/10

interfacea型はメソッドのシグニチャの集まりとして定義する。
そのメソッドの実装した値を、interface型の変数へ渡すことができる。

型にメソッドを実装していくことによって、インターフェース実装になる。
インターフェースを実装することを明示的に宣言する必要はない("implements" キーワードは必要ない)

```go
package main

import "fmt"

type I interface {
	M()
}

type T struct {
	S string
}

// This method means type T implements the interface I,
// but we don't need to explicitly declare that it does so.
func (t T) M() {
	fmt.Println(t.S)
}

func main() {
	var i I = T{"hello"}
	i.M()
}
// hello
```

## Interface values

https://go-tour-jp.appspot.com/methods/11

下記のようにインターフェースの値は、値と具体的な型のタプルのように考えられる。

```go
(value, type)
```

インターフェースの値は、特定の基底になる具体的な型の値を保持する。
インターフェースの値のメソッドを呼び出すと、その基底型の同じ名前のメソッドが呼び出される。

```go
package main

import (
	"fmt"
	"math"
)

type I interface {
	M()
}

type T struct {
	S string
}

func (t *T) M() {
	fmt.Println(t.S)
}

type F float64

func (f F) M() {
	fmt.Println(f)
}

func main() {
	var i I

	i = &T{"Hello"}
	describe(i)
	i.M()

	i = F(math.Pi)
	describe(i)
	i.M()
}

func describe(i I) {
	fmt.Printf("(%v, %T)\n", i, i)
}

```

### 解説
コード全体の流れ
- インターフェース`I`...メソッド`M`を持つ
- 構造体`T`と型`F`...それぞれが`I`を実装する具体的な型
- `main`関数...インターフェーズ型`I`に`T`と`F`を代入

- `describe`
  - 引数`i`の値と型を表示する
```go
func describe(i I) {
	fmt.Printf("(%v, %T)\n", i, i)
}
```

**ポリモーフィズム**
- インターフェース型`I`を使うことで異なる型(`*T`と`F`)を統一的に扱っている。

> *T のポインタ型で M() を実装 → ポインタ型のみ I を実装。
```go
func (t *T) M() {
	fmt.Println(t.S)
}
```

> F は値レシーバで M() を実装 → 値型もポインタ型も I を実装。
```go
func (f F) M() {
	fmt.Println(f)
}
```

## Interface values with nil underlying values

https://go-tour-jp.appspot.com/methods/12

インターフェースの具体的な値がnilの場合、メソッドはnilをレシーバとして呼び出される。

> Go では nil をレシーバーとして呼び出されても適切に処理するメソッドを記述するのが一般的です(この例では M メソッドのように)。
> 具体的な値として nil を保持するインターフェイスの値それ自体は非 nil であることに注意してください。

```go
package main

import "fmt"

type I interface {
	M()
}

type T struct {
	S string
}

func (t *T) M() {
	if t == nil {
		fmt.Println("<nil>")
		return
	}
	fmt.Println(t.S)
}

func main() {
	var i I

	var t *T
	i = t
	describe(i)
	i.M()

	i = &T{"hello"}
	describe(i)
	i.M()
}

func describe(i I) {
	fmt.Printf("(%v, %T)\n", i, i)
}
// (<nil>, *main.T)
// <nil>
// (&{hello}, *main.T)
// hello
```

## Nil interface values

https://go-tour-jp.appspot.com/methods/13

`nil`インターフェースの値は、値も具体的な型も保持しない
呼び出す具体的なメソッドを示すかたがインターフェースないのタプルに存在しないため、nilインターフェースのメソッドを呼び出すとランタイムエラーになる。

```go
package main

import "fmt"

type I interface {
	M()
}

func main() {
	var i I
	describe(i)
	i.M()
}

func describe(i I) {
	fmt.Printf("(%v, %T)\n", i, i)
}

// (<nil>, <nil>)
// panic: runtime error: invalid memory address or nil pointer dereference
// [signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x490959]

// goroutine 1 [running]:
// main.main()
	// /tmp/sandbox1141676745/prog.go:12 +0x19
```

`i`が`nil`の場合、インターフェースには型もメソッドも関連づけられないため`i.M()`はエラーになる




