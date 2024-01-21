import json

from flask import Blueprint, request, render_template, redirect, url_for, flash, Response, jsonify
from app import db, TblProducts, TblCategories, TblProductDetail, Province, District, Ward, app

order_router = Blueprint('order_router', __name__, template_folder='templates')


@order_router.route('/orders')
def orders():
    json_data = load_json_from_file()
    save_province_data(json_data)
    return render_template('order/order.html')


def load_json_from_file():
    file_path = './database/local.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return json_data

def save_province_data(json_data):
    for province_data in json_data:
        province = Province(
            name=province_data['name'],
            code=province_data['code'],
            codename=province_data['codename'],
            division_type=province_data['division_type'],
            phone_code=province_data['phone_code']
        )
        db.session.add(province)
        db.session.commit()

        for district_data in province_data.get('districts', []):
            district = District(
                name=district_data['name'],
                code=district_data['code'],
                codename=district_data['codename'],
                division_type=district_data['division_type'],
                short_codename=district_data['short_codename'],
                province=province
            )
            db.session.add(district)
            db.session.commit()

            for ward_data in district_data.get('wards', []):
                ward = Ward(
                    name=ward_data['name'],
                    code=ward_data['code'],
                    codename=ward_data['codename'],
                    division_type=ward_data['division_type'],
                    short_codename=ward_data['short_codename'],
                    district=district
                )
                db.session.add(ward)
                db.session.commit()

