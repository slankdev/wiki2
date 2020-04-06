
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
