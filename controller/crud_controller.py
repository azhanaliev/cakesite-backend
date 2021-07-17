from core_lib.codes import NO_DATA_FOUND
from core_lib.models import db
from core_lib.utils import json_to_orm, BusinessException, orm_to_json


def create(model, bag):
    m = model()
    json_to_orm(bag, m)
    db.session.add(m)
    db.session.flush()
    return m.id


def update(model, bag):
    m = db.session.query(model).filter(model.id == bag['id']).first()
    if not m:
        raise BusinessException(NO_DATA_FOUND)
    json_to_orm(bag, m)
    return m.id


def delete(model, bag):
    m = db.session.query(model).filter(model.id == bag['id']).first()
    if not m:
        raise BusinessException(NO_DATA_FOUND)
    db.session.delete(m)


def get_list(model, bag):
    result_list = []
    query = db.session.query(model).order_by(model.id).all()
    for m in query:
        result_list.append(orm_to_json(m))
    return result_list
