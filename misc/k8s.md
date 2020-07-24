
# Kubernetes

setup procedure on ubuntu18.04
```
```

## Install kubectl on macOS

https://kubernetes.io/ja/docs/tasks/tools/install-kubectl/
```
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mkdir -p /usr/local/bin
sudo mv ./kubectl /usr/local/bin/kubectl

mkdir -p ~/.kube
vim ~/.kube/config
kubectl version
```

## Setup with rancher

```
```

## CLI

```
kubectl port-forward nginx-deployment-7fd6966748-bwj5t 7000:80
curl localhost:7000
```

## Manifests

```
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer
```
