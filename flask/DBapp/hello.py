from flask import Flask, request, render_template, redirect, url_for, jsonify
from flaskext.mysql import MySQL
import json, datetime

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
	return render_template('index.html')

@app.route('/instructor_login', methods=['GET', 'POST'])
def instructor_login():
	if request.method=='GET':
		return render_template('instructor_login.html', message=request.args.get('message'))
	else:
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
		'iid':iid,
		'cid':cid,
		'students':[],
		'feedbacks':[],
		'videos_problems':[],
	}

	cursor.execute("SELECT SID, DATE, NAME FROM enrolls natural join student WHERE CID = " + cid)
	students = cursor.fetchall()

	for s in students:
		d['students'].append({'sid':s[0],'date':s[1],'sname':s[2]})

	cursor.execute("SELECT NAME, RATING, DESCRIPTION, DATE FROM feedback, student WHERE CID = " + str(cid) + " AND feedback.sid=student.sid")
	feedbacks = cursor.fetchall()

	for f in feedbacks:
		d['feedbacks'].append({'sname':f[0],'rating':f[1],'description':f[2],'date':f[3]})

	cursor.execute("SELECT VID, TOPIC FROM takes NATURAL JOIN course_video WHERE IID = " + str(iid) + " AND CID = " + str(cid))
	videos_problems = cursor.fetchall()

	for v in videos_problems:
		cursor.execute("SELECT duration from video where vid="+str(v[0]))
		duration = cursor.fetchone()[0]
		d['videos_problems'].append({'vid':v[0],'topic':v[1],'duration':duration,'problems':[]})
		l = len(d['videos_problems'])
		cursor.execute("SELECT PID,QUESTION,OPT1,OPT2,OPT3,OPT4,CORRECT FROM problem WHERE VID = " + str(v[0]))
		problems = cursor.fetchall()
		for p in problems:
			d['videos_problems'][l-1]['problems'].append({'pid':p[0],'question':p[1],'opt1':p[2],'opt2':p[3],'opt3':p[4],'opt4':p[5],'correct':p[6]})

	# return jsonify(d)
	return render_template('instructor_courses.html', data=d)

@app.route('/instructor/<iid>/courses/<cid>/add_video', methods=['GET', 'POST'])
def add_video(iid,cid):
	if request.method == 'GET' :
		d={
			'iid':iid,
			'cid':cid,
		} 
		return render_template('add_video.html', data=d, message=request.args.get('message'))

	else:
		content = request.form['content']
		topic = request.form['topic']
		duration = request.form['duration']
		description = request.form['description']

		cursor.execute("SELECT max(vid) from video")
		count = cursor.fetchone()[0]

		query="INSERT into video values ("+str(count+1)+",'"+ str(content) +"',"+str(duration)+",'"+str(description)+"')"
		print(query)
		cursor.execute(query)
		cursor.connection.commit()

		query="INSERT into takes values ("+str(iid)+","+str(count+1)+")"
		print(query)
		cursor.execute(query)
		cursor.connection.commit()

		query="INSERT into course_video values ("+str(cid)+","+str(count+1)+",'"+str(topic)+"')"
		print(query)
		cursor.execute(query)
		cursor.connection.commit()

		return redirect(url_for('instructor_courses', iid=iid, cid=cid))

@app.route('/instructor/<iid>/courses/<cid>/edit_video/<vid>', methods=['GET', 'POST'])
def edit_video(iid,cid,vid):
	pass

