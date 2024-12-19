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

## The empty interface

https://go-tour-jp.appspot.com/methods/14

0個のメソッドが指定されたインターフェース型は、空のインターフェースと呼ばれる
```go
interface{}
```

空のインターフェースは任意の型の値を保持できる(全ての型は少なくともゼロ個のメソッドを実装している)
空のインターフェースは未知の型を扱うコードで使用される

> 例えば、 fmt.Print は interface{} 型の任意の数の引数を受け取ります。

```go
package main

import "fmt"

func main() {
	var i interface{}
	describe(i)

	i = 42
	describe(i)

	i = "hello"
	describe(i)
}

func describe(i interface{}) {
	fmt.Printf("(%v, %T)\n", i, i)
}
// (<nil>, <nil>)
// (42, int)
// (hello, string)
```

## Type assertions

https://go-tour-jp.appspot.com/methods/15

型アサーション は、インターフェースの値の基になる具体的な値を利用する手段を提供します。

```go
t := i.(T)
```

この文はインターフェースの値が`i`が具体的な型`T`を保持し基になる`T`の値を変数`t`を代入することを宣言。
`i`が`T`を保持していない場合はこの分はpanicを起こす。

インターフェースの値が特定の方を保持しているかどうかをテストするために型アサーションは2つの値を返すことができる。
> 基になる値とアサーションが成功したかどうかを報告するブール値)

```go
t, ok := i.(T)
```
`i`が`T`を保持してれば、`t`は基になる値になり`ok`は`true`になる。
そうでなければ`ok`は`false`になる。`t`は型`T`のゼロ値になりpanicは起きない。

```go
package main

import "fmt"

func main() {
	var i interface{} = "hello"

	s := i.(string)
	fmt.Println(s)

	s, ok := i.(string)
	fmt.Println(s, ok)

	f, ok := i.(float64)
	fmt.Println(f, ok)

	f = i.(float64) // panic
	fmt.Println(f)
}
// hello
// hello true
// 0 false
// panic: interface conversion: interface {} is string, not float64

// goroutine 1 [running]:
// main.main()
	// /tmp/sandbox299776260/prog.go:17 +0x14f

```

## Type switches

https://go-tour-jp.appspot.com/methods/16

型`switch`はいくつかの型アサーションを直列に使用できる構造。
型`switch`は通常の`switch`文と似ているが型`switch`の`case`は型を指定し、それらの値は指定されたインターフェースの値が保持する値の型と比較される。

```go
switch v := i.(type) {
case T:
    // here v has type T
case S:
    // here v has type S
default:
    // no match; here v has the same type as i
}
```

型の`switch`の宣言は、型アサーション`i.(T)`と同じ構文を持つが、特定の型`T`はキーワード`type`に置き換得られる。

上記switch文はインターフェースの値`i`が型`T`または型`S`の値を保持するかどうかをテストする。
`T`及び`S`の各`case`において、変数`v`はそれぞれ型`T`または`S`であり、`i`によって保持される値を保持される。
defaultの場合(値が一致しない場合)、変数`v`は同じインターフェース型で値は`i`となる。

```go
package main

import "fmt"

func do(i interface{}) {
	switch v := i.(type) {
	case int:
		fmt.Printf("Twice %v is %v\n", v, v*2)
	case string:
		fmt.Printf("%q is %v bytes long\n", v, len(v))
	default:
		fmt.Printf("I don't know about type %T!\n", v)
	}
}

func main() {
	do(21)
	do("hello")
	do(true)
}
// Twice 21 is 42
// "hello" is 5 bytes long
// I don't know about type bool!
```

## Stringers

https://go-tour-jp.appspot.com/methods/17

> もっともよく使われているinterfaceの一つに fmt パッケージ に定義されている Stringer があります

```go
type Stringer interface {
    String() string
}
```

`Stringer`インターフェースは`string`として表現することができる型です。
`fmt`パッケージでは変数を文字列で出力うるためにインターフェースがあることを確認する。

```go
package main

import "fmt"

type Person struct {
	Name string
	Age  int
}

func (p Person) String() string {
	return fmt.Sprintf("%v (%v years)", p.Name, p.Age)
}

func main() {
	a := Person{"Arthur Dent", 42}
	z := Person{"Zaphod Beeblebrox", 9001}
	fmt.Println(a, z)
}
// Arthur Dent (42 years) Zaphod Beeblebrox (9001 years)
```


## Exercise: Stringers

https://go-tour-jp.appspot.com/methods/18

```go
package main

import "fmt"

type IPAddr [4]byte

// TODO: Add a "String() string" method to IPAddr.
func (i IPAddr) String() string {
	return fmt.Sprintf("%v.%v.%v.%v", i[0], i[1], i[2], i[3])
}

func main() {
	hosts := map[string]IPAddr{
		"loopback":  {127, 0, 0, 1},
		"googleDNS": {8, 8, 8, 8},
	}
	for name, ip := range hosts {
		fmt.Printf("%v: %v\n", name, ip)
	}
}
// loopback: 127.0.0.1
// googleDNS: 8.8.8.8
```

上記解説

```go
type IPAddr [4]byte
```
上記配列は4つのバイト値(0~255の整数)を保持する。IPv4の表現に適している。

`String`メソッド
```go
func (i IPAddr) String() string {
	return fmt.Sprintf("%v.%v.%v.%v", i[0], i[1], i[2], i[3])
}
```
`IPAddr`型に紐づいたメソッド
メソッド名が`String()`であるため、この型をフォーマット指定子(例`%v`)で出力すると`String()`の返り値が使われる。

`main`関数
```go
hosts := map[string]IPAddr{
	"loopback":  {127, 0, 0, 1},
	"googleDNS": {8, 8, 8, 8},
}
```

`map[string]IPAddr`はキーが文字列、値が`IPAddr`型のマップ(辞書)
2つの値を変数に格納している。

```go
for name, ip := range hosts {
	fmt.Printf("%v: %v\n", name, ip)
}
```
値は`ip`だが`IPAddr`型であるが、`fmt.Printf`の`%v`フォーマット指定子を使うと自動的に`String()`メソッドが呼び出される
上記の`String`メソッド自動呼び出しは`fmt.Stringer`(標準メソッド)によるもの

> 型が String() メソッドを実装している場合、その型は Stringer インターフェースを満たしているとみなされます。
> fmt.Printf などの関数で %v や %s を使った場合、値が Stringer を満たしていれば、String() メソッドが自動的に呼び出され、その戻り値がフォーマット出力に使われます。


## Errors

https://go-tour-jp.appspot.com/methods/19

```go
```
