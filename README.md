# Waterfall-backend

![](https://travis-ci.org/wwyf/Waterfall-backend.svg?branch=master)

## Envinment

`python=3.6`

## Start in debug mode

```
git clone git@github.com:wwyf/Waterfall-backend.git
cd Waterfall-backend
```

Then you should setup the envirnment by instrucments below.
```
# create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Finally you can run Waterfall-backend in debug mode.
```
export FLASK_APP=src
export FLASK_ENV=development # turn on debug mode and other dev features
flask run
```

Backend will run on http://localhost:5000.