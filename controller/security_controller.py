from flask import g

from core_lib.codes import NOT_AUTHORIZED, USER_BLOCKED, SYSTEM_ERROR, ACCESS_DENIED
from core_lib.models import db, Device, UserRoles
from core_lib.utils import BusinessException


def current_user_id():
    device = db.session.query(Device).filter(Device.token == g.token).first()
    if not device:
        raise BusinessException(NOT_AUTHORIZED)
    # ret = {'name': device.user.fullname, 'role': device.user.role, 'id': device.user.id}
    if device.user.blocked:
        raise BusinessException(USER_BLOCKED)
    return device.user_id


def has_role(role):
    role_query = db.session.query(UserRoles).filter(UserRoles.user_id == current_user_id()) \
        .filter(UserRoles.role == role).first()
    return role_query is not None


def required_roles(roles):
    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            if isinstance(roles, str):
                role_query = db.session.query(UserRoles).filter(UserRoles.user_id == current_user_id()) \
                    .filter(UserRoles.role == roles).first()
                if not role_query:
                    raise BusinessException(ACCESS_DENIED)
            elif isinstance(roles, list):
                if len(roles) > 1:
                    role_query = db.session.query(UserRoles).filter(UserRoles.user_id == current_user_id()) \
                        .filter(UserRoles.role.in_(roles)).first()
                    if not role_query:
                        raise BusinessException(ACCESS_DENIED)
            else:
                BusinessException(SYSTEM_ERROR, 'Invalid require role defined')
            return func(*args, **kwargs)

        return wrapper

    return actual_decorator
