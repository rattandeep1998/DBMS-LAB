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
		'videos':[],
		'problems':[]
	}
	cursor.execute("SELECT SID, RATING, DESCRIPTION, DATE FROM FEEDBACK WHERE CID = " + cid)
	feedbacks = cursor.fetchall()
	for f in feedbacks:
		cursor.execute("SELECT NAME, DOB, PHONE_NUMBER FROM STUDENT WHERE SID = " + str(f[0]))
		s = cursor.fetchone()
		d['students'].append({'sid':f[0],'name':s[0],'dob':s[1],'phone_number':s[2]})
		d['feedbacks'].append({'sname':s[0],'rating':f[1],'description':f[2],'date':f[3]})

	cursor.execute("SELECT VID, TOPIC FROM COURSE_VIDEO WHERE CID = " + cid)
	videos = cursor.fetchall()
	for v in videos:
		d['videos'].append({'vid':v[0],'topic':v[1]})
		cursor.execute("SELECT PID,QUESTION,OPT1,OPT2,OPT3,OPT4,CORRECT FROM PROBLEM WHERE VID = " + str(v[0]))
		problems = cursor.fetchall()
		for p in problems:
			d['problems'].append({'pid':p[0],'question':p[1],'opt1':p[2],'opt2':p[3],'opt3':p[4],'opt4':p[5],'correct':p[6]})

	return jsonify(d)
	# return render_template('instructor_courses.html', data=d)

# @app.route("/Authenticate")
# def Authenticate():
#     email = request.args.get('email')
#     password = request.args.get('password')
#     cursor = mysql.connect().cursor()
#     cursor.execute("SELECT * from instructor where email='" + email + "' and password='" + password + "'")
#     data = cursor.fetchone()
#     print 'email' + email
#     print 'password' + password

#     if data is None:
#         return "Email or Password is wrong"
#     else:
#         return "Logged in successfully"

# @app.route('/signUp')
# def signUp():
#     return render_template('signUp.html')


# @app.route('/signUpUser', methods=['POST'])
# def signUpUser():
#     user =  request.form['username']
#     password = request.form['password']
    
#     return json.dumps({'status':'OK','user':user,'pass':password})

if __name__ == "__main__":
	app.run(port=8000, debug=True)