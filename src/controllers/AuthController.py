from unicodedata import name
from app import *
import json

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if "user" in session:
            return redirect(url_for("index"))
        return render_template('login.html')

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pass"]
        user = mongo.db.users.find_one({'email': email})

        if user:
            if check_password_hash(user['password'], password):
                session["user"] = json.loads(json_util.dumps(user))
                return redirect(url_for('index'))
            else:
                message = 'Contraseña incorrecta'
                return render_template('login.html', message = message)
        else:
            message = 'Usuario no registrado'
            return render_template('login.html', message = message)

@app.route('/logout', methods=['GET'])
def logout():
    if "user" in session:
        session.pop("user", None)
        return redirect(url_for('login'))
    return redirect(url_for('index'))

@app.route('/login/student', methods=['GET'])
def studentLogin():
    if "student" in session:
        return redirect(url_for("indexStudent"))
    
    students = mongo.db.students.find()
    return render_template('pages/student/login.html', students = students)

@app.route('/login/student/<id>', methods=['GET'])
def studentSession(id):
    if id:
        session["student"] = id
        return redirect(url_for('indexStudent'))
    else:
        return redirect(url_for('studentLogin'))

@app.route('/logout/student', methods=['GET'])
def studentLogout():
    if "student" in session:
        session.pop("student", None)
        return redirect(url_for('studentLogin'))
    return redirect(url_for('indexStudent'))