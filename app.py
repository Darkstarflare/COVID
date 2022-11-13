#!/usr/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from controllers import city_bp
from controllers import user_bp
from models import database
import config

app = Flask(__name__)

# Register the controllers
app.register_blueprint(city_bp.CITY_BP)
app.register_blueprint(user_bp.USER_BP)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
database.db.init_app(app)

@app.route('/')
def index():
    return 'Hello World'

@app.errorhandler(404)
def page_not_found(e):
    return 'ERROR!!!', 404

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host=config.CONF['host'], port=config.CONF['port'], debug=True)