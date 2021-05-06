from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY'] =  "asdjkgasd$#43"

db = SQLAlchemy(app)
migrate = Migrate (app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)

from app.models import tables
from app.controllers import default



