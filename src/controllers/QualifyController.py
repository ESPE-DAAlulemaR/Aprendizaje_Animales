from app import *

# Index qualifies
@app.route('/qualifies', methods=['GET'])
def qualifiesIndex():
    if session['user']['role']['role'] == 'admin':
        qualifies = mongo.db.qualifies.find()
        nQualifies = mongo.db.qualifies.count_documents({})
    else:
        qualifies = mongo.db.qualifies.find({ 'user._id': ObjectId(session['user']['_id']['$oid']) })
        nQualifies = mongo.db.qualifies.count_documents({ 'user._id': ObjectId(session['user']['_id']['$oid']) })
    return render_template('pages/qualifies/index.html', qualifies = qualifies, nQualifies = nQualifies)

# Show qualifie
@app.route('/qualifies/<id>', methods=['GET'])
def qualifiesShow(id):
    qualify = mongo.db.qualifies.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(qualify)
    return Response(response, mimetype="application/json")

# Store qualifies
@app.route('/qualifies', methods=['POST'])
def qualifiesStore():
    note = request.form['note']
    comments = request.form['comments']

    if note:
        mongo.db.qualifies.insert_one({
            'note': note,
            'comments': comments,
            'user': mongo.db.users.find_one({'_id': ObjectId(ObjectId(session['user']['_id']['$oid'])), })
        })

    return redirect(url_for("qualifiesIndex"))

# Update qualifie
@app.route('/qualifies/update/<_id>', methods=['POST'])
def qualifiesUpdate(_id):
    note = request.form['note']
    comments = request.form['comments']

    if note and _id:
        mongo.db.qualifies.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {
                'note': note,
                'comments': comments,
                'user': mongo.db.users.find_one({'_id': ObjectId(ObjectId(session['user']['_id']['$oid'])), })
            }
        })
    return redirect(url_for("qualifiesIndex"))

# Delete qualifie
@app.route('/qualifies/delete/<id>', methods=['POST'])
def qualifiesDestroy(id):
    mongo.db.qualifies.delete_one({'_id': ObjectId(id)})
    return redirect(url_for("qualifiesIndex"))