from itertools import count
from app import *
import json

@app.route('/', methods=['GET'])
def index():
    if "user" in session:
        if session['user']['role']['role'] == 'admin':
            classrooms = mongo.db.classrooms.find()
            nUsers = mongo.db.users.count_documents({})
            nStudets = mongo.db.students.count_documents({})
            nCalendars = mongo.db.calendars.count_documents({})
            nClassrooms = mongo.db.classrooms.count_documents({})
            return render_template('index.html', classrooms = classrooms, nUsers = nUsers, nStudets = nStudets, nCalendars = nCalendars, nClassrooms = nClassrooms)
        if session['user']['role']['role'] == 'teacher':
            classrooms = mongo.db.classrooms.find({ 'tutor._id': ObjectId(session['user']['_id']['$oid']) })
            return render_template('pages/home/teacher/index.html', classrooms = classrooms)
    else:
        return redirect(url_for("login"))

@app.route('/student', methods=['GET'])
def indexStudent():
    if "student" in session:
        return render_template('pages/student/game.html')
    else:
        return redirect(url_for("studentLogin"))

# Index users
@app.route('/game', methods=['GET'])
def game():
    return render_template('pages/student/game.html')

# Course
@app.route('/course/<id>', methods=['GET'])
def course(id):
    classroom = mongo.db.classrooms.find_one({'_id': ObjectId(id), })
    students = mongo.db.students.find({'course._id': ObjectId(id), })
    return render_template('pages/teacher/course.html', students = students, classroom = classroom)