# websvc
Python FastAPI webapi for testing

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