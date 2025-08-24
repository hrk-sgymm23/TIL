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