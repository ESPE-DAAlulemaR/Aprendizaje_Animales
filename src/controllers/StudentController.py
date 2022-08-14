from app import *

# Index users
@app.route('/game', methods=['GET'])
def game():
    return render_template('pages/student/game.html')