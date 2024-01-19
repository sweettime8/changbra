from flask import Blueprint, request, render_template, redirect, url_for, flash, Response, jsonify
from app import db

warehouse = Blueprint('warehouse', __name__, template_folder='templates')

@warehouse.route('/warehouse')
def product():
    return render_template('warehouse.html')