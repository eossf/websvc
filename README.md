# FastAPI websvc
Python FastAPI webapi for testing
You need curl, docker, docker-compose, helm, and python/pip + conda for local dev

## -- Get repository for read-write access
````
ssh-agent bash -c 'ssh-add ~/.ssh/id_rsa; git clone git@github.com:eossf/websvc.git'
git config --global user.email "stephane.metairie@gmail.com"
````

## -- Run locally in VSCode
````
conda env create
conda activate WEBSVC 
uvicorn main:app
````

## -- Build Image
````
docker build . -t websvc:0.0.1
docker-compose build --force-rm --progress plain
````

## -- Helm deploy package

### create a namespace, add context
````
kubectl create namespace websvc
````

### install websvc package
````
cd ~/websvc
helm install -f myvalue.yaml websvc ./websvc 
helm install websvc ./websvc 
````
