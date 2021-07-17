from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from core_lib.models import db
from api.app import app

app.config.from_object('configuration')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