@app.route('/instructor/<iid>/courses/<cid>/<vid>/add_problem', methods=['GET', 'POST'])
def add_problem(iid,cid,vid):
	if request.method == 'GET' :
		d={
			'iid':iid,
			'cid':cid,
			'vid':vid,
		} 
		return render_template('add_problem.html', data=d, message=request.args.get('message'))

	else:
		question = request.form['question']
		opt1 = request.form['opt1']
		opt2 = request.form['opt2']
		opt3 = request.form['opt3']
		opt4 = request.form['opt4']
		correct = request.form['correct']

		cursor.execute("SELECT max(pid) from problem")
		count = cursor.fetchone()[0]

		try:
			query="INSERT into problem values ("+str(count+1)+",'"+str(question)+"','"+str(opt1)+"','"+str(opt2)+"','"+str(opt3)+"','"+str(opt4)+"','"+str(correct)+"',"+str(vid)+")"
			print(query)
			cursor.execute(query)
			cursor.connection.commit()
			return redirect(url_for('instructor_courses', iid=iid, cid=cid))
		except:
			return redirect(url_for('add_problem', iid=iid, cid=cid, vid=vid, message="Choose Correct option between 1 and 4"))

@app.route('/instructor/<iid>/courses/<cid>/delete_problem/<pid>', methods=['GET', 'POST'])
def delete_problem(iid,cid,pid):

	cursor.execute("DELETE FROM problem where pid = " + str(pid))
	cursor.connection.commit()

	cursor.execute("DELETE FROM attempted where pid = " + str(pid))
	cursor.connection.commit()
	
	return redirect(url_for('instructor_courses', iid=iid, cid=cid))

@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
	if request.method=='GET':
		return render_template('student_signup.html', message=request.args.get('message'))
	else:
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
		
		try:
			cursor.execute("SELECT max(sid) FROM student")
			count = cursor.fetchone()[0]
			data = (count+1,name,str(dob),address,phone_number,highest_degree,email,password)
			query = "INSERT INTO student VALUES ("+str(count+1)+",'"+name+"','"+dob+"','"+address+"',"+phone_number+",'"+highest_degree+"','"+email+"','"+password+"')"
			print(query)
			cursor.execute(query)
			cursor.connection.commit()
			
			return redirect('/student/'+str(count+1), code=307)

		except Exception as e:
			print(str(e))
			return redirect(url_for('student_signup' , message='You should be atleast 10 years old'))
		

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
	if request.method=='GET':
		return render_template('student_login.html', message=request.args.get('message'))
	else:
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

@app.route('/student/<sid>', methods=['GET', 'POST'])
def student_dashboard(sid):
	print('sid = ', sid)
	cursor.execute("SELECT name from student where sid="+str(sid))
	name=cursor.fetchone()[0]
	d={
		'sid':sid,
		'name':name,
		'enrolled_courses':[],
		'other_courses':[]
	}

	cursor.execute("SELECT cid, name, rating, description, date FROM enrolls natural join course where sid=" + sid)
	enrolled_courses = cursor.fetchall()
	# PERCENTAGE COMPLETED WALA BACHA Hai
	for c in enrolled_courses:
		d['enrolled_courses'].append({'cid':str(c[0]),'cname':str(c[1]),'rating':str(c[2]),'description':str(c[3])})

	query="SELECT cid,name,rating,description,start_date,fees from course where cid not in (select cid from enrolls where sid="+str(sid)+")"
	print(query)
	cursor.execute(query)
	other_courses = cursor.fetchall()
	print(other_courses)
	for c in other_courses:
		data={
			'cid':str(c[0]),
			'cname':str(c[1]),
			'rating':str(c[2]),
			'description':str(c[3]),
			'start_date':str(c[4]),
			'fees':str(c[5]),
		}
		d['other_courses'].append(data)

	return render_template('student_dashboard.html', data=d)

@app.route('/student/<sid>/courses/<cid>', methods=['GET', 'POST'])
def student_courses(sid,cid):
	d = {
		'sid':str(sid),
		'cid':str(cid),
		'feedback':{},
		'attempted':[],
		'videos':[]
	}

	cursor.execute("SELECT vid, topic from course_video where cid = " + str(cid))
	videos = cursor.fetchall()

	for v in videos:
		d['videos'].append({'vid':v[0],'topic':v[1]})

	cursor.execute("SELECT rating, description, date from feedback where sid="+str(sid)+" and cid="+str(cid))
	feedback = cursor.fetchone()
	print('feedback ----- ',  feedback)
	if feedback is None:
		d['feedback']['rating']='-1'
		d['feedback']['description']=''
		d['feedback']['date']=''
	else:
		d['feedback']['rating']=feedback[0]
		d['feedback']['description']=feedback[1]
		d['feedback']['date']=feedback[2]

	return render_template('student_courses.html', data=d, message=request.args.get('message'))

