from flask import Blueprint, request, render_template, redirect, url_for, flash, Response, jsonify
from app import db

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/')
def index():
    return render_template('index.html')
