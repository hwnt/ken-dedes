from flask import Flask, request
import sys
import json
import os
import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity, get_jwt_claims
from datetime import timedelta
from functools import wraps
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['APP_DEBUG'] = True

# JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jd8&xusyJx6')

try:
    env = os.environ.get('FOR_DEV', 0)
    if env == '1':
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)   
        app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    else:
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)   
        app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

except Exception as e:
    raise e

jwt = JWTManager(app)

# authorization for admin only
def adminRequired(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] == 2:
            return fn(*args, **kwargs)
        else:
            return {'status': 'Forbidden', 'message': 'admin only'}, 403
    return wrapper

# authorization for user & provider
def nonAdminRequired(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] == 1 | claims['role'] == 0:
            return fn(*args, **kwargs)
        else:
            return {'status': 'Forbidden', 'message': 'user only'}, 403
    return wrapper

# authorization for everyone 
def everyoneRequired(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] == 1 | claims['role'] == 0 | claims['role'] == 2:
            return fn(*args, **kwargs)
        else:
            return {'status': 'Forbidden', 'message': 'user only'}, 403
    return wrapper

# Database
try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config.from_object(config.TestingConfig)
    else:
        app.config.from_object(config.DevelopmentConfig)

except Exception as e:
    raise e

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Middlewares
@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    app.logger.warning("REQUEST_LOG\t%s", json.dumps({
        'method': request.method,
        'code': response.status,
        'uri': request.full_path,
        'request': requestData,
        'response': json.loads(response.data.decode('utf-8'))
    })
    )
    return response


from apps.users.resources import bp_users
from apps.auth import bp_auth
from apps.categories.resources import bp_categories

version = 'v1'

app.register_blueprint(bp_auth, url_prefix=f'/{version}/auth')
app.register_blueprint(bp_users, url_prefix=f'/{version}/user')
app.register_blueprint(bp_categories, url_prefix=f'/{version}/category')

db.create_all()
