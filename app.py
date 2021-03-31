import os
import jwt
import datetime
from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from resources.event import Event, Allevents, db
from functools import wraps
from modules import logger

# get an application object
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///database/data.db')

# This is a logger used to log the code execution
# just use code_logger.<level>("<your logging message>")
# check modules/logger.py for more details
code_logger = logger.logger("./log/app.log",name=__name__).log

# The token check function
SECRET = "testpass"
def token_required(f):
    '''
    This is a decorator used to force authenction
    when using some http methods
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') 

        if not token:
            return {'message' : 'Token is missing!'}, 401

        try: 
            data = jwt.decode(token, SECRET, algorithms="HS256")
        except Exception as error:
            code_logger.error(error)
            return {'message' : 'Token is invalid!'}, 403

        return f(*args, **kwargs)

    return decorated

# Decorate functions we want to check token using setattr builtin
setattr(Event, "delete", token_required(Event.delete))

# Configure the swagger interface
@app.route("/events/docs/")
@app.route("/events/docs")
def get_docs():
    return render_template("swaggerui.html")

# Get a token to be used in a basic authentication
@app.route('/events/login')
def login():
    '''
    This is a simple http autheication that will ask a user and a passphrase
    Returns a token that will be used in query parameters
    '''
    auth = request.authorization

    if auth and auth.password == 'secret':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET)
        return {'token' : token}

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

api = Api(app)
api.add_resource(Event, '/events/<int:EventID>')
api.add_resource(Allevents, '/events/','/events')


if __name__ == '__main__':
    
    code_logger.info("Initialize database")
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)