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
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    type = db.Column(db.String(500))
    weight = db.Column(db.Integer)
    entry_price = db.Column(db.Integer)
    wholesale_price = db.Column(db.Integer)
    retail_price = db.Column(db.Integer)
    image = db.Column(db.String(500))
    description = db.Column(db.String(500))


class TblProductImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    p_id = db.Column(db.Integer)
    image_src = db.Column(db.String(500))


class TblProductDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer)
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    image = db.Column(db.String(500))
    entry_date = db.Column(db.String(50))


class TblOrders(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy - mã đơn hàng
    customer_name = db.Column(db.String(500))
    phone = db.Column(db.String(50))
    status = db.Column(db.String(50))
    total_amount = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.String(50))

class TblOrderItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    order_id = db.Column(db.Integer)


class Province(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    code = db.Column(db.Integer)
    codename = db.Column(db.String(255))
    division_type = db.Column(db.String(255))
    phone_code = db.Column(db.Integer)

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    code = db.Column(db.Integer)
    codename = db.Column(db.String(255))
    division_type = db.Column(db.String(255))
    short_codename = db.Column(db.String(255))
    province_id = db.Column(db.Integer, db.ForeignKey('province.id'))
    province = db.relationship('Province', backref='districts')

class Ward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    code = db.Column(db.Integer)
    codename = db.Column(db.String(255))
    division_type = db.Column(db.String(255))
    short_codename = db.Column(db.String(255))
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    district = db.relationship('District', backref='wards')
