# coding=utf-8

SYSTEM_ERROR = -1
DATABASE_CONNECTION_ERROR = -2
REDIS_CONNECTION_ERROR = -3
ACCESS_DENIED = -4
NO_DATA_FOUND = -5
OK = 0
INVALID_LOGIN_PASS = -7
NOT_AUTHORIZED = -15
USER_BLOCKED = -16
INVALID_FIRST_PASSWORD = -17
INVALID_PASSWORD = -17
INTEGRITY_ERROR = -18

OBJECT_HAS_NO_CHILDREN = -20
CHILD_OBJECT_CANNOT_BE_PARENT = -21
CANNOT_DELETE_MYSELF = -22

USER_ALREADY_EXISTS = -100
DATA_ALREADY_EXISTS = 100
INVALID_DOMAIN = -101
INVALID_USERNAME = -102
LARGE_FILE_SIZE = 1005
FILE_NOT_ALLOWED = 1006

WRONG_DATA = -103

MESSAGES = {
    'ru': {
        SYSTEM_ERROR: u'Системная ошибка, попробуйте позже',
        NOT_AUTHORIZED: u'Вы не авторизованы, пожалуйста авторизуйтесь!',
        USER_BLOCKED: u'Доступ заблокирован!',
        DATABASE_CONNECTION_ERROR: u'Ошибка соединения с базой данных',
        REDIS_CONNECTION_ERROR: u'Ошибка соединения с Redis',
        ACCESS_DENIED: u'Доступ запрещен',
        NO_DATA_FOUND: u'Данные не найдены',
        INVALID_LOGIN_PASS: u'Неправильный логин или пароль',
        OBJECT_HAS_NO_CHILDREN: u'В объекте дочерних элементов не существует!',
        CHILD_OBJECT_CANNOT_BE_PARENT: u'Дочерний объект не может быть родиельским объектом',
        INVALID_FIRST_PASSWORD: u'Пароль для первого входа не верный. Проверьте и введите заново.',
        INVALID_PASSWORD: u'Старый пароль не верный. Проверьте и введите заново.',
        INTEGRITY_ERROR: u'Ошибка при обработке данных!',
        CANNOT_DELETE_MYSELF: u'Нельзя удалить себя!',
        USER_ALREADY_EXISTS: u'Пользователь с таким логином существует',
        DATA_ALREADY_EXISTS: u'Данные уже существует',
        INVALID_DOMAIN: u'Invalid domain name',
        INVALID_USERNAME: u'Invalid user name',
        LARGE_FILE_SIZE: u'Размер файла не должен превышать 5mb',
        FILE_NOT_ALLOWED: u'Не допустимый файл',
        WRONG_DATA: u'Неверные параметры данных!'
    },
    'en': {},
    'kg': {}
}
