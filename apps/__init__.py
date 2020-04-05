from flask import Flask, request
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

################################
# JWT
################################
app.config['JWT_SECRET_KEY'] = 'A28s0(@2s909s0s90s90s9s09s)'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)


def adminRequired(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role']:
            return fn(*args, **kwargs)
        else:
            return {'status': 'Forbidden', 'message': 'admin only'}, 403
    return wrapper


def userRequired(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['role']:
            return fn(*args, **kwargs)
        else:
            return {'status': 'Forbidden', 'message': 'user only'}, 403
    return wrapper
####################
# Database
#############


try:
    env = os.environ.get('FLASK_ENV', 'development')
    # env = 'testing'
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

#########################################
# Middlewares
#########################################
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


db.create_all()
