import json

from flask import Blueprint, request, render_template, redirect, url_for, flash, Response, jsonify
from app import db, TblProducts, TblCategories, TblProductDetail

products = Blueprint('products', __name__, template_folder='templates')


@products.route('/products')
def product():
    return render_template('product/product.html')


@products.route('/create-products', methods=['POST'])
def create_products():
    print("create_products")
    try:
        if request.method == 'POST':
            # Lấy dữ liệu từ form
            productName = request.form.get('productName')
            entryPrice = request.form.get('entryPrice')
            wholesalePrice = request.form.get('wholesalePrice')
            retailPrice = request.form.get('retailPrice')
            productDetail = request.form.get('productDetail')

            # Bổ sung dấu ngoặc vuông để tạo mảng Chuyển dữ liệu JSON thành danh sách Python
            product_detail = json.loads(f"[{productDetail}]")

            # In ra màn hình để kiểm tra
            print("Product Name:", productName)
            print("Product Detail:", product_detail)

            # insert to database Products:
            # 1. check database is existed
            # results = TblProducts.query.filter_by(name=productName, entry_price=entryPrice, wholesale_price=wholesalePrice, retail_price=retailPrice,).first()
            results = TblProducts.query.filter_by(name=productName).first()
            if results is None:
                new_database = TblProducts(name=productName, entry_price=entryPrice, wholesale_price=wholesalePrice,
                                           retail_price=retailPrice)
                db.session.add(new_database)
                db.session.commit()

                # Lấy ID của Product vừa insert
                product = TblProducts.query.filter_by(name=productName).first()
                p_id = product.id

                for item in product_detail:
                    print("phien ban : " + item['p_name'])
                    name
                    print("ton ban dau : " + item['p_initial'])
                    # insert to database TblProductDetail:
                    new_product = TblProductDetail(p_id=p_id, size=size, color=color,
                                               retail_price=retailPrice)



            return jsonify(
                {'status': 'success', 'message': 'Add product successful!', 'data': "success"})



    except Exception as e:
        print("error : ", e)
        return jsonify({'status': 'error', 'message': str(e)})
