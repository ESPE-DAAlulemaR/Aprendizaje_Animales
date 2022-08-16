from flask import Flask, Response, request, session, jsonify, render_template, url_for, redirect
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'development'
app.config['MONGO_URI'] = 'mongodb://localhost/pythonmongodb'
mongo = PyMongo(app)

@app.errorhandler(404)
def not_found(error=None):
    return render_template('404.html')
    
@app.errorhandler(500)
def not_found(error=None):
    return render_template('500.html')

from controllers.AuthController import *
from controllers.HomeController import *
from controllers.UserController import *
from controllers.TeacherController import *
from controllers.StudentController import *

if __name__ == "__main__":
    app.run(debug=True)