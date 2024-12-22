## Goroutines

https://go-tour-jp.appspot.com/concurrency/1

ゴルーチンはGoのランタイムに管理される軽量なスレッドのこと。

```go
go f(x, y, z)
```
上記のようにかけば新しいgorutineが実行される

```go
f(x, y, z)
```
`f`,`x`,`y`,`z`の評価は実行元のgorutineで実行され、`f`の実行は、新しいgoroutineで実行される。

goroutineは同じアドレス空間で実行されるため、共有メモリへのアクセスは必ず同期する必要がある。

```go
package main

import (
	"fmt"
	"time"
)

func say(s string) {
	for i := 0; i < 5; i++ {
		time.Sleep(100 * time.Millisecond)
		fmt.Println(s)
	}
}

func main() {
	go say("world")
	say("hello")
}
// world
// hello
// hello
// world
// world
// hello
// hello
// world
// world
// hello
// 実行順序は保証されない
```

## Channels

https://go-tour-jp.appspot.com/concurrency/2

チャネル(`Channel`)型は、チャネルオペレータの`<-`を用いて値の送受信ができる通り道です。

```go
ch <- v    // v をチャネル ch へ送信する
v := <-ch  // ch から受信した変数を v へ割り当てる
```
データは矢印の方向へ流れる

マップとスライスのようにチャンネルを使う場合は以下のように生成する。

```go
ch := make(chan int)
```

通常は片方が準備できるまで送受信はブロックされる。これにより明確なロックや条件変数がなくてもgoroutinenの同期を可能にする。


```go
package main

import "fmt"

func sum(s []int, c chan int) {
	sum := 0
	for _, v := range s {
		sum += v
	}
	c <- sum // send sum to c
}

func main() {
	s := []int{7, 2, 8, -9, 4, 0}

	c := make(chan int)
	go sum(s[:len(s)/2], c) // 配列の前半取得
	go sum(s[len(s)/2:], c) // 配列の後半取得
	x, y := <-c, <-c // receive from c

	fmt.Println(x, y, x+y)
}
// -5 17 12
```

上位のコードはスライス内の数値を合算し2つのgoroutine間で作業を分配する。
両方のgoroutine間で作業が完了すると最終結果が示される。

解説
```go
c := make(chan int)
go sum(s[:len(s)/2], c) // 配列の前半取得
go sum(s[len(s)/2:], c) // 配列の後半取得
```

上記にて`c`が上書きされない理由
```go
c <- sum
```
上記にてチャネルへ格納することでチャネル内のキュー(FIFO)に値が格納される

```go
x, y := <-c, <-c // receive from c
fmt.Println(x, y, x+y)
```

上記の計算結果が`-5 17 12`となり配列の後半の計算結果が`x`にはいるにはFIFOの影響


