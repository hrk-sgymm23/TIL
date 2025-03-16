# discord操作に必要な環境を揃える

https://qiita.com/0xkei10/items/ac906d50a922dbbfbcea

```bash
$ npm install discord.js dotenv
```

# discord.jsについて調べる

- https://discordjs.guide/creating-your-bot/slash-commands.html#before-you-continue
- https://zenn.dev/sapphire/scraps/0aa3948dcde6a7

# noenv anyenvに関して

- ルートの`.node-version`を削除

- https://qiita.com/turara/items/6b7f4a8e3770a7074072
- https://zenn.dev/donchan922/articles/b08a66cf3cbbc5

# botの実装

https://qiita.com/spore0814/items/f2597be62431c0888fcc

上記を参考に

# 実装例

```ts
import { Client, Events, GatewayIntentBits, BaseGuildTextChannel } from 'discord.js';
import * as config from '../config.json';

const client: Client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.once(Events.ClientReady, async (c) => {
    console.log(`Ready! Logged in as ${c.user.tag}`);

    // クライアントが完全に準備できた後にチャンネルを取得
    const channel = await client.channels.fetch('1350506981621764186');

    // チャンネルがテキストチャンネルならメッセージを送信
    if (channel && channel.isTextBased()) {
        (channel as BaseGuildTextChannel).send('Hello!');
    } else {
        console.error('チャンネルが見つからないか、テキストチャンネルではありません。');
    }
});

client.login(config.token);

```
