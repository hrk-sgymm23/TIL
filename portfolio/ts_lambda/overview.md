# TypeScript x Lambdaで開発する

# ローカルの環境を作成する

- https://qiita.com/coatly/items/ecf889f283a6d36a9864

```bash
$ npm init
$ npm install -D @types/aws-lambda esbuild
```

## jest導入

https://qiita.com/mktu/items/d36416baba155dfecc00

```bash
$ npm install --save-dev jest @types/jest ts-jest
$ npx ts-jest config:init
```

`package.json`

```bash
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "build": "esbuild index.ts --bundle --minify --sourcemap --platform=node --target=es2020 --outfile=dist/index.js",
    "unit": "jest" // 追加
  },
```

```bash
$ npm set-script unit "jest"
$ npm run unit
```

## 環境変数を読み込ませる

```bash
$ npm install dotenv
```

# Macのnodenvのバージョンを切り替える

