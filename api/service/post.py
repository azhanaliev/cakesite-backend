# coding=utf-8
import os, json
from flask import Flask, request
from controller import crud_controller
from configuration import UPLOAD_PATH, ALLOWED_EXTENSIONS, IMAGES_URL_PATH
from core_lib.codes import NO_DATA_FOUND, SYSTEM_ERROR
from core_lib.models import db, Post, PostCategory
from core_lib.utils import BusinessException, orm_to_json
from datetime import datetime


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_list(bag):
    query = db.session.query(Post)
    query = query.join(PostCategory)
    if bag.get('code'):
        query = query.filter(PostCategory.code.in_(bag['code']))
    query = query.order_by(Post.id).all()
    result_list = []
    for p in query:
        p_json = orm_to_json(p)
        result_list.append(p_json)
    return {'list': result_list}


def create(bag):
    data = request.form.get('data')
    data = json.loads(data)
    m_id = crud_controller.create(Post, data)
    if 'file' in request.files:
        file = request.files['file']
        filename = str(m_id) + '_post.jpg'
        if file and allowed_file(file.filename):
            file.save(os.path.join(UPLOAD_PATH, filename))
        m = db.session.query(Post).filter(Post.id == m_id).first()
        if not m:
            raise BusinessException(NO_DATA_FOUND)
        m.image = IMAGES_URL_PATH + '/' + filename
        m.date_create = datetime.now()
        db.session.flush()
    return {'id': m_id}


def update(bag):
    data = request.form.get('data')
    data = json.loads(data)
    m_id = crud_controller.update(Post, data)
    if 'file' in request.files:
        file = request.files['file']
        filename = str(m_id) + '_product.jpg'
        if file and allowed_file(file.filename):
            file.save(os.path.join(UPLOAD_PATH, filename))
        m = db.session.query(Post).filter(Post.id == m_id).first()
        if not m:
            raise BusinessException(NO_DATA_FOUND)
        m.image = IMAGES_URL_PATH + '/' + filename
        db.session.flush()
    return {'id': m_id}


def delete(bag):
    try:
        crud_controller.delete(Post, bag)
    except:
        raise BusinessException(SYSTEM_ERROR, u'Невозможно удалить новость, запись используется в другом месте')
    return {}


def get_detail(bag):
    product = db.session.query(Post).filter(Post.id == bag['id']).first()
    if not product:
        raise BusinessException(NO_DATA_FOUND)
    return {'post': orm_to_json(product)}


def get_categories(bag):
    result_list = crud_controller.get_list(PostCategory, bag)
    return {'list': result_list}