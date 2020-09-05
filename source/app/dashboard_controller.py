import numpy as np
import pandas as pd
import sqlite3
import ast
import json
import math
from app.models import User, Item
from app import db
from flask_login import current_user


def get_all_items():
    return Item.query.all()

def delete_item(item_id):
    item = Item.query.filter(Item.id == item_id).delete()
    db.session.commit()
    return get_all_items()

def add_new_item(item_type, item_name, item_price):
    added = False
    try:
        date_added = 0
        date_updated = 0
        item = Item(item_type, item_name, item_price, date_added, date_updated)
        item.save()
    except:
        print("An exception occurred")
    
    return get_all_items()
