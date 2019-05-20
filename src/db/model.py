from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from run import app
import json

with open('db/sql_config.json', encoding='utf-8') as sqlConfFile:
    sqlConf = json.loads(sqlConfFile.read())
    sqlConnector = "mysql+pymysql://{}:{}@{}/{}".format(sqlConf['username'], sqlConf['password'], sqlConf['host'], sqlConf['database'])
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlConnector

app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Users(db.Model):
    __tablename__ = 'Users'
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text)
    phone = db.Column(db.Text)
    balance = db.Column(db.Float, default=0)
    usertype = db.Column(db.Integer)
    userstatus = db.Column(db.Integer)
    def __init__(self, username, password, email, phone, usertype):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.usertype = usertype
        self.balance = 0.0
        self.userstatus = 0

class Orders(db.Model):
    __tablename__ = 'Orders'
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    createdate = db.Column(db.Date)
    deadline = db.Column(db.Date)
    address = db.Column(db.Text)
    amount = db.Column(db.Integer)
    price = db.Column(db.Float)
    totalprice = db.Column(db.Float)
    createuser = db.Column(db.Integer)
    comments = db.Column(db.Text)
    contect = db.Column(db.Text)
    status = db.Column(db.Integer)
    progress = db.Column(db.Integer)
    def __init__(self, name, createdate, deadline, address, amount, price, createuser, comments, contect):
        self.name = name
        self.createdate = createdate
        self.deadline = deadline
        self.address = address
        self.amount = amount
        self.price = price
        self.totalprice = price * amount
        self.createuser = createuser
        self.comments = comments
        self.contect = contect
        self.status = 0
        self.progress = 0

class subOrders(db.Model):
    __tablename__ = 'subOrders'
    ID = db.Column(db.Integer, primary_key=True)
    createdate = db.Column(db.Date)
    mainorder = db.Column(db.Integer)
    supplier = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    price = db.Column(db.Float)
    totalprice = db.Column(db.Float)
    comments = db.Column(db.Text)
    contect = db.Column(db.Text)
    status = db.Column(db.Integer)
    def __init__(self, createdate, mainorder, supplier, amount, price, totalprice, comments, contect, status):
        self.createdate = createdate
        self.mainorder = mainorder
        self.supplier = supplier
        self.amount = amount
        self.price = price
        self.totalprice = price * amount
        self.comments = comments
        self.contect = contect
        self.status = 0

db.create_all()


