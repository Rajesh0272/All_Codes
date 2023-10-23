from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app) 

@app.route("/")
def index():
    return "Hello"
    
class Drink(db.Model):
    id = db.column(db.INTEGER())
    name=db.column(db.String(80))
    description = db.column(db.String(120))
    
    def __repr__(self):
        return f"{self.name} -{self.description}"
@app.route("/drinks")
def get_drinks():
    return {'drinks':'drink data'}

