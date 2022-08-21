from app import *

# Index matters
@app.route('/matters', methods=['GET'])
def mattersIndex():
    matters = mongo.db.matters.find()
    return render_template('pages/matters/index.html', matters = matters)

# Show matter
@app.route('/matters/<id>', methods=['GET'])
def mattersShow(id):
    matter = mongo.db.matters.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(matter)
    return Response(response, mimetype="application/json")

# Store matter
@app.route('/matters', methods=['POST'])
def mattersStore():
    name = request.form['name']

    if name:
        mongo.db.matters.insert_one({
            'name': name
        })

    return redirect(url_for("mattersIndex"))

# Update matter
@app.route('/matters/update/<_id>', methods=['POST'])
def mattersUpdate(_id):
    name = request.form['name']

    if name:
        mongo.db.matters.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {
                'name': name
            }
        })
    return redirect(url_for("mattersIndex"))

# Delete matter
@app.route('/matters/delete/<id>', methods=['POST'])
def mattersDestroy(id):
    mongo.db.matters.delete_one({'_id': ObjectId(id)})
    return redirect(url_for("mattersIndex"))