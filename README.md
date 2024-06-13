# Simple MNIST bayesian classifier 🥷  

- This repo contains a frontend web client and a backend python service for an MNIST classifier
- Please refer to README.md files in respective folders 
  
## Quick start
### Dependencies
- Docker Desktop 🐋 
### Step-by-step
1. Download `train.csv` and `test.csv` files from https://www.kaggle.com/code/ngbolin/mnist-dataset-digit-recognizer/input
2. Place both files in `service/data`
3. From project root run `run_linux.sh` or `run_windows.bat` depending on your OS

- Verify service is running at http://localhost:4000
- Verify client is running at http://localhost:4001

### Troubleshoot
- Verrify containers are running with 'docker ps -a' (`bayes-classifier-api`, `bayes-classifier-db`, `bayes-classifier-migration` and `bayes-classifier-client`)
- Verify data has been successfully migrated (you can use a client like MongoDB Compass):
  - Connection string: `mongodb://localhost:27017/`
  - Db: `bayes_classifier`
  - Collection: `MNIST_train`