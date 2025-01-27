# 1. インターリーブ機能の設計方針によってはいくつかの観点でトレードオフが発生します。実装方針をいくつか挙げその中からどれか一つを理由を明確にし選んでください。

## 方針1: ページネーション分のIDを取得後にインターリーブ処理を実行

### 方針1: ページネーション分のIDを取得後にインターリーブ処理
- ページ番号と1 ページあたりのアイテム数を基に、ページに必要なデータの範囲を計算。
- 各アルゴリズムで、必要な範囲だけの ID を事前に取得。
- 例: 新アルゴリズム、旧アルゴリズムでそれぞれ1ページあたりに表示する範囲のデータを取得。必要なデータが揃った後に、インターリーブ処理を行い、結果を整形。


## 方針2: ID全件取得後、インターリーブ処理をかけてページネーション分に分割
- 新アルゴリズムと旧アルゴリズムから、全件の ID をそれぞれ取得。
- 全件のデータをインターリーブ処理して、交互に並べた結果を作成。
- 作成した結果をページネーションに基づいて、必要な範囲を切り出して返却。

## 決定した方針

### 選んだ方針: 方針2
- 方針1のページネーションを実装する方法の例としてリクエストされた該当するページのIDを取得することがバックエンドサーバー、DBへの負担を軽減することにつながる。
- しかしID取得のアルゴリズム内で取得するIDに更新などがあった際にデータの重複がありデータの選出の正確性に問題が出る可能性がある。
- 一方で方針の2ではIDを全件取得するため、バックエンドサーバー、DBへの負担が懸念されるが全件に対してインターリーブ処理とページネーションの分割を行うため、データ選出の正確性を担保することができる。
- 今回の目的である新旧のアルゴリズムを比較するためのインターリーブし検証することであるため、データ選出の正確性を担保することのプライオリティーが一番高くなる。
- よって方針2を選択した。

# 2. interleaving 関数を実装してください。

`main.rb`
```ruby
JobPost = Data.define(:id, :source)

# @param [Integer] user_id アクセスしたユーザーのID
# @param [Integer] page ページ番号（1から始まる）
# @param [Integer] per_page 1ページあたりの要求するアイテム数（基本は10だが、場合によって異なる）
# @return [Array<JobPost>] 募集のリスト
def interleaving(user_id, page, per_page)
  new_algo_results = new_algorithm(user_id, page, per_page)
  old_algo_results = old_algorithm(user_id, page, per_page)

  interleaved_list = new_algo_results.zip(old_algo_results).flatten.uniq.compact
  start_idx = (page - 1) * per_page
  end_idx = start_idx + per_page - 1
  page_data = interleaved_list[start_idx..end_idx]

  return [] if page_data.nil?
  page_data.map.with_index do |id, i|
    JobPost.new(id: id, source: i.even? ? :new_algorithm : :old_algorithm)
  end
end

# @param [Integer] user_id アクセスしたユーザーのID
# @param [Integer] page ページ番号（1から始まる）
# @param [Integer] per_page 1ページあたりの要求するアイテム数（基本は10だが、場合によって異なる）
# @return [Array<Integer>] 募集のIDのリスト
def new_algorithm(user_id, page, per_page)
    ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    ids[(page - 1) * per_page..page * per_page - 1]
end

def old_algorithm(user_id, page, per_page)
    ids = [15, 21, 6, 23, 30, 1, 7, 14, 29, 12, 24, 18, 10, 13, 20, 3, 22, 27, 26, 11, 4, 5, 9, 17, 28, 8, 2, 19, 16, 25]
    ids[(page - 1) * per_page..page * per_page - 1]
end

```


# 3. 作成した interleaving 関数のテストケースを挙げてください。

- `test.rb`を用意し`main.rb`から関数を読み込みテストを行う

## ディレクトリ構成

```sh
tree .
.
├── main.rb
└── test.rb
```

`test.rb`

```ruby
require 'test/unit'
require_relative 'main'

class TestInterleaving < Test::Unit::TestCase
  def setup
    @user_id = 1
    @per_page = 10
    # 以下仮の総データを用意
    @new_algo_results = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    @old_algo_results = [15, 21, 6, 23, 30, 1, 7, 14, 29, 12, 24, 18, 10, 13, 20, 3, 22, 27, 26, 11, 4, 5, 9, 17, 28, 8, 2, 19, 16, 25]
    @all_data_length = (@new_algo_results + @old_algo_results).uniq.size
    @total_pages = total_page_count(@all_data_length, @per_page)
  end

  def total_page_count(all_data_length, per_page)
    (all_data_length.to_f / per_page).ceil
  end

  # 異なるページ間で重複がないことを確認
  def test_no_duplicates_across_pages2
    all_ids = []
    duplicate_ids = []
    (1..@total_pages + 1).each do |page|
        all_ids = interleaving(@user_id, page, @per_page)
        duplicate_ids = duplicate_ids & all_ids
    end

    unless duplicate_ids.empty?
        assert(false, "Duplicate IDs found across pages: #{duplicate_ids}")
    end
  end

  # 各ページで募集数が per_page を超えないことを確認
  def test_no_extra_items_per_page
    (1..@total_pages + 1).each do |page|
      page_data = interleaving(@user_id, page, @per_page)
      assert(page_data.size <= @per_page, "Page #{page} contains more items than allowed") if page_data.any?
    end
  end

  # new_algorithm と old_algorithm で返された募集がすべて interleaving で返されることを確認
  def test_no_item_missed
    all_algo_data_list = []
    (1..@total_pages + 1).each do |page|
        page_per_data_list = new_algorithm(@user_id, page, @per_page) + old_algorithm(@user_id, page, @per_page)
        all_algo_data_list.concat(page_per_data_list)
    end

    expect_data_list = (@new_algo_results.concat(@old_algo_results)).sort
    unless all_algo_data_list.sort == expect_data_list
        assert(false, "Error: The values do not match.")
    end
  end
end
```

## テストを実行
```sh
$ ruby test.rb

Loaded suite test
Started
Finished in 0.001434375 seconds.
-------------------------------------------------------------------------------------------------------------------------------------------
3 tests, 2 assertions, 0 failures, 0 errors, 0 pendings, 0 omissions, 0 notifications
100% passed
-------------------------------------------------------------------------------------------------------------------------------------------
2091.50 tests/s, 1394.34 assertions/s
```


# 利用したプロンプト
```
- REST APIにおけるページネーションの設計方針と実装方法を教えて
- REST APIにおけるページネーションとインターリーブを組み合わせるにあたって考慮すべきことを教えて
- rubyのユニットテストをやり方を教えて
- (main.rbを共有した状態で)上記コードに対してテストコードを書いてみて
- (日本語で作成しらエラー文を添えた上で)上記の文章を英訳して

```
