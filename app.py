from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, sys

# Application initializations
app = Flask(__name__)

isExist = os.path.exists("database")
if not isExist:
    os.makedirs("database")
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir + "\database", 'changbra.db')

print("mrd db_path : " + db_path)

app.config["SECRET_KEY"] = 'nghduc91'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///{}'.format(db_path)

db = SQLAlchemy(app)


class TblCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    name = db.Column(db.String(500))
    image = db.Column(db.String(500))


class TblProducts(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    cate_id = db.Column(db.Integer)
    name = db.Column(db.String(500))
    entry_price = db.Column(db.Integer)
    wholesale_price = db.Column(db.Integer)
    retail_price= db.Column(db.Integer)
    description = db.Column(db.String(500))

class TblProductDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer)
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    entry_date = db.Column(db.String(50))


# class TblProductColor(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(500))
#
#
# class TblProductSize(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     size = db.Column(db.String(50))