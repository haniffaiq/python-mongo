from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)

# Load configuration from instance/config.py
app.config.from_pyfile('./config.py')

# Initialize PyMongo
mongo = PyMongo(app)

# Register blueprints (routes) from app/routes.py
from app.users.routes import users_bp
# from app.routes import routes
app.register_blueprint(users_bp)
# app.register_blueprint(routes)





# if __name__ == '__main__':
#     app.run()
