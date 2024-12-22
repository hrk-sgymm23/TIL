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


## Buffered Channels

https://go-tour-jp.appspot.com/concurrency/3

チャネルはバッファとして使うことができる。
バッファを持つチャネルを初期化するには`make`の２つ目の引数にバッファを与える。

```go
ch := make(chan int, 100)
```

バッファが詰まった時はチャネルへの送信をブロックする。バッファがからのときはチャネルの受信をブロックする。

```go
package main

import "fmt"

func main() {
	ch := make(chan int, 3)
	ch <- 1
	ch <- 3
	ch <- 2 // チャネルへのデータ送信を増やすとデッドロックになる

	fmt.Println(<-ch)
	fmt.Println(<-ch)
	fmt.Println(<-ch)
}
// 1
// 3
// 2
```

## Range and Close

https://go-tour-jp.appspot.com/concurrency/4

送り手はこれ以上の値の送信する値がないことを示すためチャネルを`close`できる。
受けては受信の式にパラメータを渡すことでチャネルが``close`されているかどうかを確認することができる。

```go
v, ok := <-ch
```

受信する値がないかつチャネルが閉じているなら`ok`の変数は`false`になる。
ループの`for i range c`はチャネルが閉じられるまでチャネルから値を繰り返し受信時続ける。


```go
package main

import (
	"fmt"
)

func fibonacci(n int, c chan int) {
	x, y := 0, 1
	for i := 0; i < n; i++ {
		c <- x
		x, y = y, x+y
	}
	close(c) // closeをつかわないrangeを使ったループを終了できない
}

func main() {
	c := make(chan int, 10)
	go fibonacci(cap(c), c) //capはバッファサイズを取得する
	for i := range c {
		fmt.Println(i)
	}
}
// 0
// 1
// 1
// 2
// 3
// 5
// 8
// 13
// 21
// 34
```

## Select 

https://go-tour-jp.appspot.com/concurrency/5

`select`ステートメントはgoroutineを複数操作で待たせる。
`select`は複数ある`case`のいずれが準備できるようになるまでブロックし、`case`の準備ができたら実行する。
もし複数の`case`の準備ができている場合、`case`はランダムに選択される。

```go
package main

import "fmt"

func fibonacci(c, quit chan int) {
	x, y := 0, 1
	for {
		select {
		case c <- x:
			x, y = y, x+y
		case <-quit:
			fmt.Println("quit")
			return
		}
	}
}

func main() {
	c := make(chan int)
	quit := make(chan int)
	go func() {
		for i := 0; i < 10; i++ {
			fmt.Println(<-c)
		}
		quit <- 0
	}()
	fibonacci(c, quit)
}
// 0
// 1
// 1
// 2
// 3
// 5
// 8
// 13
// 21
// 34
// quit
```

## Default Selection

https://go-tour-jp.appspot.com/concurrency/6

どの`case`も準備できていない時に実行する`default`がある

```go
select {
case i := <-c:
    // use i
default:
    // receiving from c would block
}
```

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	tick := time.Tick(100 * time.Millisecond)
	boom := time.After(500 * time.Millisecond)
	for {
		select {
		case <-tick:
			fmt.Println("tick.")
		case <-boom:
			fmt.Println("BOOM!")
			return
		default:
			fmt.Println("何もねえよ")
			time.Sleep(50 * time.Millisecond)
		}
	}
}

// 何もねえよ
// 何もねえよ
// tick.
// 何もねえよ
// 何もねえよ
// tick.
// 何もねえよ
// 何もねえよ
// tick.
// 何もねえよ
// 何もねえよ
// tick.
// 何もねえよ
// 何もねえよ
// BOOM!
```

## WIP: Exercise: Equivalent Binary Trees

https://go-tour-jp.appspot.com/concurrency/8

```go
package main

import (
	"fmt"
	"golang.org/x/tour/tree"
)

// Walk walks the tree t sending all values
// from the tree to the channel ch.
func Walk(t *tree.Tree, ch chan int) {
	walk(t, ch)
	close(ch)
}

func walk(t *tree.Tree, ch chan int) {
	if t == nil {
		return
	}
	walk(t.Left, ch)
	ch <- t.Value
	walk(t.Right, ch)
}

// Same determines whether the trees
// t1 and t2 contain the same values.
func Same(t1, t2 *tree.Tree) bool {
	c1, c2 := make(chan int), make(chan int)
	go Walk(t1, c1)
	go Walk(t2, c2)
	for {
		v1, ok1 := <-c1
		v2, ok2 := <-c2
		switch {
		case !ok1, !ok2:
			return ok1 == ok2
		case v1 != v2:
			return false
		}
	}
}

func main() {
	ch := make(chan int)
	go Walk(tree.New(1), ch)
	for i := range ch {
		fmt.Println(i)
	}
	fmt.Println(Same(tree.New(1), tree.New(1)))
	fmt.Println(Same(tree.New(1), tree.New(2)))
}
// 1
// 2
// 3
// 4
// 5
// 6
// 7
// 8
// 9
// 10
// true
// false
```

