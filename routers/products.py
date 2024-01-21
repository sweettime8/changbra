import json

from flask import Blueprint, request, render_template, redirect, url_for, flash, Response, jsonify
from app import db, TblProducts, TblCategories, TblProductDetail, app
import os
import unicodedata
from werkzeug.utils import secure_filename
from datetime import datetime
from sqlalchemy import func

products = Blueprint('products', __name__, template_folder='templates')


@products.route('/products')
def product():
    result = db.session.query(TblProducts, func.sum(TblProductDetail.quantity).label('total_quantity')).join(
        TblProductDetail, TblProducts.id == TblProductDetail.p_id
    ).group_by(TblProducts.id).all()
    # Duyệt qua kết quả để in ra thông tin
    for product, total_quantity in result:
        print(f"Product ID: {product.id}, Product Name: {product.name}")
        print(f"Total Quantity: {total_quantity}")
    return render_template('product/product.html', list_products=result)


@products.route('/create-products', methods=['POST'])
def create_products():
    print("create_products")
    try:
        if request.method == 'POST':
            # Lấy dữ liệu từ form
            productName = request.form.get('productName')
            productType = request.form.get('productType')
            productWeight = int(request.form.get('productWeight'))
            entryPrice = request.form.get('entryPrice')
            wholesalePrice = request.form.get('wholesalePrice')
            retailPrice = request.form.get('retailPrice')
            productDetail = request.form.get('productDetail')

            files = request.files.getlist('files')

            if files:
                # Lưu file vào thư mục uploads
                # Tạo thư mục dựa trên tên sản phẩm không dấu
                product_folder = os.path.join(app.config['UPLOAD_FOLDER'], slugify(productName))
                if not os.path.exists(product_folder):
                    os.makedirs(product_folder)

                # Lưu các file vào thư mục sản phẩm
                image_paths = []
                for file in files:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(product_folder, filename)
                    file.save(file_path)
                    image_paths.append(file_path)
            else:
                print("No files ")

            # Bổ sung dấu ngoặc vuông để tạo mảng Chuyển dữ liệu JSON thành danh sách Python
            product_detail = json.loads(f"[{productDetail}]")

            # In ra màn hình để kiểm tra
            print("Product Name:", productName)
            print("Product Detail:", product_detail)

            # insert to database Products:
            # 1. check database is existed
            results = TblProducts.query.filter_by(name=productName).first()
            if results is None:
                new_database = TblProducts(name=productName, type=productType, weight=productWeight,
                                           entry_price=entryPrice, wholesale_price=wholesalePrice,
                                           retail_price=retailPrice)
                db.session.add(new_database)
                db.session.commit()

                # Lấy ID của Product vừa insert
                product = TblProducts.query.filter_by(name=productName).first()
                p_id = product.id

                for item in product_detail:
                    print("Product_name : " + item['p_name'])
                    print("ton ban dau : " + item['p_initial'])
                    p_detail_name, p_detail_size, p_detail_color = item['p_name'].split(" - ")
                    print("p_detail_name : " + p_detail_name)
                    print("p_detail_size : " + p_detail_size)
                    print("p_detail_color : " + p_detail_color)

                    # insert to database TblProductDetail:
                    now = datetime.now()
                    new_product = TblProductDetail(p_id=p_id, size=p_detail_size, color=p_detail_color,
                                                   quantity=item['p_initial'], entry_date=now.strftime("%Y-%m-%d"))
                    db.session.add(new_product)
                    db.session.commit()

            return jsonify(
                {'status': 'success', 'message': 'Add product successful!', 'data': "success"})



    except Exception as e:
        print("error : ", e)
        return jsonify({'status': 'error', 'message': str(e)})


@products.route('/product-detail/<string:id>', methods=['GET'])
def product_detail(id):
    print("## [product_detail] ##")
    try:
        if request.method == 'GET':
            # get infor product_detail
            product_detail = TblProductDetail.query.filter_by(p_id=id).all()

            return render_template('product/product-detail.html', product_detail=product_detail)
    except Exception as e:
        print("error : ", e)
        return jsonify({'status': 'error', 'message': str(e)})


# Hàm xử lý tên sản phẩm không dấu
def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('utf-8')
    value = secure_filename(value)
    return value


@products.route('/uploads', methods=['POST'])
def upload_files():
    return jsonify({'status': 'success', 'message': 'Upload successful.'})
