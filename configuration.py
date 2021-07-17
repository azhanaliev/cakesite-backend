STATION_DB_NAME = 'db_tortik'
STATION_DB_USER = 'core'
STATION_DB_PASS = 'Pass4Database'

STATION_DB = {
    'user': STATION_DB_USER,
    'pw': STATION_DB_PASS,
    'db': STATION_DB_NAME,
    'host': 'localhost',
    'port': '5432',
}

SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % STATION_DB
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_TRACK_MODIFICATIONS = False
REDIS_URI = "localhost"
REDIS_DB = "10"
UPLOAD_PATH = '//home/backenduser/front_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
IMAGES_URL_PATH = 'https://tortik.kg/api/images'
