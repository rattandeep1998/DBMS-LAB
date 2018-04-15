from flask import Flask, request, render_template, redirect, url_for, jsonify
from flaskext.mysql import MySQL
import json

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'AppData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
cursor = mysql.connect().cursor()
 
@app.route("/")
def hello():
	return "Welcome to Python Flask App!"

@app.route('/instructor_login')
def instructor_login():
	return render_template('instructor_login.html', message=request.args.get('message'))

@app.route('/instructor_login_auth', methods = ['POST'])
def instructor_login_auth():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	cursor.execute("SELECT iid from instructor where email='" + email + "' and password='" + password + "'")
	data = cursor.fetchone()
	print(data)
	if data is None:
		return redirect(url_for('instructor_login', message='Email or Password is invalid'))
	else:
		return redirect('/instructor/'+str(data[0]), code=307)

@app.route('/instructor/<iid>', methods=['POST'])
def instructor_dashboard(iid):
	print('iid = ', iid)
	cursor.execute("SELECT name FROM instructor where iid=" + iid)
	name = cursor.fetchone()[0]
	cursor.execute("SELECT CID FROM instructor_courses where iid=" + iid)
	cids = cursor.fetchall()
	d={
		'iid':iid,
		'name':name,
		'cid':[],
		'cname':[]
	}
	for c in cids:
		cid = str(c[0])
		print('cid = ', cid)
		cursor.execute("SELECT name FROM course where cid=" + cid)
		name = cursor.fetchone()[0]
		d['cid'].append(cid)
		d['cname'].append(name)

	return render_template('instructor_dashboard.html', data=d)

@app.route('/instructor/<iid>/courses/<cid>', methods=['GET', 'POST'])
def instructor_courses(iid, cid):
	d={
		'students':[],
		'feedbacks':[],
		'videos_problems':[],
	}

	cursor.execute("SELECT SID, DATE FROM enrolls WHERE CID = " + cid)
	students = cursor.fetchall()

	for s in students:
		d['students'].append({'sid':s[0],'date':s[1]})

	cursor.execute("SELECT NAME, RATING, DESCRIPTION, DATE FROM feedback, student WHERE CID = " + str(cid) + " AND feedback.sid=student.sid")
	feedbacks = cursor.fetchall()

	for f in feedbacks:
		d['feedbacks'].append({'sname':f[0],'rating':f[1],'description':f[2],'date':f[3]})

	cursor.execute("SELECT VID, TOPIC FROM takes NATURAL JOIN course_video WHERE IID = " + str(iid) + " AND CID = " + str(cid))
	videos_problems = cursor.fetchall()

	for v in videos_problems:
		d['videos_problems'].append({'vid':v[0],'topic':v[1],'problems':[]})
		l = len(d['videos_problems'])
		cursor.execute("SELECT PID,QUESTION,OPT1,OPT2,OPT3,OPT4,CORRECT FROM problem WHERE VID = " + str(v[0]))
		problems = cursor.fetchall()
		for p in problems:
			d['videos_problems'][l-1]['problems'].append({'pid':p[0],'question':p[1],'opt1':p[2],'opt2':p[3],'opt3':p[4],'opt4':p[5],'correct':p[6]})

	return jsonify(d)
	# return render_template('instructor_courses.html', data=d)

@app.route('/instructor/<iid>/courses/<cid>/add_video', methods=['GET', 'POST'])
def add_video(iid,cid):
	pass

@app.route('/instructor/<iid>/courses/<cid>/edit_video/<vid>', methods=['GET', 'POST'])
def edit_video(iid,cid,vid):
	pass

@app.route('/instructor/<iid>/courses/<cid>/add_problem', methods=['GET', 'POST'])
def add_problem(iid,cid):
	pass

@app.route('/instructor/<iid>/courses/<cid>/edit_problem/<pid>', methods=['GET', 'POST'])
def edit_problem(iid,cid,pid):
	pass

@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
	return render_template('student_signup.html', message=request.args.get('message'))

@app.route('/student_register', methods=['POST'])
def student_register():
	name = request.form['name']
	dob = request.form['dob']
	address = request.form['address']
	phone_number = request.form['phone_number']
	highest_degree = request.form['highest_degree']
	email = request.form['email']
	password = request.form['password']

	print(name, dob, address, phone_number, highest_degree, email, password)
	cursor.execute("SELECT sid from student where email='" + email + "'")
	f = cursor.fetchone()
	if f is not None:
		return redirect(url_for('student_signup', message='User already exists'))
	
	cursor.execute("SELECT COUNT(*) FROM student")
	count = cursor.fetchone()[0]
	data = (count+1,name,str(dob),address,phone_number,highest_degree,email,password)
	query = "INSERT INTO student VALUES ("+str(count+1)+",'"+name+"','"+dob+"','"+address+"',"+phone_number+",'"+highest_degree+"','"+email+"','"+password+"')"
	print(query)
	cursor.execute(query)
	cusor.connection.commit()
	print('-----')
	return redirect('/student/'+str(count+1), code=307)

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
	return render_template('student_login.html', message=request.args.get('message'))

@app.route('/student_login_auth', methods = ['POST'])
def student_login_auth():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	cursor.execute("SELECT sid from student where email='" + email + "' and password='" + password + "'")
	data = cursor.fetchone()
	print(data)
	if data is None:
		return redirect(url_for('student_login', message='Email or Password is invalid'))
	else:
		return redirect('/student/'+str(data[0]), code=307)

@app.route('/student/<sid>', methods=['POST'])
def student_dashboard(sid):
	print('sid = ', sid)
	cursor.execute("SELECT cid, date FROM enrolls where sid=" + sid)
	courses = cursor.fetchall()

	for c in courses:
		pass

	return sid
	# d={
	# 	'iid':iid,
	# 	'name':name,
	# 	'cid':[],
	# 	'cname':[]
	# }

	# return render_template('student_dashboard.html', data=d)

if __name__ == "__main__":
	app.run(port=8000, debug=True)