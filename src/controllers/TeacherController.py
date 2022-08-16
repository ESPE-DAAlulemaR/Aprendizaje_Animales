from app import *

# Parallel 1
@app.route('/teacher/parallel/1', methods=['GET'])
def parallel_1():
    return render_template('pages/teacher/parallel_1.html')

# Parallel 2
@app.route('/teacher/parallel/2', methods=['GET'])
def parallel_2():
    return render_template('pages/teacher/parallel_2.html')