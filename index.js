var express = require('express')
var mysql = require('mysql')
var app = express();
app.set('view engine', 'ejs');
app.use(express.static("public"));
const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({extended: true}));

var con = mysql.createConnection({
	host: 'localhost',
	user: 'root',
	password: 'rattandeep1998',
	database: 'mydb'
});

con.connect(function(err) {
	if(err)	throw err;
	console.log("CONNECTED");
});

app.get('/', function(req,res) {
	res.render('index');
});


//------------------------------------------------------------------------------------

app.get('/teacher/login/', function(req,res) {

	res.render('teacher_login');
});















// -----------------------------------------------------------------------------------
app.post('/student',function(req,res) {
	console.log(req.body);


	sql = "insert into student values(\""+req.body.email+"\",\""+req.body.password+"\")";
	console.log("lallalalala");
	console.log(sql);

	con.query(sql, function(err,result) {
		if(err) throw err;
		console.log(result);
	});

	res.send("STUDENT INSERTED");
});

app.get('/show-students',function(req,res) {
	sql = "select * from student";

	con.query(sql, function(err,result,fields) {
		if(err) throw err;
		console.log(result);
		
		//--Not Required console.log(fields);
	});

	res.send("STUDENTS SHOWN");

});

app.listen(3000);