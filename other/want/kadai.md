# want 課題

https://docs.google.com/document/d/1PK_sGhTurmZHJ3OQsij11zxLCOruBoHwqtHzy419QZE/edit?tab=t.0

# 作業メモ

## `Data.define`

`Data`クラスにサブクラスを作成しそれを返す
https://docs.ruby-lang.org/ja/latest/method/Data/s/define.html

```ruby
Dog = Data.define(:name, :age)
fred = Dog.new("Fred", 5)
p fred.name # => "Fred"
p fred.age  # => 5
```

# やるべきこと
```
- 設計方針を複数考える
- interleave関数の実装
- テストケース作成(マニュアル/テストコード)
```

# 設計方針を考える

