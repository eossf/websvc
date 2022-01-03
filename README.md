# websvc
Python FastAPI webapi for testing

## run locally in VSCode
conda env create
conda activate WEBSVC 
uvicorn main:app

## build docker
docker build . -t websvc:0.0.1

## Helm

### Install Helm
````
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 775 get_helm.sh
./get_helm.sh
````

### Reminder : Create a package
````
helm create <NAME>
````

### Helm websvc package

