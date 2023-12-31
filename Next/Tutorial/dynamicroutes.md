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
