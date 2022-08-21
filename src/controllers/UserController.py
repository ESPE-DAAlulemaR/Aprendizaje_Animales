from app import *

# Index users
@app.route('/users', methods=['GET'])
def usersIndex():
    users = mongo.db.users.find()
    permissions = mongo.db.permissions.find()
    roles = mongo.db.roles.find()
    return render_template('pages/users/index.html', users = users, roles = roles, permissions = permissions)

# Show user
@app.route('/users/<id>', methods=['GET'])
def usersShow(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")

# Store user
@app.route('/users', methods=['POST'])
def usersStore():
    name = request.form['name']
    lastname = request.form['lastname']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    role = mongo.db.roles.find_one({'_id': ObjectId(request.form['role']), })

    if name and lastname and username and email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({
            'name': name,
            'lastname': lastname,
            'username': username,
            'email': email,
            'password': hashed_password,
            'role': role
        })

    return redirect(url_for("usersIndex"))

# Update user
@app.route('/users/update/<_id>', methods=['POST'])
def usersUpdate(_id):
    name = request.form['name']
    lastname = request.form['lastname']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    role = mongo.db.roles.find_one({'_id': ObjectId(request.form['role']), })

    if name and lastname and username and email and _id:
        if password:
            hashed_password = generate_password_hash(password)
        else:
            user = mongo.db.users.find_one({'_id': ObjectId(_id) })
            hashed_password = user['password']

        mongo.db.users.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {
                'name': name,
                'lastname': lastname,
                'username': username,
                'email': email,
                'password': hashed_password,
                'role': role
            }
        })
    return redirect(url_for("usersIndex"))

# Delete user
@app.route('/users/delete/<id>', methods=['POST'])
def usersDestroy(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    return redirect(url_for("usersIndex"))