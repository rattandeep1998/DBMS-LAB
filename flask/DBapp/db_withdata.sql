drop database AppData;

create database AppData;
use AppData;

CREATE TABLE attempted (
	sid INT NOT NULL,
	cid INT NOT NULL,
	pid INT NOT NULL,
	chosenOption INT NOT NULL,
	PRIMARY KEY(sid,cid,pid)
);

CREATE TABLE course (
	cid INT NOT NULL, 
	name varchar(50) NOT NULL, 
	rating int, 
	start_date date NOT NULL, 
	description text NOT NULL, 
	fees int NOT NULL, 
	PRIMARY KEY(cid)
);

CREATE TABLE course_tag (
	cid INT NOT NULL,
	tags varchar(200) NOT NULL,
	PRIMARY KEY(cid,tags)
);

CREATE TABLE course_video ( 
	cid INT NOT NULL, 
	vid INT NOT NULL, 
	topic TEXT NOT NULL,
	PRIMARY KEY(cid,vid)
);

CREATE TABLE enrolls (
	sid INT NOT NULL, 
	cid INT NOT NULL,
	date text NOT NULL,
	PRIMARY KEY(sid,cid)
);

CREATE TABLE feedback (
	sid integer NOT NULL, 
	cid int NOT NULL,
	rating int NOT NULL check(rating between 1 and 5), 
	description text NOT NULL, 
	date text NOT NULL, 
	primary key(sid, cid)
);

CREATE TABLE instructor (
	iid integer NOT NULL, 
	name varchar(20) NOT NULL, 
	dob date NOT NULL, 
	address text, 
	phone_number varchar(10), 
	qualification text NOT NULL, 
	email text NOT NULL, 
	password text NOT NULL, 
	PRIMARY KEY(iid)
);

CREATE TABLE instructor_expertise (
	iid integer NOT NULL, 
	expertise varchar(200) NOT NULL, 
	primary key(iid, expertise), 
	foreign key(iid) references instructor(iid)
);

CREATE TABLE video (
	vid integer not null,
	content text not null,
	duration integer,
	description text NOT NULL,
	PRIMARY key(vid)
);

CREATE TABLE problem  ( 
	pid INT NOT NULL, 
	question TEXT NOT NULL, 
	opt1 TEXT NOT NULL, 
	opt2 TEXT NOT NULL, 
	opt3 TEXT NOT NULL,
	opt4 TEXT NOT NULL,
	correct INT NOT NULL, 
	vid INT NOT NULL, 
	PRIMARY KEY(pid), 
	FOREIGN KEY(vid) REFERENCES video(vid)
);

CREATE TABLE student ( 
	sid integer NOT NULL, 
	name varchar(20) NOT NULL, 
	dob date NOT NULL, 
	address TEXT, 
	phone_number varchar(10), 
	highest_degree text, 
	email text NOT NULL, 
	password text NOT NULL, 
	PRIMARY KEY(sid)
);

CREATE TABLE takes ( 
	iid INTEGER NOT NULL, 
	vid INTEGER NOT NULL,
	PRIMARY KEY(iid,vid)
);

CREATE TABLE instructor_courses ( 
	iid INTEGER NOT NULL, 
	cid INTEGER NOT NULL, 
	PRIMARY KEY(iid,cid)
);



DELIMITER $$
CREATE TRIGGER checkrating BEFORE INSERT ON feedback
for each row
begin
if new.rating<0 OR new.rating>5 then
signal sqlstate '45000' set message_text = 'invalid rating';
end if;
end; $$

DELIMITER $$
CREATE TRIGGER checkproblemoption BEFORE INSERT ON problem
for each row
begin
if new.correct<0 OR new.correct>4 then
signal sqlstate '45000' set message_text = 'Choose option between 1 and 4';
end if;
end; $$

DELIMITER $$
CREATE TRIGGER checkattemptedoption BEFORE INSERT ON attempted
for each row
begin
if new.chosenOption<0 OR new.chosenOption>4 then
signal sqlstate '45000' set message_text = 'Choose option between 1 and 4';
end if;
end; $$

DELIMITER $$
CREATE TRIGGER checkstudentdateofbirth BEFORE INSERT ON student
for each row
begin
if new.dob > DATE_SUB(Date(SYSDATE()), INTERVAL 10 YEAR)  then
signal sqlstate '45000' set message_text = 'DOB should be less than current date';
end if;
end; $$



INSERT into student values(101,'RATTANDEEP SINGH','1998-07-03','Tilak Nagar, New Delhi',8447151548,'BTECH','merattandeep@gmail.com','pass123');
INSERT into student values(102,'RAJAT SINGHAL','1997-02-01','Dwarka, New Delhi',8447151548,'BE','rs@gmail.com','rrrr');
INSERT into student values(103,'RAUNAQ','1997-09-05','Paschim Vihar, New Delhi',999999999,'MS','raunaqsuryakhattar@gmail.com','abcd123');

