import datetime
import decimal
import io
import json
import logging
import os
import random
import string
from copy import copy

# from PIL import Image, ImageDraw, ImageFont
from dateutil import parser
from flask import Response
# from resizeimage import resizeimage
from sqlalchemy import Date
from sqlalchemy.ext.declarative.api import DeclarativeMeta


__author__ = 'Azamatshekin'


class JSONEncoderCore(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            r = str(o)[:19]
            return r
        elif isinstance(o, datetime.date):
            return str(o)
        elif isinstance(o, datetime.time):
            r = str(o)
            return r
        elif isinstance(o, decimal.Decimal):
            return fakefloat(o)
        elif isinstance(o, datetime.timedelta):
            return o.total_seconds()
        elif isinstance(o.__class__, DeclarativeMeta):
            return orm_to_json(o)
        else:
            return super(JSONEncoderCore, self).default(o)


class fakefloat(float):
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return str(self._value)


def make_json_response(p_content, status=200):
    if not p_content:
        p_content = {}
    if 'result' not in p_content:
        p_content.update({'result': 0})

    if p_content['result'] == 0:
        status = 200
    elif p_content['result'] == -1:
        status = 500
    elif p_content['result'] == -15:
        status = 401
    elif p_content['result'] == -16:
        status = 403
    else:
        status = 405

    json_string = json.dumps(p_content, cls=JSONEncoderCore)
    #    save_request(json_string, is_resp=True, is_xml=False)
    resp = Response(json_string, mimetype='application/json; charset=utf-8', status=status)
    return resp


class BusinessException(Exception):
    def __init__(self, code, message=None):
        super(BusinessException, self).__init__()
        self.code = code
        self.message = message


def json_to_orm(json_, orm):
    """
    Merge in items in the values dict into our object if it's one of our columns
    """
    if hasattr(orm, '__table__'):
        for c in orm.__table__.columns:
            if c.name in json_:
                if isinstance(c.type, Date):
                    setattr(orm, c.name, None if not json_[c.name] else parser.parse(json_[c.name]))
                else:
                    setattr(orm, c.name, json_[c.name])
    else:
        for c in orm._asdict().keys():
            if c in json_:
                setattr(orm, c, json_[c])


def orm_to_json(orm):
    if isinstance(orm, list):
        ret = []
        for o in orm:
            if hasattr(o, '__dict__'):
                d = copy(o.__dict__)
            else:
                d = o._asdict()
            d.pop('_sa_instance_state', None)
            ret.append(d)
        return ret
    else:
        if hasattr(orm, '__dict__'):
            d = copy(orm.__dict__)
        else:
            d = orm._asdict()
        d.pop('_sa_instance_state', None)
        return d


def generate_password(pass_length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(pass_length))


def allowed_photo(content_type):
    return content_type in ['image/jpg', 'image/jpeg', 'image/png']


def allowed_file(content_type):
    # ['avi', 'flv', 'wmv', 'mov', 'mp4', 'mp3', 'wma', 'ogg']
    return True


# def upload_photo(photo, filename, folder=None):
#     if not hasattr(photo, 'content_type'):
#         raise BusinessException(FILE_NOT_ALLOWED)
#     if photo and allowed_photo(photo.content_type):
#         file_bytes = photo.read()
#         if len(file_bytes) > (5 * 1024 * 1024):
#             raise BusinessException(LARGE_FILE_SIZE)
#         upload_path = UPLOAD_PATH
#         photo_url = PHOTO_UPLOADS_URL
#         if folder:
#             upload_path = os.path.join(upload_path, folder)
#             photo_url = photo_url + folder + '/'
#         if not os.path.exists(upload_path):
#             os.makedirs(upload_path)
#         img = Image.open(io.BytesIO(file_bytes))
#         width, height = img.size
#         if height > 400:
#             img = resizeimage.resize_height(img, 400)
#         # # --> drawing image eltor
#         # draw = ImageDraw.Draw(img)
#         # # font = ImageFont.truetype("sans-serif.ttf", 16)
#         # draw.text((0, 0), "Eltor", (255, 255, 255))
#         # # --< end of draw
#
#         img.save(os.path.join(upload_path, filename), img.format)
#         return photo_url + filename
#     else:
#         raise BusinessException(FILE_NOT_ALLOWED)
#
#
# def upload_file(file_to_upload, filename, folder=None):
#     if not hasattr(file_to_upload, 'content_type'):
#         raise BusinessException(FILE_NOT_ALLOWED)
#     if file_to_upload and allowed_file(file_to_upload.content_type):
#         file_bytes = file_to_upload.read()
#         if len(file_bytes) > (20 * 1024 * 1024):
#             raise BusinessException(LARGE_FILE_SIZE)
#         upload_path = UPLOAD_PATH
#         photo_url = FILE_UPLOADS_URL
#         if folder:
#             upload_path = os.path.join(upload_path, folder)
#             photo_url = photo_url + folder + '/'
#         if not os.path.exists(upload_path):
#             os.makedirs(upload_path)
#
#         with open(os.path.join(upload_path, filename), 'wb') as f:
#             f.write(file_bytes)
#             f.close()
#         return photo_url + filename
#     else:
#         raise BusinessException(FILE_NOT_ALLOWED)
#
#
# def del_file(filename, folder=None):
#     if filename:
#         try:
#             upload_path = UPLOAD_PATH
#             if folder:
#                 upload_path = os.path.join(upload_path, folder)
#             os.remove(os.path.join(upload_path, filename))
#         except Exception as e:
#             logging.info('DELETE FILE ERROR: ' + str(e))
