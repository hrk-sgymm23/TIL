# 第２章 名前に情報を詰め込む

## 鍵となる考え
**名前に情報を詰め込む**

## 6つのテーマ
- 明確な単語を選ぶ
- 汎用的な名前を避ける(あるいは、使う状況を使う状況を選ぶ)
- 抽象的な名前より具体的な名前を使う
- 接尾辞や接頭辞を使って情報を追加する
- 名前の長さを決める
- 名前のフォーマットで情報を伝える

＃＃　明確な単語を選ぶ
- 「名前に情報を詰め込む」には、明確な単語を選ばなければならない。「空虚な単語」は避けるべき。
- 例えば`get`はあまり明確な単語ではない。
```java
def GetPage(url):
  ...
```
しかし上記`GetPage`では伝わってこない。ページはキャッシュから？DBから？
インターネットであれば`FetchPage()`や`DownloadPage()`の方が明確。


- `BinaryTree`クラスの例
```java
class BinaryTree {
  int Size();
};
```
上記Size()メソッドは何を返すのだろうか。ツリーの高さ？ノードの数？ツリーのメモリの消費量？
目的に適した名前をつけるなら`Height()`,`'NumNodes()`,`MemoryBytes()`になる。


- `Thread`クラスの例
```java
class Thread {
  void stop();
  ...
};
```
`Stop()`という名前でも良いが、動作にあわえてもっと明確な名前をつけた方が良い。
例えば、取り消しができない重い動作なら`kill()`にするといい。
後から`Resume()`できるなら`Pouse()`にしてもいい。

## もっとカラフルな単語を探す
- シソーラス(類語辞典)を使って調べる

`send`...`deliver`, `dispatch`, `announce`, `distribute`, `route`

`find`...`search`, `extract`, `locate`, `recover`

`start`...`launch`, `create`, `begin`, `open`

`make`...`create`, `set up`, `build`, `generate`, `compose`, `add`, `new`

## `tmp`や`retval`など汎用的な名前を避ける
- このような「空虚な名前」をつけるのではなく、**エンティティの値や目的を表した名前を選ぼう**

### `tmp`の怠慢な使い方
```javascript
let tmp = user.name 
tmp += user.phone_number
tmp += user.email
tmp += user.address
// 以下同様の処理
template.set("user_info", tmp)
```
上記の例では「一時保管」ではなく「ユーザーの情報を何度も書き換えられる変数」として利用される。
上記では`user_info`という命名がふさわしい。

反対に以下は`tmp`の例として適している。
```javascript
// 2つの変数の中身を入れ替えるコード
if(right < left){
  tmp = right
  right = left
  left = tmp
}
```
**`tmp`は生存期間が短く一時的な保管としての意味合いがある**

# 抽象的な名前より具体的な名前を使う

## ループイテレータ
- `i`,`j`,`k`,`iter`よりいい名前がある時もある。
- 例えば、クラブに所属しているユーザーを調べるループの例。
```javascript
for (let i = 0; i < clubs.size; i++) {
  for (let j = 0; j < clubs[i].members.size; j++) {
    for (let k = 0; k < users.size; k++) {
      if(clubs[i].members[k] === users[j]){
      }
    }
  }
}
```
- ループの処理のネストが増えると、イテレータの数が多くなってしまい、最後のif文において`members`,`users`のインデックス(k,j)が逆になる。
- イテレータが複数ある時、にはインデックスに最も明確な名前をつけると良い。
  - `i`,`k`,`j`ではなく説明的な名前(`clubs_i`,`members_i`,`user_i`)または(`ci`,`mi`,`ui`)にする
 
## 汎用的な名前のまとめ
### アドバイス
**`tmp`,`it`,`retval`のような汎用的な名前を使うときは、それ相応の理由を用意する**

## 名前の情報を追加する
- 例えば16進数の文字列を持つ変数について
  - idのフォーマットが大切な場合は`hex_id`が望ましい。

### 名前に情報が少ない変数
```javascript
var start = (new.Date()).getTime()
console.log(`開始時間は${start}秒`)
```
`getTime()`ではミリ秒を返すため、`start`を`strat_ms`とする。

関数の仮引数→単位を追加した仮引数
Start(int  `delay`)→`delay_secs`
CreateCache(int `size`)→`size_mb`
ThlotteleDownload(float `limit`)→`maxkbps`
Rotate(float `angle`)→`degreees_angle`



