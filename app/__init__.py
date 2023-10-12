from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager


app = Flask(__name__)
jwt = JWTManager(app)

app.secret_key = 'kuncirahasiasaya'

# Konfigurasi Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = 'secret_key_yang_amat_rahasia'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
# Load configuration from instance/config.py
app.config.from_pyfile('./config.py')

# Initialize PyMongo
mongo = PyMongo(app)

# Register blueprints (routes) from app/routes.py
from app.users.routes import users_bp
from app.auth.routes import auth_bp
# from app.routes import routes
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
# app.register_blueprint(routes)


