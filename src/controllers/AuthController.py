from unicodedata import name
from app import *

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
                sessionUser = json_util.dumps(user)
                session["user"] = sessionUser
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