INSERT into instructor values(201,'Ram Kumar','1975-01-01','Banglore',2188192681,'PHD','ramkumar@gmail.com','ramu123');
INSERT into instructor values(202,'Shyam Malhotra','1980-05-04','Chennai',1219821999,'MBA','shyam@gmail.com','password');
INSERT into instructor values(203,'Anand Shenoi','1984-06-22','Hyderabad',8877999735,'MCOM','ashenoi@gmail.com','anand');

INSERT into course values(1,'DATA STRUCTURES',4,'2018-05-10','DS Course',20000);
INSERT into course values(2,'WEB DEVELOPMENT',3,'2018-05-15','WEB Development Course',23000);
INSERT into course values(3,'MACHINE LEARNING',5,'2018-04-20','ML Course',30000);

INSERT into course_tag values(1,'DS');
INSERT into course_tag values(1,'Beginner');
INSERT into course_tag values(2,'WEBD');
INSERT into course_tag values(2,'Advanced');
INSERT into course_tag values(3,'ML');
INSERT into course_tag values(3,'Data Science');
INSERT into course_tag values(3,'Advanced');

INSERT into video values(301,"https://www.youtube.com/embed/bjtvf_BFMgs",5,'Video on Arrays');
INSERT into video values(302,"https://www.youtube.com/embed/eGnlKPCkAFY",35,'Video on Linked Lists');
INSERT into video values(303,"https://www.youtube.com/embed/y3UH2gAhwPI",24,'Video on HTML');
INSERT into video values(304,"https://www.youtube.com/embed/Ukg_U3CnJWI",17,'Video on Javascript');
INSERT into video values(305,"https://www.youtube.com/embed/zPG4NjIkCjc",9,'Video on Linear Regression');
INSERT into video values(306,"https://www.youtube.com/embed/IHZwWFHWa-w",2,'Video on Gradient Descent');

INSERT into course_video values(1,301,'arrays');
INSERT into course_video values(1,302,'lists');
INSERT into course_video values(2,303,'front end html');
INSERT into course_video values(2,304,'front end javascript');
INSERT into course_video values(3,305,'linear regression');
INSERT into course_video values(3,306,'gradient descent');

INSERT into enrolls values(101,1,'2018-05-15');
INSERT into enrolls values(101,2,'2018-09-09');
INSERT into enrolls values(101,3,'2018-04-08');
INSERT into enrolls values(102,2,'2018-06-10');
INSERT into enrolls values(103,1,'2018-05-15');
INSERT into enrolls values(103,2,'2018-05-15');

INSERT into instructor_expertise values(201,'swag');
INSERT into instructor_expertise values(202,'motivator');
INSERT into instructor_expertise values(202,'exceptional');
INSERT into instructor_expertise values(203,'professional');
INSERT into instructor_expertise values(203,'cool');

INSERT into problem values(501,'Size of array {12,45,22} ?','1','2','3','4',3,301);
INSERT into problem values(502,'Value of a[1] where a={8,3,9,1} ?','8','3','9','1',2,301);
INSERT into problem values(503,'Which of the following sorting algorithms can be used to sort a random linked list with minimum time complexity?','insertion','quick','heap','merge',4,302);
INSERT into problem values(504,'In the worst case, the number of comparisons needed to search a singly linked list of length n for a given element is ?','log2n','n/2','log2n-1','n',4,302);
INSERT into problem values(505,'The common element which describe the web page, is ?','heading','paragraph','list','all',4,303);
INSERT into problem values(506,'HTML stands for?','Hyper Text Markup Language','High Text Markup Language','Hyper Tabular Markup Language','None',1,303);
INSERT into problem values(507,'Javascript is ?','programming','applicaion','scripting','none',3,304);
INSERT into problem values(508,'To test linear relationship of y(dependent) and x(independent) continuous variables, which of the following plot best suited?','Scatter plot','Barchart','Histograms','None',1,305);
INSERT into problem values(509,'A correlation between age and health of a person found to be -1.09.  On the basis of this you would tell the doctors that:',' The age is good predictor of health','The age is poor predictor of health','none','both',3,305);
INSERT into problem values(510,'What are general limitations of back propagation rule?','local minima','slow convergence','scaling','all',4,306);

INSERT into attempted values(101,1,501,3);
INSERT into attempted values(101,2,505,3);
INSERT into attempted values(101,3,510,4);
INSERT into attempted values(102,2,506,3);
INSERT into attempted values(103,2,507,3);

INSERT into feedback values(101,1,5,'awesome course','2018-05-30');
INSERT into feedback values(101,3,4,'mindblowing','2018-04-15');
INSERT into feedback values(102,2,2,'good','2018-06-30');

INSERT into instructor_courses values(201,1);
INSERT into instructor_courses values(201,3);
INSERT into instructor_courses values(202,2);
INSERT into instructor_courses values(202,3);
INSERT into instructor_courses values(203,1);

INSERT into takes values(201,301);
INSERT into takes values(203,302);
INSERT into takes values(202,303);
INSERT into takes values(202,304);
INSERT into takes values(201,305);
INSERT into takes values(202,306);

