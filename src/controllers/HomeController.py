from app import *
import json

@app.route('/', methods=['GET'])
def index():
    if "user" in session:
        user = json.loads(session['user'])
        return render_template('index.html')
    else:
        return redirect(url_for("login"))

@app.route('/student', methods=['GET'])
def indexStudent():
    if "user" in session:
        return render_template('pages/home/student/index.html')
    else:
        return redirect(url_for("login"))

@app.route('/teacher', methods=['GET'])
def indexTeacher():
    if "user" in session:
        return render_template('pages/home/teacher/index.html')
    else:
        return redirect(url_for("login"))

# Index users
@app.route('/game', methods=['GET'])
def game():
    return render_template('pages/student/game.html')

# Parallel 1
@app.route('/teacher/parallel/1', methods=['GET'])
def parallel_1():
    return render_template('pages/teacher/parallel_1.html')

# Parallel 2
@app.route('/teacher/parallel/2', methods=['GET'])
def parallel_2():
    return render_template('pages/teacher/parallel_2.html')