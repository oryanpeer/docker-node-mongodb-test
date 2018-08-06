# Deploy Bigpanda containerized application,node application, only if healthcheck success
Deploy docker container with python3.4 only if the application pass healthcheck
## Description
This project is using Docker and Docker compose, download and extract tar.gz archive, link node application to MongoDB using docker compose.

Explanation of each tool can be found on the links below:
* Docker (https://docs.docker.com/)
* Docker-Compose (https://docs.docker.com/compose/)
* Node in Docker (https://nodejs.org/en/docs/guides/nodejs-docker-webapp/)

## Requirements
* [Git](http://git-scm.com)
* [Docker](https://docs.docker.com/install/)
* [Docker-Compose](http://www.vagrantup.com) - The binary file needs to be locates at /usr/local/bin/docker-compose
* [python3.4](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/installing/)

## Optional Requirements
* [virtualenv](https://docs.python-guide.org/dev/virtualenvs/)

## Install clone the repository and install pip packages

```
git clone https://github.com/oryanfarjon/docker-node-mongodb-test.git
cd docker-node-mongodb-test
pip install -r requirements.txt
```

After installing requirements and pip you will be able to deploy the application using the command below:
```
python deployment.py
```
You can follow the script output to follow the deployment proccess

After successful deployment, the node app will be available on port 3000 on the server.
* nodeapp: http://localhost:3000
* healthcheck: http://localhost:3000/health

If everything is working properly you will be able to browse the node application URL and see Panda's images.
