# Docker周り用意

```bash
$ $ docker-compose run --rm app yarn create next-app . --ts
```

`src/setup.sh`
```sh
set -eu

yarn && yarn dev
```
