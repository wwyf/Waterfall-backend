# Waterfall-backend

![](https://travis-ci.org/wwyf/Waterfall-backend.svg?branch=master)

## Install

### Prerequisite

- python : 3.6
- pip

### Install

Create a python virtual environment, and
(just an example)

```
git clone git@github.com:wwyf/Waterfall-backend.git
cd Waterfall-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Deploy

Finally you can run Waterfall-backend.

```
export FLASK_APP=src
export FLASK_ENV=development # turn on debug mode and other dev features
flask run
```

Backend will run on http://localhost:5000.

Or maybe you can just run with the sample shell script `./run.sh` after you configure with virtual environment.

```shell
./run.sh
```

## Docker

### Build and Run


```
git clone git@github.com:wwyf/Waterfall-backend.git
cd Waterfall-backend
```

To build the project into docker image, it's as simple as

```
docker build -t waterfall-backend .
docker run  -d waterfall-backend
```

Also you can get it from [DockerHub](https://cloud.docker.com/u/wwyf/repository/docker/wwyf/waterfall-backend)