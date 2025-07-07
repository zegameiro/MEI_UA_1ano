```shell

export KUBECONFIG=./kubeconfig 

sudo -s

export KUBECONFIG=/vagrant/kubeconfig
kubctl get nodes
unset KUBECONFIG

kubectl create namespace a108840
kubectl get namespace
kubectl delete namespace a108840
```