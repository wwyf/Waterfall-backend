from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from src import app
import json

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
    summary = db.Column(db.Text)
    createdate = db.Column(db.Date)
    deadline = db.Column(db.Date)
    address = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    totalprice = db.Column(db.Float)
    createuser = db.Column(db.Integer)
    comments = db.Column(db.Text)
    phone = db.Column(db.Text)
    status = db.Column(db.Integer)
    progress = db.Column(db.Integer)
    def __init__(self, name, summary, createdate, deadline, address, quantity, price, totalprice, createuser, comments, phone, status, progress):
        self.name = name
        self.summary = summary
        self.createdate = createdate
        self.deadline = deadline
        self.address = address
        self.quantity = quantity
        self.price = price
        self.totalprice = price * quantity
        self.createuser = createuser
        self.comments = comments
        self.phone = phone
        self.status = status
        self.progress = progress
    def to_json(self):
        return {
            "id" : self.ID,
            "name" : self.name,
            "summary" : self.summary,
            "createdate" : self.createdate,
            "deadline" : self.deadline,
            "address" : self.address,
            "quantity" : self.quantity,
            "price" : self.price,
            "totalprice" : self.totalprice,
            "createuser" : self.createuser,
            "comments" : self.comments,
            "phone" : self.phone,
            "status" : self.status,
            "progress" : self.progress,
        }

class subOrders(db.Model):
    __tablename__ = 'subOrders'
    ID = db.Column(db.Integer, primary_key=True)
    # TODO: 需要弄成外键的形式吗
    mainorder = db.Column(db.Integer)
    createdate = db.Column(db.DateTime)
    # TODO: 需要弄成外键的形式吗
    createuser = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    # price = db.Column(db.Float)
    # totalprice = db.Column(db.Float)
    comments = db.Column(db.Text)
    phone = db.Column(db.Text)
    status = db.Column(db.Integer)
    def __init__(self, mainorder, createdate, createuser, quantity,  comments, phone, status):
        self.mainorder = mainorder
        self.createdate = createdate
        self.createuser = createuser
        self.quantity = quantity
        # self.price = price
        # self.totalprice = price * quantity
        self.comments = comments
        self.phone = phone
        self.status = 0
    def to_json(self):
        return {
            "id" : self.ID,
            "mainorder" : self.mainorder,
            "createdate" : self.createdate,
            "createuser" : self.createuser,
            "quantity" : self.quantity,
            "comments" : self.comments,
            "phone" : self.phone,
            "status" : self.status
        }

db.create_all()


