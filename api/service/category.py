# coding=utf-8
import os, json
from flask import Flask, request
from controller import crud_controller
from configuration import UPLOAD_PATH, ALLOWED_EXTENSIONS, IMAGES_URL_PATH
from core_lib.codes import NO_DATA_FOUND, SYSTEM_ERROR
from core_lib.models import db, Category
from core_lib.utils import BusinessException, orm_to_json
from datetime import datetime


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_list(bag):
    result_list = crud_controller.get_list(Category, bag)
    return {'list': result_list}


def create(bag):
    data = request.form.get('data')
    data = json.loads(data)
    m_id = crud_controller.create(Category, data)
    if 'file' in request.files:
        file = request.files['file']
        filename = str(m_id) + '_category.jpg'
        if file and allowed_file(file.filename):
            file.save(os.path.join(UPLOAD_PATH, filename))
        m = db.session.query(Category).filter(Category.id == m_id).first()
        if not m:
            raise BusinessException(NO_DATA_FOUND)
        m.image = IMAGES_URL_PATH + '/' + filename
        m.date_create = datetime.now()
        db.session.flush()
    return {'id': m_id}


def update(bag):
    data = request.form.get('data')
    data = json.loads(data)
    m_id = crud_controller.update(Category, data)
    if 'file' in request.files:
        file = request.files['file']
        filename = str(m_id) + '_category.jpg'
        if file and allowed_file(file.filename):
            file.save(os.path.join(UPLOAD_PATH, filename))
        m = db.session.query(Category).filter(Category.id == m_id).first()
        if not m:
            raise BusinessException(NO_DATA_FOUND)
        m.image = IMAGES_URL_PATH + '/' + filename
        db.session.flush()
    return {'id': m_id}


def delete(bag):
    try:
        crud_controller.delete(Category, bag)
    except:
        raise BusinessException(SYSTEM_ERROR, u'Невозможно удалить категорию, запись используется в другом месте')
    return {}


def get_detail(bag):
    product = db.session.query(Category).filter(Category.id == bag['id']).first()
    if not product:
        raise BusinessException(NO_DATA_FOUND)
    return {'category': orm_to_json(product)}