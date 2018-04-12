from flask import Flask, request, render_template
from flaskext.mysql import MySQL
import json

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'AppData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
 
@app.route("/")
def hello():
    return "Welcome to Python Flask App!"

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
#     user =  request.form['username'];
#     password = request.form['password'];
#     return json.dumps({'status':'OK','user':user,'pass':password});

if __name__ == "__main__":
    app.run(port=8000, debug=True)