# Kubernetes学習

## 基本用語

### ノード
- ノードとはkubernetesがインストールされている物理または仮想マシンのことを指す
- ノードはワーカマシンのことでkubernetesによってコンテナが起動される場所
- 障害児のための複数のノードを用意する必要がある。ノードのグループのことをクラスターという
  - 上記により一つのノードで障害がは発生した場合にも、他のノードからアプリケーションにアクセスすることができる
  - また複数のノードを持つことで負荷分散も可能

### マスター
- マスターはkubernetesが実行されている別のノードでマスターとして設定される
- マスターはクラスター内のノードを監視しワーカーノード上のコンテナの実際のオーケストレーションを担当
- マスターサーバーにはKube APIサーバーがあり、それがマスターであることを意味する
- 反対にワーカーにはマスターと対話する役割を担うkubeletエージェントがある
  - 収集した情報はマスターのキーバリューストアへ保存

### コンポーネント
- kubernetesをインストールする際以下コンポーネントをインストールすることになる
  - API Server
  - ectd
  - kubelet
  - Container Runtime
  - Controller
  - Scheduler

#### ectd
- Kubernetesがクラスタ管理に使用する全てのデータを格納するためのキーバリューストア

#### scheduler
- 複数のノードに作業やコンテナを分散させる役割を持つ

#### Controller
- ノードやコンテナ、エンドポイントがダウンした時、気づいて対応する役割を持つ

#### kubelet
- コンテナがノード上で実行されているかを確認する役割を担っている

### kubectl
- kubernetesクラスタ上のアプリケーションをデプロイし管理するために使用される

#### `kubectl run`
- アプリケーションをクラスタ上にデプロイ

#### `kubectl cluster info`
- クラスタの情報を開示

#### `kubectl get nodes`
- クラスタに属する全てのノードをリストアップする

## ポッド
- kubernetesではワーカーノードに直接コンテナをデプロイするわけではない
- コンテナはポッドと呼ばれるkubernetesのオブジェクトにカプセル化されている
- 負荷分散の際は同じkebernetes上の2つの別々にpodでアプリケーションの2つのインスタンスが動作する
- さらに負荷分散が必要な場合はクラスタの新しいノードに追加のpodをデプロイする
- スケールアップ...ポッド追加、スケールダウン...ポッド削除

-  一つのポッドで通常同じ種類のコンテナであることを除いて複数のコンテナを持つことができる
- ポッドがどのようなコンテナで構成されているかを定義するだけでデフォルトでポッド内のコンテナは同じストレージ、ネットワーク空間にアクセスすることができ、一緒に作成され一緒に破棄できる

### `kubectl`
- `kubectl run nginx`
  - 自動的にPodを作成しNginxのDockerイメージのインスタンスをデプロイする
- `kubectl get pods`
  - クラスタ内のpodリスト確認
 
## インストール

### kubectl

```
$ brew install kubectl
$ kubectl version --client
```

### minikube

```
$ brew install minikube
$ minikube version
```

#### `minikube start`できない
- docker desctopを利用しているためrestartし
```
$ minikube delete
minikube start --driver=docker
😄  Darwin 11.3.1 (arm64) 上の minikube v1.35.0
✨  ユーザーの設定に基づいて docker ドライバーを使用します
📌  root 権限を持つ Docker Desktop ドライバーを使用
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🚜  Pulling base image v0.0.46 ...
🔥  Creating docker container (CPUs=2, Memory=4000MB) ...
🐳  Docker 27.4.1 で Kubernetes v1.32.0 を準備しています...
    ▪ 証明書と鍵を作成しています...
    ▪ コントロールプレーンを起動しています...
    ▪ RBAC のルールを設定中です...
🔗  bridge CNI (コンテナーネットワークインターフェース) を設定中です...
🔎  Kubernetes コンポーネントを検証しています...
    ▪ gcr.io/k8s-minikube/storage-provisioner:v5 イメージを使用しています
🌟  有効なアドオン: storage-provisioner, default-storageclass
🏄  終了しました！kubectl がデフォルトで「minikube」クラスターと「default」ネームスペースを使用するよう設定されました
```

### クラスタ起動

https://minikube.sigs.k8s.io/docs/start/?arch=%2Fmacos%2Farm64%2Fstable%2Fbinary+download

```
$ kubectl get nodes
NAME       STATUS   ROLES           AGE    VERSION
minikube   Ready    control-plane   3m7s   v1.32.0
```

```
$ kubectl create deployment hello-minikube --image=kicbase/echo-server:1.0
deployment.apps/hello-minikube created
```

