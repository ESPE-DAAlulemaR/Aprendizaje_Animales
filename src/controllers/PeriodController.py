from app import *

# Index periods
@app.route('/periods', methods=['GET'])
def periodsIndex():
    periods = mongo.db.periods.find()
    return render_template('pages/periods/index.html', periods = periods)

# Show period
@app.route('/periods/<id>', methods=['GET'])
def periodsShow(id):
    period = mongo.db.periods.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(period)
    return Response(response, mimetype="application/json")

# Store period
@app.route('/periods', methods=['POST'])
def periodsStore():
    name = request.form['name']
    start_at = request.form['start_at']
    end_at = request.form['end_at']

    if name and start_at and end_at:
        mongo.db.periods.insert_one({
            'name': name,
            'start_at': start_at,
            'end_at': end_at
        })

    return redirect(url_for("periodsIndex"))

# Update period
@app.route('/periods/update/<_id>', methods=['POST'])
def periodsUpdate(_id):
    name = request.form['name']
    start_at = request.form['start_at']
    end_at = request.form['end_at']

    if name and start_at and end_at and _id:
        mongo.db.periods.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {
                'name': name,
                'start_at': start_at,
                'end_at': end_at
            }
        })
    return redirect(url_for("periodsIndex"))

# Delete period
@app.route('/periods/delete/<id>', methods=['POST'])
def periodsDestroy(id):
    mongo.db.periods.delete_one({'_id': ObjectId(id)})
    return redirect(url_for("periodsIndex"))