# TyoeScriptの練習問題

[【初学者向け】具体例で学ぶTypeScript練習問題集](https://zenn.dev/kagan/articles/typescript-practice)



## Lv.1】引数の型注釈 2（配列） 
```ts
const double = (array: number[]) => {
  console.log(array.map((num) => num * 2));
  return array.map((num) => num * 2);
};
```

## 【Lv.1】引数の型注釈 3（オブジェクト）
```ts
const message = (user: {name: string, age: number}) => {
  console.log(
    `${user.name}さん、${user.age}歳です。来年は${user.age + 1}歳ですね。`
  );
};
```

