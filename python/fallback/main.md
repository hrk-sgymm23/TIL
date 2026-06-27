# フォールバックについて学ぶ

> フォールバック（Fallback）とは、システムで何かエラーや不具合が起きたときに、完全に止まってしまうのではなく、代替の手段（予備のプラン）に切り替えて処理を続行することです。
身近な例でいうと、「スマホで5Gが繋がらないときに、自動的に4Gに切り替わる」のもフォールバックの一種です。

## 簡単な例

ユーザーの設定がなければデフォルトで設定したthemeを返す
```python
user_profile = {"name": "タロウ", "age": 25}

# 'theme'（背景色）の設定があるか確認し、なければ 'light'（白）にする
# get(キー, フォールバック値) の形です
current_theme = user_profile.get("theme", "light")

print(f"現在のテーマ: {current_theme}")
# ユーザー設定に theme はないので、フォールバックされて 'light' が出力されます

# 1. 辞書に最初から 'theme': 'dark' を追加しておきます
user_profile["theme"] = "dark"

# 2. 'theme' を探します。今回は見つかるので、後ろの 'light' は無視されます
current_theme = user_profile.get("theme", "light")

print(f"現在のテーマ: {current_theme}")

現在のテーマ: light
現在のテーマ: dark
```

## 実践的な例

プライマリーのサーバから取得しにいき落ちていればセカンダリのサーバー、さらに落ちていればローカルを見に行く例

```python
import time


class NewsService:

    def __init__(self):
        # 模擬的なサーバーの状態（True = 正常, False = 障害発生）
        self.primary_server_alive = False
        self.backup_server_alive = False  # バックアップは生きている状態

    def _fetch_from_primary(self):
        """メインサーバーからの取得（シミュレーション）"""
        if not self.primary_server_alive:
            raise ConnectionError("メインサーバーが応答しません。")
        return ["メイン: 本日のニュースA", "メイン: 本日のニュースB"]

    def _fetch_from_backup(self):
        """バックアップサーバーからの取得（シミュレーション）"""
        if not self.backup_server_alive:
            raise ConnectionError("バックアップサーバーも応答しません。")
        return ["副系: [保存済] ニュースA", "副系: [保存済] ニュースB"]

    def get_latest_news(self):
        """フォールバックロジックを組み込んだメイン処理"""
        # --- 第1コース：メインサーバーを試す ---
        try:
            print("1. メインサーバーに接続中...")
            return self._fetch_from_primary()

        except ConnectionError as e:
            print(f"   [失敗] {e}")
            print("2. ➔ バックアップサーバーへフォールバックします...")
            time.sleep(0.5)  # 少し待機

            # --- 第2コース：バックアップサーバーを試す ---
            try:
                return self._fetch_from_backup()

            except ConnectionError as e:
                print(f"   [大失敗] {e}")
                print("3. ➔ 最終フォールバック（ローカルデータ）を適用します。")

                # --- 最終コース：完全なオフライン用固定データ ---
                return ["オフライン: ニュースを読み込めませんでした。再試行してください。"]


# --- 実際に動かしてみる ---
service = NewsService()
news = service.get_latest_news()

print("\n【最終結果】")
print(news)
```
