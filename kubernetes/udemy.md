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

## デプロイメント

### デプロイの定義に関して

`kind`を`Deployment`へ変更する
```yaml
kind: Deployment
```

### コマンド

```bahs
kubctl get all
```

### 実装

`deployment.yml`
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  labels:
    tier: frontend
    app: nginx
spec:
  selector:
    matchLabels:
      app: myapp
  replicas: 3
  template:
    metadata:
      name: nginx-2
      labels:
        app: myapp
    spec:
      containers:
        - name: nginx
          image: nginx
```

`kubectl create -f deployment.yml`を実行しデプロイメント作成

- デプロイメント一覧取得
```
$ kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
myapp-deployment   3/3     3            3           21s
```

- 指定したデプロイメントの詳細情報を確認
```
$ kubectl describe deployment myapp-deployment
Name:                   myapp-deployment
Namespace:              default
CreationTimestamp:      Sun, 27 Apr 2025 19:11:04 +0900
Labels:                 app=nginx
                        tier=frontend
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=myapp
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=myapp
  Containers:
   nginx:
    Image:        nginx
    Port:         <none>
    Host Port:    <none>
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   myapp-deployment-5655d5f56f (3/3 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  5m1s   deployment-controller  Scaled up replica set myapp-deployment-5655d5f56f from 0 to 1
  Normal  ScalingReplicaSet  4m57s  deployment-controller  Scaled down replica set myapp-rs from 3 to 2
  Normal  ScalingReplicaSet  4m57s  deployment-controller  Scaled up replica set myapp-deployment-5655d5f56f from 1 to 2
  Normal  ScalingReplicaSet  4m54s  deployment-controller  Scaled down replica set myapp-rs from 2 to 1
  Normal  ScalingReplicaSet  4m54s  deployment-controller  Scaled up replica set myapp-deployment-5655d5f56f from 2 to 3
  Normal  ScalingReplicaSet  4m51s  deployment-controller  Scaled down replica set myapp-rs from 1 to 0
```

- `kubectl get all`でポッド、コントローラーなどの情報一覧取得

### ロールアウトとバージョニング

- revision1、revison2のようにデプロイバージョンごとにバージョンをつける

#### コマンド
- ロールアウトのステータスを確認
```
$ kubectl rollout status deployment.apps/myapp-deployment
deployment "myapp-deployment" successfully rolled out
```

- デプロイ直後のステータス
```
kubectl rollout status deployment.apps/myapp-deployment
Waiting for deployment "myapp-deployment" rollout to finish: 0 of 6 updated replicas are available...
Waiting for deployment "myapp-deployment" rollout to finish: 1 of 6 updated replicas are available...
Waiting for deployment "myapp-deployment" rollout to finish: 2 of 6 updated replicas are available...
Waiting for deployment "myapp-deployment" rollout to finish: 3 of 6 updated replicas are available...
Waiting for deployment "myapp-deployment" rollout to finish: 4 of 6 updated replicas are available...
Waiting for deployment "myapp-deployment" rollout to finish: 5 of 6 updated replicas are available...
deployment "myapp-deployment" successfully rolled out
```

- ロールアウトの履歴を確認
  - 以下は--recordをつけてクリエイトした場合
```
kubectl rollout history deployment.apps/myapp-deployment
deployment.apps/myapp-deployment
REVISION  CHANGE-CAUSE
1         kubectl create --filename=deployment.yml --record=true
```

#### デプロイメントストラテジー
- Recreate
  - 1つ目の方法は全てのインスタンスを全て削除し、一気に新しいインスタンスをデプロイすること
    - この方法はデフォルトではない
- RollingUpdate
  - 2つ目の方法は一気に全てのインスタンスは削除しない方法
    - 一つのインスタンスずつ古いバージョンから新しいバージョンへ切り替えていく
    - デフォルト

 #### デプロイメントの更新方法
 - `kubectl apply -f 定義ファイル名`
または
```
$ kubectl set image deployment/myapp-deployment \
  nignx-container=nignx:1.9.1
```
setの場合だと定義ファイルとデプロイされたものが異なることに注意

- `kubectl rollout undo deployment/myapp`

### 流れ

- editでnginxのバージョン変更
```
$ kubectl edit deployment myapp-deployment --record
Flag --record has been deprecated, --record will be removed in the future
deployment.apps/myapp-deployment edited
```

- statusでローリングアップデートの流れを確認
```
$ kubectl rollout status deployment.apps/myapp-deployment
Waiting for deployment "myapp-deployment" rollout to finish: 3 out of 6 new replicas have been updated...
Waiting for deployment "myapp-deployment" rollout to finish: 3 out of 6 new replicas have been updated...
Waiting for deployment "myapp-deployment" rollout to finish: 3 out of 6 new replicas have been updated...
Waiting for deployment "myapp-deployment" rollout to finish: 4 out of 6 new replicas have been updated...
Waiting for deployment "myapp-deployment" rollout to finish: 4 out of 6 new replicas have been updated...
Waiting for deployment "myapp-deployment" rollout to finish: 4 out of 6 new replicas have been updated...
Waiting for deployment "myapp-deployment" rollout to finish: 4 out of 6 new replicas have been updated...
Waiting for deployment "myapp-deployment" rollout to finish: 4 out of 6 new replicas have been updated...
Waiting for deployment "myapp-deployment" rollout to finish: 5 out of 6 new replicas have been updated...
Waiting for deployment "myapp-deployment" rollout to finish: 5 out of 6 new replicas have been updated...
Waiting for deployment "myapp-deployment" rollout to finish: 5 out of 6 new replicas have been updated...
Waiting for deployment "myapp-deployment" rollout to finish: 5 out of 6 new replicas have been updated...
Waiting for deployment "myapp-deployment" rollout to finish: 2 old replicas are pending termination...
Waiting for deployment "myapp-deployment" rollout to finish: 2 old replicas are pending termination...
Waiting for deployment "myapp-deployment" rollout to finish: 2 old replicas are pending termination...
Waiting for deployment "myapp-deployment" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "myapp-deployment" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "myapp-deployment" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "myapp-deployment" rollout to finish: 5 of 6 updated replicas are available...
deployment "myapp-deployment" successfully rolled out
```
上記の方法以外でもset imageでも変更可能

- 改めてデプロイ履歴確認
```
$ kubectl rollout history deployment.apps/myapp-deployment
deployment.apps/myapp-deployment
REVISION  CHANGE-CAUSE
1         kubectl create --filename=deployment.yml --record=true
2         kubectl edit deployment myapp-deployment --record=true
```

- ロールバック
```
$ kubectl rollout undo deployment/myapp-deployment
deployment.apps/myapp-deployment rolled back
```














