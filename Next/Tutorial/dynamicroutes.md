# 動的ルートの詳細

## 外部APIまたはクエリデータベースを取得する
- `getStaticProps`,`getStaticPaths`は任意のデータソースからデータをフェッチできる
- `getAllPostsIds`は(getStaticPathsが使用される)は外部APIエンドポイントからフェッチできる
```javascript
export async function getAllPostIds() {
  // Instead of the file system,
  // fetch post data from an external API endpoint
  const res = await fetch('..');
  const posts = await res.json();
  return posts.map((post) => {
    return {
      params: {
        id: post.id,
      },
    };
  });
}
```

## 開発と本番
- 開発の場合
  - リクエストごとに`getStaticPaths`が実行される
- 本番の場合
  - ビルド時に`getStaticPaths`が実行される
 
## fallbackについて
- `true`の時、server errorが返される
- `false`の時、404エラーになる

## catch allnroutes
- `...`動的ルートは括弧内に3つのドットを追加することで全てのパスをキャッチすることができる
- `pages/posts/[...id].js`に一致する。｀posts/a`,`postst/a/b/c`にも一致する
- 以上のことを行うために以下のように`getStaticPaths`の値として配列を返す必要がある
```javascript
return [
  {
    params: {
      // Statically Generates /posts/a/b/c
      id: ['a', 'b', 'c'],
    },
  },
  //...
];
```

```javascript
export async function getStaticProps({ params }) {
  // params.id will be like ['a', 'b', 'c']
}
```
