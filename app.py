from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from routes import *

if __name__ == '__main__':
    from database import init_db
    init_db()
    app.run(debug=True)
