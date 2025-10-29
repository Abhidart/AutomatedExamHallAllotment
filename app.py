from flask import Flask, render_template,request,redirect,url_for
app= Flask(__name__)

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


if __name__=='__main__':
    app.run(debug=True)
    