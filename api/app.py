# coding=utf-8
import logging
import os
import traceback
from time import time

from flask import request, g, Response, send_file
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from api import service
from configuration import UPLOAD_PATH
from core_lib import AppFactory
from core_lib.codes import INTEGRITY_ERROR, MESSAGES
from core_lib.models import db
from core_lib.utils import make_json_response, BusinessException

__author__ = 'Azamatshekin'

app = AppFactory.create_app(__name__)
app.config.from_object('configuration')
db.init_app(app)

CORS(app, headers=['Content-Type', 'Authorization'])


# with app.app_context():
#     db.create_all()
#     db.create_all(bind=['middleware'])


@app.before_request
def before():
    g.time = time()
    g.language = 'ru'
    g.imei = 'web'
    g.request_data = request.json
    if 'Authorization' in request.headers:
        a = request.authorization
        g.imei = a.username
        g.token = a.password
        # if g.imei == 'web':
        #     data = redis_session.get_session(a.password)
        #     if data:
        #         data = json.loads(data)
        #         if data['verified']:
        #             g.token = data['token']
        # else:
        #     g.token = a.password
    if request.method != 'OPTIONS':
        logging.info(u'{0}: Request:{1} - Data:{2}'.format(request.remote_addr, request.url, request.json))


@app.after_request
def after_request(response):
    try:
        db.session.commit()
    except IntegrityError as e:
        code = INTEGRITY_ERROR
        logging.error(traceback.format_exc() + str(code))
        try:
            db.session.rollback()
        finally:
            pass
        e.message = MESSAGES.get(g.language, {}).get(code, 'Unknown error code: {}'.format(code))
        return make_json_response({'result': code, 'message': e.message})
    finally:
        pass
    return response


@app.teardown_request
def teardown(exception):
    if not hasattr(g, 'time'):
        g.time = time()
    logging.info('{0}: Request: {1} finished in {2} sec'.format(request.remote_addr, request.url, time() - g.time))


@app.errorhandler(BusinessException)
@app.errorhandler(Exception)
def core_error(e):
    code = ''
    if hasattr(e, 'code'):
        code = str(e.code)
    logging.error(traceback.format_exc() + code)
    try:
        db.session.rollback()
    finally:
        pass

    if isinstance(e, BusinessException):
        if not e.message:
            e.message = MESSAGES.get(g.language, {}).get(e.code, 'Unknown error code: {}'.format(e.code))
        return make_json_response({'result': e.code, 'message': e.message})
    if isinstance(e, KeyError):
        return make_json_response({'result': -20, 'message': str(e)})
    return make_json_response({'result': -1, 'message': 'Server error'})


@app.route("/api/images/<string:filename>", methods=['GET'])
def get_image(filename):
    # if not hasattr(g, 'token'):
    #     raise BtaException(NOT_AUTHORIZED)
    return send_file(os.path.join(UPLOAD_PATH, filename), mimetype='image/jpeg')


@app.route('/api/auth', methods=['POST'])
def auth():
    data = g.request_data
    data['remote_address'] = request.remote_addr
    results = service.call('user.logon', data)
    # sid = redis_session.open_session(json.dumps({'token': results['token'], 'verified': True}))
    # results.update({'token': None, 'session': results['token']})
    return make_json_response(results)


@app.route("/api/<string:path>/<string:command>", methods=['POST'])
@app.route("/api/<string:path>.<string:command>", methods=['POST'])
def catcher(path, command):
    data = request.json
    # g.user_id = is_authorized()
    # if not hasattr(g, 'token'):
    #     raise BusinessException(NOT_AUTHORIZED)
    # user = service.call('user.current_user', {})
    # if not user:
    #     raise BusinessException(NOT_AUTHORIZED)
    ret = service.call('{}.{}'.format(path, command), data)
    if isinstance(ret, Response):
        return ret
    return make_json_response(ret)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5050)
