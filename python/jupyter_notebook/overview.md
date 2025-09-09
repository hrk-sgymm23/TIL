# Jupyter NoteBookについて

参考: https://zenn.dev/haruki1009/articles/045a07794899c2


## 導入

`requirements.txt`
```
jupyter
```

```
$ pip install -r requirements.txt
$ jupyter notebook --version
```

## 起動

```
$ jupyter notebook
```

`docker-compose`に以下追加
```
ports:
    - "8888:8888"
```

## 新規のノートブックを作成


### 簡単な実行

NotebookのPython3を押してコードをセルへ入力

```
print("Hello, Jupyter!")
```

上記入力し、shfit + Enterで実行


### グラフを作成

```
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

plt.plot(x, y)
plt.title("Simple Plot")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
```

### マークダウンセルでのドキュメントの記述

- 新しいセルからmdファイルを選択し記載

基本的な構文
```
# 見出し1
## 見出し2
### 見出し3

- 箇条書き1
- 箇条書き2

[リンクテキスト](http://example.com)

![画像の説明](path/to/image.png)
```


# JupyterNoteBookのtips

https://qiita.com/simonritchie/items/d7dccb798f0b9c8b1ec5

## 入力補完

### `jupyter_contrib_nbextensions`を使う

- venvを使う
```
$ python3 -m venv ~/venvs/nbx
$ source ~/venvs/nbx/bin/activate
$ pip install "notebook<7,>=6.4" \\n            "jupyter_contrib_nbextensions==0.7.0" \\n            "jupyter_nbextensions_configurator==0.6.3" \\n            ipykernel
$ jupyter contrib nbextension install --user
$ jupyter nbextensions_configurator enable --user
$ jupyter notebook
```

- Hinterlandにチェックを入れると補完が効くようになる

## 目次を自動で入れる
- Table of Contents (2)にチェックを入れる
- するとメニュー欄にハンバーガーメニューが現れる
- 



