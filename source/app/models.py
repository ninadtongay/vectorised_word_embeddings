# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app         import db
from flask_login import UserMixin
import time

class User(UserMixin, db.Model):

    id                    = db.Column(db.Integer,     primary_key=True)
    company_name          = db.Column(db.String(500))
    name                  = db.Column(db.String(64),  unique = True)
    email                 = db.Column(db.String(120), unique = True)
    phone                 = db.Column(db.String(12))
    account_creation_time = db.Column(db.String(500))
    account_approval_time = db.Column(db.String(500))
    password              = db.Column(db.String(500))
    role                  = db.Column(db.String(120))

    def __init__(self, company_name, name, email, phone, password, role):
        self.company_name          = company_name
        self.name                  = name
        self.email                 = email
        self.phone                 = phone
        self.account_creation_time = 0
        self.account_approval_time = 0
        self.password              = password
        self.role                  = role

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.user)

    def save(self):

        # inject self into db session    
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )

        return self

class Item(db.Model):

    id              = db.Column(db.Integer, primary_key=True)
    item_type       = db.Column(db.String(500))
    item_name       = db.Column(db.String(120))
    item_price      = db.Column(db.String(500))
    date_added      = db.Column(db.String(120))
    date_updated    = db.Column(db.String(500))

    def __init__(self, item_type, item_cost, item_price, date_added, date_updated):
        self.item_type      = item_type
        self.item_name      = item_cost
        self.item_price     = item_price
        self.date_added     = date_added
        self.date_updated   = date_updated
    
    def to_json(self):
        return {
            "item_id": self.id,
            "item_type": self.item_type,
            "item_name": self.item_name,
            "item_price": self.item_price,
        }

    def save(self):

        # inject self into db session    
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )

        return self

class Order(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.String(500))
    item_id         = db.Column(db.String(120))
    amount          = db.Column(db.String(500))
    date_ordered    = db.Column(db.String(120))
    date_confirmed  = db.Column(db.String(500))

    def __init__(self, user_id, item_id, amount, date_ordered, date_confirmed):
        self.user_id        = user_id
        self.item_id        = item_id
        self.amount         = amount
        self.date_ordered   = date_ordered
        self.date_confirmed = date_confirmed

    # def get_cost(self):
    #     return str(self.cost)
    
    # def __repr__(self):
    #     return str(self.id) + ' - ' + str(self.function)

    def save(self):

        # inject self into db session
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )

        return self