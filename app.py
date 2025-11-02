import mysql.connector
from flask import Flask, render_template,request,redirect,url_for



    
app= Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",           # replace with your MySQL username
    password="12345",  # replace with your MySQL password
    database="exam_allotment")
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/insert',methods=['GET','POST'])
def how_many():
    if request.method=='POST':
        num_students=int(request.form['num_students'])
        return render_template('student_form.html',num_students=num_students)
    return render_template('how_many.html')

@app.route('/submit', methods=['POST'])
def submit():
    ids = request.form.getlist('id[]')
    names = request.form.getlist('name[]')
    branches = request.form.getlist('branch[]')
    reg_nums = request.form.getlist('reg_num[]')
    students = []
    for i in range(len(ids)):
        students.append({
            'id': ids[i],
            'name': names[i],
            'branch': branches[i],
            'reg_num': reg_nums[i]
        })
    return render_template('results.html', students=students)


@app.route('/rooms')
def rooms():
    cursor.execute("SELECT DISTINCT room_no FROM exam_halls")
    all_rooms = cursor.fetchall()
    return render_template('rooms.html', rooms=[room[0] for room in all_rooms])

@app.route('/room/<room_no>')
def room_students(room_no):
    query = """
        SELECT eh.id, eh.seat_no, s.id, s.name, s.branch, s.register_no
        FROM exam_halls eh
        JOIN students s ON eh.student_id = s.id
        WHERE eh.room_no = %s AND eh.is_occupied = 1
    """
    cursor.execute(query, (room_no,))
    students = cursor.fetchall()
    return render_template('room_students.html', students=students, room_no=room_no)






if __name__=='__main__':
    app.run(debug=True)
    