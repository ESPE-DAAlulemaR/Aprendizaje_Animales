from app import *
from controllers.ClassroomController import classroomsShow
import json

# Index Students
@app.route('/students', methods=['GET'])
def studentsIndex():
    students = mongo.db.students.find()
    classrooms = mongo.db.classrooms.find()
    return render_template('pages/administration/students/index.html', students = students, classrooms = classrooms)

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

    if request.files['photo']:
        photo_name = request.files['photo']
        photo = request.files['photo']
        photo.save(PATH_FILE + photo.filename)
    else:
        photo_name = ''

    if name and lastname and course:
        mongo.db.students.insert_one({
            'name': name,
            'lastname': lastname,
            'course': course,
            'photo': photo_name
        })

    return redirect(url_for("studentsIndex"))

# Update Students
@app.route('/students/update/<_id>', methods=['POST'])
def studentsUpdate(_id):
    name = request.form['name']
    lastname = request.form['lastname']
    course = mongo.db.classrooms.find_one({'_id': ObjectId(request.form['course']), })

    if name and lastname and course and _id:
        student = mongo.db.students.find_one({'_id': ObjectId(_id), })

        if request.files['photo']:
            photo = request.files['photo']
            photo.save(PATH_FILE + photo.filename)
            photo_path = PATH_FILE + photo.filename
        else:
            photo_path = student['photo']
        
        mongo.db.students.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {
                'name': name,
                'lastname': lastname,
                'course': course,
                'photo': photo_path
            }
        })
    return redirect(url_for("studentsIndex"))

# Delete Students
@app.route('/students/delete/<id>', methods=['POST'])
def studentsDestroy(id):
    mongo.db.students.delete_one({'_id': ObjectId(id)})
    return redirect(url_for("studentsIndex"))