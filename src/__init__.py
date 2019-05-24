import os
from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY='dev',
    # store the database in the instance folder
    # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

with open('src/db/sql_config.json', encoding='utf-8') as sqlConfFile:
    sqlConf = json.loads(sqlConfFile.read())
    sqlConnector = "mysql+pymysql://{}:{}@{}/{}".format(sqlConf['username'], sqlConf['password'], sqlConf['host'], sqlConf['database'])
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlConnector

app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


# # ensure the instance folder exists
# try:
#     os.makedirs(app.instance_path)
# except OSError:
#     pass

# apply the blueprints to the app
from src import bp
app.register_blueprint(bp.order_bp)
app.register_blueprint(bp.wallet_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)