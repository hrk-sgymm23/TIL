# SeverSideRenderingについて

## `getServerSideProps`
- `getServerSideProps`リクエスト時にデータを取得する必要があるページをプレレンダリングする場合のみに使用
- 最初のバイトまでの時間はサーバーがリクエストごとに結果を返す必要があり、追加の構成を行わないとCDNで結果をキャッシュできないため、通常よりも遅くなる
```javascript
export async function getServerSideProps(context) {
  return {
    props: {
      // props for your component
    },
  };
}
```

## SWR
- クライアント側でデータを取得する再利用を推奨される
- キャッシュ、再検証、フォーカス追跡、一定間隔での再フェッチなどを処理する
- クライアント側でえんだリングが必要なケース...SEOとは関係ないユーザー固有のページの場合
  
```javascript
import useSWR from 'swr';

function Profile() {
  const { data, error } = useSWR('/api/user', fetch);

  if (error) return <div>failed to load</div>;
  if (!data) return <div>loading...</div>;
  return <div>hello {data.name}!</div>;
}
```

## 参考
https://nextjs.org/learn-pages-router/basics/data-fetching/request-time
