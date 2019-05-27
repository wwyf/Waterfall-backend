#!/bin/bash
source venv/bin/activate
export FLASK_APP=src
export FLASK_ENV=development # turn on debug mode and other dev features
flask run