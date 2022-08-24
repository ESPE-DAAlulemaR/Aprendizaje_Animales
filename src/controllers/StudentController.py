from app import *
from controllers.ClassroomController import classroomsShow
import json

# Index Students
@app.route('/students', methods=['GET'])
def studentsIndex():
    students = mongo.db.students.find()
    classrooms = mongo.db.classrooms.find()
    periods = mongo.db.periods.find()
    return render_template('pages/administration/students/index.html', students = students, classrooms = classrooms, periods = periods)

# Show Student
@app.route('/students/<id>', methods=['GET'])
def studentsShow(id):
    student = mongo.db.students.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(student)
    return Response(response, mimetype = "application/json")

# Store Students
@app.route('/students', methods=['POST'])
def studentsStore():
    name = request.form['name']
    lastname = request.form['lastname']
    course = mongo.db.classrooms.find_one({'_id': ObjectId(request.form['course']), })
    period = mongo.db.periods.find_one({'_id': ObjectId(request.form['period']), })

    if request.files['photo']:
        photo = request.files['photo']
        photo.save(PATH_FILE + photo.filename)
        photo_name = photo.filename
    else:
        photo_name = ''

    if name and lastname and course and period:
        course['note'] = 0
        course['attempts'] = 0

        mongo.db.students.insert_one({
            'name': name,
            'lastname': lastname,
            'course': course,
            'photo': photo_name,
            'period': period
        })

    return redirect(url_for("studentsIndex"))

# Update Students
@app.route('/students/update/<_id>', methods=['POST'])
def studentsUpdate(_id):
    name = request.form['name']
    lastname = request.form['lastname']
    course = mongo.db.classrooms.find_one({'_id': ObjectId(request.form['course']), })
    period = mongo.db.periods.find_one({'_id': ObjectId(request.form['period']), })

    if name and lastname and course and period and _id:
        student = mongo.db.students.find_one({'_id': ObjectId(_id), })
        course['note'] = int(student['course']['note'])
        course['attempts'] = int(student['course']['attempts'])

        if request.files['photo']:
            photo = request.files['photo']
            photo.save(PATH_FILE + photo.filename)
            photo_name = photo.filename
        else:
            photo_name = student['photo']
            
        mongo.db.students.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {
                'name': name,
                'lastname': lastname,
                'course': course,
                'photo': photo_name,
                'period': period
            }
        })
    return redirect(url_for("studentsIndex"))

# Delete Students
@app.route('/students/delete/<id>', methods=['POST'])
def studentsDestroy(id):
    mongo.db.students.delete_one({'_id': ObjectId(id)})
    return redirect(url_for("studentsIndex"))

# Notes
@app.route('/students/note/<_id>', methods=['POST'])
def studentNote(_id):
    student = mongo.db.students.find_one({'_id': ObjectId(_id)})
    course = mongo.db.classrooms.find_one({'_id': student['course']['_id'] })

    if request.form['note']:
        auxNote = request.form['note']
        if request.form['attempt'] == True:
            course['attempts'] = student['course']['attempts'] + 1
            note = (student['course']['note'] + auxNote) / course['attempts']
            course['note'] = note
        else:
            course['note'] = auxNote
            course['attempts'] = int(student['course']['attempts'])
    else:
        course['note'] = student['course']['note']
        course['attempts'] = student['course']['attempts']
    
    course['note'] = int(course['note'])
    course['attempts'] = int(course['attempts'])

    mongo.db.students.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
        {'$set': {
            'course': course
        }
    })

    return redirect(request.referrer)