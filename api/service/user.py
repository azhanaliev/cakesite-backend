# coding=utf-8
import re
import uuid
from datetime import datetime


from controller import security_controller, crud_controller
from controller.security_controller import current_user_id, required_roles
from core_lib.codes import INVALID_LOGIN_PASS, USER_BLOCKED, INVALID_USERNAME, NO_DATA_FOUND, INVALID_PASSWORD, \
    WRONG_DATA, SYSTEM_ERROR
from core_lib.models import db, User, Device, UserRoles
from core_lib.utils import BusinessException, orm_to_json

regex = re.compile('^(?=.{5,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$')


def logon(bag):
    user = db.session.query(User).filter(User.username == bag['username'].lower()).filter(
        User.password == bag['password']).first()
    if user is None:
        raise BusinessException(INVALID_LOGIN_PASS)
    if user.blocked:
        raise BusinessException(USER_BLOCKED)
    device = db.session.query(Device) \
        .filter(Device.user_id == user.id).first()
    if device is None:
        device = Device()
    device.date = datetime.now()
    device.user_id = user.id
    device.token = str(uuid.uuid4())  # generate unique token
    db.session.add(device)
    db.session.flush()

    result = {'session': device.token, 'name': user.name, 'roles': []}
    roles_query = db.session.query(UserRoles).filter(UserRoles.user_id == user.id)
    for r in roles_query:
        result['roles'].append(r.role)

    return result


def check_username(username):
    if not username:
        raise BusinessException(INVALID_USERNAME)

    if not regex.search(username):
        raise BusinessException(INVALID_USERNAME)


def change_password(bag):
    u = db.session.query(User).filter(User.id == current_user_id()).first()
    if not u:
        raise BusinessException(NO_DATA_FOUND)
    if u.password != bag['old_password']:
        raise BusinessException(INVALID_PASSWORD)
    u.password = bag['new_password']
    return u


#@required_roles("ADMIN")
def get_list(bag):
    result_list = []
    query = db.session.query(User)

    if bag.get('username'):
        query = query.filter(User.username.ilike('%' + bag['username'] + '%'))
    if bag.get('name'):
        query = query.filter(User.name.ilike('%' + bag['name'] + '%'))

    query = query.order_by(User.name.asc()).all()
    for r in query:
        user = {
            'id': r.id,
            'username': r.username,
            'name': r.name,
            'surname': r.surname,
            'patronymic': r.patronymic,
            'blocked': r.blocked,
            'roles': [],
        }
        query_perm = db.session.query(UserRoles).filter(UserRoles.user_id == r.id)
        for ur in query_perm:
            user['roles'].append(ur.role)
        result_list.append(user)
    return {'list': result_list}


#@required_roles("ADMIN")
def create(bag):
    u = User()
    u.username = bag['username'].lower()
    u.surname = bag['surname']
    u.patronymic = bag['patronymic']
    u.password = bag['password']
    u.name = bag['name']
    u.date_create = datetime.now()
    u.blocked = False

    db.session.add(u)
    db.session.flush()

    for p in bag['roles']:
        up = UserRoles()
        up.user_id = u.id
        up.role = p

        db.session.add(up)
        db.session.flush()

    return {}


#@required_roles("ADMIN")
def update(bag):
    m = db.session.query(User).filter(User.id == bag['id']).first()
    if not m:
        raise BusinessException(NO_DATA_FOUND)
    m.username = bag['username'].lower()
    m.name = bag['name']
    m.surname = bag['surname']
    m.patronymic = bag['patronymic']

    for up in db.session.query(UserRoles).filter(UserRoles.user_id == m.id):
        # if up.role == 'ADMIN':
        #     if current_user_id() == bag['id']:
        #         raise BusinessException(WRONG_DATA, 'Удалить свою роль Администратора запрещена!')
        db.session.delete(up)

    for p in bag['roles']:
        up = UserRoles()
        up.user_id = m.id
        up.role = p
        db.session.add(up)
        db.session.flush()

    return {}


#@required_roles("ADMIN")
def block(bag):
    m = db.session.query(User).filter(User.id == bag['id']).first()
    if not m:
        raise BusinessException(NO_DATA_FOUND)
    m.blocked = True
    return {}


#@required_roles("ADMIN")
def unblock(bag):
    m = db.session.query(User).filter(User.id == bag['id']).first()
    if not m:
        raise BusinessException(NO_DATA_FOUND)
    m.blocked = False
    return {}


def delete(bag):
    for up in db.session.query(UserRoles).filter(UserRoles.user_id == bag['id']):
        db.session.delete(up)

    try:
        crud_controller.delete(User, bag)
    except:
        raise BusinessException(SYSTEM_ERROR, u'Невозможно удалить пользователя, запись используется в другом месте')
    return {}
