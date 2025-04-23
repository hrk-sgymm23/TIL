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



