@app.route('/student/<sid>/courses/<cid>/<vid>', methods=['GET', 'POST'])
def courses_video(sid,cid,vid):

	cursor.execute("SELECT content, duration, description from video where vid="+str(vid))
	v_info = cursor.fetchone()

	cursor.execute("SELECT iid, name from takes natural join instructor where vid="+str(vid))
	instructor = cursor.fetchone()

	cursor.execute("SELECT * from problem where vid="+str(vid)+" AND pid NOT IN (SELECT pid from attempted where cid = " + str(cid) + " and sid = " + str(sid) + ")")
	problems = cursor.fetchall()

	d = {
		'sid':sid,
		'cid':cid,
		'attempted':[],
		'video':{
			'vid':vid,
			'iid':instructor[0],
			'instructor':instructor[1],
			'content':v_info[0],
			'duration':v_info[1],
			'description':v_info[2],
			'problems':[]
		}
	}

	for p in problems:
		d['video']['problems'].append({'pid':p[0],'question':p[1],'opt1':p[2],'opt2':p[3],'opt3':p[4],'opt4':p[5],'correct':p[6]})	

	cursor.execute("SELECT pid, question, correct, chosenOption from problem natural join attempted where cid = '%s' and sid = '%s' and vid = '%s'"%(str(cid),str(sid),str(vid)))
	attempted = cursor.fetchall()

	for a in attempted:
		result = a[2]==a[3]
		d['attempted'].append({'pid':a[0], 'question':a[1], 'correct':a[2], 'chosenOption':a[3], 'result':result})

	print(d)

	return render_template('course_video.html', data=d, message=request.args.get('message'))

@app.route('/student/<sid>/courses/<cid>/<vid>/submit/<pid>', methods=['GET', 'POST'])
def submit_problem(sid,cid,vid,pid):
	option = request.form['option']
	print(option)

	try:
		cursor.execute("SELECT * from problem where pid="+str(pid))
		p = cursor.fetchone()

		d={'correct':p[6], 'option':option}

		cursor.execute("INSERT INTO attempted VALUES (%s,%s,%s,%s)"%(str(sid),str(cid),str(pid),str(option)))
		cursor.connection.commit()

		return redirect(url_for('courses_video', sid=sid, cid=cid, vid=vid))

	except Exception as e:
		return redirect(url_for('courses_video', sid=sid, cid=cid, vid=vid, message='Chose option between 1 and 4'))
	

@app.route('/student/<sid>/courses/<cid>/join', methods=['GET', 'POST'])
def join_course(sid, cid):
	if request.method=='GET':
		date=datetime.datetime.now()
		date = str(date).split(' ')[0]
		print(date)
		cursor.execute("INSERT INTO enrolls VALUES (%s,%s,'%s')"%(str(sid),str(cid),date))
		c = cursor.connection.commit()

		return redirect('/student/'+str(sid), code=307)

@app.route('/student/<sid>/courses/<cid>/feedback', methods=['POST'])
def submit_feedback(sid, cid):
	rating = request.form['rating']
	description = request.form['description']
	date=datetime.datetime.now()
	date = str(date).split(' ')[0]
	print(date)
	query="INSERT INTO feedback VALUES ("+str(sid)+","+str(cid)+","+rating+",'"+str(description)+"','"+date+"')"
	print(query)

	try:
		cursor.execute(query)
		cursor.connection.commit()
		return redirect(url_for('student_courses', sid=sid, cid=cid))
	except:
		return redirect(url_for('student_courses', sid=sid, cid=cid, message="Invalid Rating"))

if __name__ == "__main__":
	app.run(port=8000, debug=True)