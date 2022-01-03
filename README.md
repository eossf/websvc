# websvc
Python FastAPI webapi for testing

## Get repository for rw
````
ssh-agent bash -c 'ssh-add ~/.ssh/id_rsa; git clone git@github.com:eossf/websvc.git'
git config --global user.email "my@email.com"
````

## run locally in VSCode
conda env create
conda activate WEBSVC 
uvicorn main:app

## build docker
docker build . -t websvc:0.0.1

## Helm

### Helm install : websvc package
````
helm install -f myvalue.yaml websvc ./websvc 
helm install websvc ./websvc 
````