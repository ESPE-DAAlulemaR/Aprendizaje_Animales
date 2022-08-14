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
