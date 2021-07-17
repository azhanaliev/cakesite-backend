from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer, String, DateTime, Column, Boolean, Float, Date, Time
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 't_user'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    name = Column(String(64), default='')
    surname = Column(String(32))
    patronymic = Column(String(32))
    phone = Column(String(64))
    email = Column(String(64))
    blocked = Column(Boolean, default=False)
    date_register = Column(DateTime)


class UserRoles(db.Model):
    __tablename__ = 't_user_roles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    role = Column(String(128))


class Device(db.Model):
    __tablename__ = 't_device'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    device_id = Column(String(128))
    device_name = Column(String(128))
    language = Column(String(2))
    token = Column(String(128))
    date = Column(DateTime)
    user = relationship(User)


class Category(db.Model):
    __tablename__ = 't_category'

    id = Column(Integer, primary_key=True)
    date_create = Column(DateTime)
    name = Column(String(64))
    code = Column(String(32))
    info = Column(String(256))
    image = Column(String(128))


class Product(db.Model):
    __tablename__ = 't_product'

    id = Column(Integer, primary_key=True)
    date_create = Column(DateTime)
    name = Column(String(64))
    info = Column(String(256))
    price = Column(Float)
    image = Column(String(128))
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    category = relationship('Category', lazy='joined')

class PostCategory(db.Model):
    __tablename__ = 't_post_category'

    id = Column(Integer, primary_key=True)
    date_create = Column(DateTime)
    name = Column(String(64))
    code = Column(String(32))
    info = Column(String(256))


class Post(db.Model):
    __tablename__ = 't_post'

    id = Column(Integer, primary_key=True)
    date_create = Column(DateTime)
    name = Column(String(64))
    info = Column(String(256))
    image = Column(String(128))
    category_id = Column(Integer, ForeignKey(PostCategory.id), nullable=False)
    category = relationship('PostCategory', lazy='joined')
