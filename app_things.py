from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#para mysql
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://flask_app:flask_pass@localhost/calibracion"
app.config['MYSQL_DATABASE_USER'] = 'flask_app'
app.config['MYSQL_DATABASE_PASSWORD'] = 'flask_pass'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
