# coding=utf-8
import os, json
from flask import Flask, request
from controller import crud_controller
from configuration import UPLOAD_PATH, ALLOWED_EXTENSIONS, IMAGES_URL_PATH
from core_lib.codes import NO_DATA_FOUND, SYSTEM_ERROR
from core_lib.models import db, Product
from core_lib.utils import BusinessException, orm_to_json
from datetime import datetime


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_list(bag):
    query = db.session.query(Product)
    if bag.get('id'):
        query = query.filter(Product.category_id == bag['id'])
    query = query.order_by(Product.id).all()
    result_list = []
    for p in query:
        p_json = orm_to_json(p)
        result_list.append(p_json)
    return {'list': result_list}


def create(bag):
    data = request.form.get('data')
    data = json.loads(data)
    if not data.get('category_id'):
        raise BusinessException(NO_DATA_FOUND, 'Укажите вид категории!')
    m_id = crud_controller.create(Product, data)
    if 'file' in request.files:
        file = request.files['file']
        filename = str(m_id) + '_product.jpg'
        if file and allowed_file(file.filename):
            file.save(os.path.join(UPLOAD_PATH, filename))
        m = db.session.query(Product).filter(Product.id == m_id).first()
        if not m:
            raise BusinessException(NO_DATA_FOUND)
        m.image = IMAGES_URL_PATH + '/' + filename
        m.date_create = datetime.now()
        db.session.flush()
    return {'id': m_id}


def update(bag):
    data = request.form.get('data')
    data = json.loads(data)
    m_id = crud_controller.update(Product, data)
    if 'file' in request.files:
        file = request.files['file']
        filename = str(m_id) + '_product.jpg'
        if file and allowed_file(file.filename):
            file.save(os.path.join(UPLOAD_PATH, filename))
        m = db.session.query(Product).filter(Product.id == m_id).first()
        if not m:
            raise BusinessException(NO_DATA_FOUND)
        m.image = IMAGES_URL_PATH + '/' + filename
        db.session.flush()
    return {'id': m_id}


def delete(bag):
    try:
        crud_controller.delete(Product, bag)
    except:
        raise BusinessException(SYSTEM_ERROR, u'Невозможно удалить продукт, запись используется в другом месте')
    return {}


def get_detail(bag):
    product = db.session.query(Product).filter(Product.id == bag['id']).first()
    if not product:
        raise BusinessException(NO_DATA_FOUND)
    return {'product': orm_to_json(product)}