## sync.Mutex

https://go-tour-jp.appspot.com/concurrency/9

コンフリクトを避けるために一度に一つだけのgoroutineが変数へアクセスできるようにしたい場合はどうするか？
排他制御(mutual exclusion)と呼ばれ、このデータ構造を指す一般的な名前は`mutex`。

Goの標準ライブラリは排他制御を`sync.Mutex`と次の2つのメソッドで表す。
- Lock
- Unlock

> Inc メソッドにあるように、 Lock と Unlock で囲むことで排他制御で実行するコードを定義できます。
> Value メソッドのように、mutexがUnlockされることを保証するために defer を使うこともできます。

```go
package main

import (
	"fmt"
	"sync"
	"time"
)

// SafeCounter is safe to use concurrently.
type SafeCounter struct {
	mu sync.Mutex
	v  map[string]int
}

// Inc increments the counter for the given key.
func (c *SafeCounter) Inc(key string) {
	c.mu.Lock()
	// Lock so only one goroutine at a time can access the map c.v.
	c.v[key]++
	c.mu.Unlock()
}

// Value returns the current value of the counter for the given key.
func (c *SafeCounter) Value(key string) int {
	c.mu.Lock()
	// Lock so only one goroutine at a time can access the map c.v.
	defer c.mu.Unlock()
	return c.v[key]
}

func main() {
	c := SafeCounter{v: make(map[string]int)}
	for i := 0; i < 1000; i++ {
		go c.Inc("somekey")
	}

	time.Sleep(time.Second)
	fmt.Println(c.Value("somekey"))
}
// 1000
```

## Exercise: Web Crawler

https://go-tour-jp.appspot.com/concurrency/10

https://qiita.com/rock619/items/f412d1f870a022c142d0#exercise-web-crawler

```go
package main

import (
	"fmt"
	"sync"
)

type Fetcher interface {
	// Fetch returns the body of URL and
	// a slice of URLs found on that page.
	Fetch(url string) (body string, urls []string, err error)
}

// Crawl uses fetcher to recursively crawl
// pages starting with url, to a maximum of depth.
func Crawl(url string, depth int, fetcher Fetcher) {
	cache := struct {
		visited map[string]bool
		sync.Mutex
	}{
		visited: make(map[string]bool),
	}
	var wg sync.WaitGroup
	var crawl func(string, int)
	crawl = func(url string, depth int) {
		if depth <= 0 {
			return
		}
		cache.Lock()
		if cache.visited[url] {
			cache.Unlock()
			return
		}
		cache.visited[url] = true
		cache.Unlock()
		body, urls, err := fetcher.Fetch(url)
		if err != nil {
			fmt.Println(err)
			return
		}
		fmt.Printf("found: %s %q\n", url, body)
		wg.Add(len(urls))
		for _, u := range urls {
			go func(u string) {
				crawl(u, depth-1)
				wg.Done()
			}(u)
		}
	}
	crawl(url, depth)
	wg.Wait()
}

func main() {
	Crawl("https://golang.org/", 4, fetcher)
}

// fakeFetcher is Fetcher that returns canned results.
type fakeFetcher map[string]*fakeResult

type fakeResult struct {
	body string
	urls []string
}

func (f fakeFetcher) Fetch(url string) (string, []string, error) {
	if res, ok := f[url]; ok {
		return res.body, res.urls, nil
	}
	return "", nil, fmt.Errorf("not found: %s", url)
}

// fetcher is a populated fakeFetcher.
var fetcher = fakeFetcher{
	"https://golang.org/": &fakeResult{
		"The Go Programming Language",
		[]string{
			"https://golang.org/pkg/",
			"https://golang.org/cmd/",
		},
	},
	"https://golang.org/pkg/": &fakeResult{
		"Packages",
		[]string{
			"https://golang.org/",
			"https://golang.org/cmd/",
			"https://golang.org/pkg/fmt/",
			"https://golang.org/pkg/os/",
		},
	},
	"https://golang.org/pkg/fmt/": &fakeResult{
		"Package fmt",
		[]string{
			"https://golang.org/",
			"https://golang.org/pkg/",
		},
	},
	"https://golang.org/pkg/os/": &fakeResult{
		"Package os",
		[]string{
			"https://golang.org/",
			"https://golang.org/pkg/",
		},
	},
}

// found: https://golang.org/ "The Go Programming Language"
// found: https://golang.org/pkg/ "Packages"
// found: https://golang.org/ "The Go Programming Language"
// found: https://golang.org/pkg/ "Packages"
// not found: https://golang.org/cmd/
// not found: https://golang.org/cmd/
// found: https://golang.org/pkg/fmt/ "Package fmt"
// found: https://golang.org/ "The Go Programming Language"
// found: https://golang.org/pkg/ "Packages"
// found: https://golang.org/pkg/os/ "Package os"
// found: https://golang.org/ "The Go Programming Language"
// found: https://golang.org/pkg/ "Packages"
// not found: https://golang.org/cmd/
```