```
$ kubectl expose deployment hello-minikube --type=NodePort --port=8080
```

```
$ minikube service hello-minikube --url
http://127.0.0.1:62934
```

クリーンアップ
```
$ service "hello-minikube" deleted
$ kubectl delete deployment hello-minikube
```

## ポッド起動

```
$ kubectl run nignx --image=nginx
$ kubectl get pods
NAME    READY   STATUS    RESTARTS   AGE
nignx   1/1     Running   0          15s

$ kubectl describe pod nignx

$ kubectl get pods -o wide
NAME    READY   STATUS    RESTARTS   AGE     IP           NODE       NOMINATED NODE   READINESS GATES
nignx   1/1     Running   0          3m42s   10.244.0.4   minikube   <none>           <none>
```

## ポッド YAML

### YAML in kubernetes

`pod-defnition.yml`
```
apiVersion: v1
kind: Pod
metaData:
  name: myapp-pod
  labls:
    app: myapp
    type: front-end
spec:
  containers:
    - name: nginx-container
      image: nginx
```

- 上記作成後`kubectl create -f pod-defnition.yml`実行でkubernetsがPodを作成する

### 利用するコマンド
- `kubectl get pods`
  - 作成されているポッド一覧を取得する
- `kubectl describe pod (ポッド名)`
  - 指定したポッドの詳細情報を表示する


### 一連の流れ

- 以下yamlファイル作成
```
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app: nginx
    type: frontend
spec:
  containers:
    - name: nginx
      image: nginx
```

- 以下実行
```
$ kubectl apply -f nginx-def.yml
pod/nginx created

$ kubectl get pods
NAME        READY   STATUS    RESTARTS   AGE
nginx       1/1     Running   0          18s
```

## レプリケーション　コントローラー

### レプリケーションコントローラーとは
- kubenetsクラスタの中で1つのpodの複数のインスタンスを動作することで高価用性を実現するのに役立つ
- ではポッドが一台の場合レプリケーションコントローラーは使えないのか
  - そんなことはなくレプリケーションコントローラーは例えポッドが1台での100台でも指定されたポッド数が常に稼働されていることを保証する
- レプリケーションコントローラーが必要な理由は複数のポッドを使って負荷分散させるためである
  - 負荷分散の際レプリケーションコントローラはクラスタ内の複数のノードにまたがっている
- またレプリケーションコントローラとレプリケーションセットがある
  - 目的は一緒だが全くの別物
 
### レプリケーションコントローラの定義

`rc-def.yml`
```
apiVersion: v1
kind: ReplicationController
metadata:
  name: myapp-rc
  labels:
    app: myapp
    type: front-end
spec:
  template:
    metadata:
      name: nginx
      labels:
        app: nginx
        type: frontend
    spec:
      containers:
        - name: nginx-container
          image: nginx
  replicas: 3
```

`kubectl create -f rc-def.yml`を実行

- レプリケーションコントローラ一覧取得

```
$ kubectl get replicationcontrollers
NAME       DESIRED   CURRENT   READY   AGE
myapp-rc   3         3         3       2m57s
```

- ポッド一覧取得

```
$ kubectl get pods
NAME             READY   STATUS    RESTARTS   AGE
myapp-pod        1/1     Running   0          82m
myapp-rc-4f26j   1/1     Running   0          4m43s
myapp-rc-5dtr2   1/1     Running   0          4m43s
nginx            1/1     Running   0          62m
```

### レプリケーションセット定義

```
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myapp-rs
  labels:
    app: myapp
    type: front-end
spec:
  template:
    metadata:
      name: myapp-pod
      labels:
        app: myapp
        type: front-end
    spec:
      containers:
        - name: nginx-container
          image: nginx
  replicas: 3
  selector:
    matchLabels:
      type: front-end
```

- 以下を実行してレプリカセット確認

```bash
$ kubectl get replicaset
NAME       DESIRED   CURRENT   READY   AGE
myapp-rs   3         3         3       105s
```


### レプリカセットのラベルとセレクターについて

- レプリカセットはパーツを監視するためのプロセス
- クラスタ内には数百のアプリケーションを実行しているパーツがある可能性
- 上記の際に便利なのが作成時にポッドにラベルをつけること

ポッド
```
metadata:
      name: myapp-pod
      labels:
        app: myapp
        type: front-end
```

レプリカセット
```
selector:
    matchLabels:
      type: front-end
```

### レプリカセットのスケーリング

- スケーリングする方法は複数ある
- 1つ目は`replicas: 3`を編集する方法
- 2つ目は`kubectl scale --reprilas=6 replicaset myapp-rs`を実行


















