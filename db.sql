drop database AppData;

create database AppData;
use AppData;

CREATE TABLE attempted ( sid INT NOT NULL, cid INT NOT NULL, pid INT NOT NULL, chosenOption INT NOT NULL, PRIMARY KEY(sid,cid,pid));

CREATE TABLE course ( cid INT NOT NULL, name varchar(50) NOT NULL, rating int, start_date date NOT NULL, description text NOT NULL, fees int NOT NULL, PRIMARY KEY(cid));

CREATE TABLE course_tag ( cid INT NOT NULL, tags varchar(200) NOT NULL, PRIMARY KEY(cid,tags));

CREATE TABLE course_video ( cid INT NOT NULL, vid INT NOT NULL, topic TEXT NOT NULL,PRIMARY KEY(cid,vid));

CREATE TABLE enrolls (sid INT NOT NULL, cid INT NOT NULL,date text NOT NULL,PRIMARY KEY(sid,cid));

CREATE TABLE feedback (sid integer NOT NULL, cid int NOT NULL, rating int NOT NULL check(rating between 1 and 5), description text NOT NULL, date text NOT NULL, primary key(sid, cid));

CREATE TABLE instructor (iid integer NOT NULL, name varchar(20) NOT NULL, dob date NOT NULL, address text, phone_number integer, qualification text NOT NULL, email text NOT NULL, password text NOT NULL, PRIMARY KEY(iid));

CREATE TABLE instructor_expertise (iid integer NOT NULL, expertise varchar(200) NOT NULL, primary key(iid, expertise), foreign key(iid) references instructor(iid));

CREATE TABLE video (vid integer not null,duration integer,description text NOT NULL,PRIMARY key(vid));

CREATE TABLE problem  ( pid INT NOT NULL, question TEXT NOT NULL, opt1 TEXT NOT NULL, opt2 TEXT NOT NULL, opt3 TEXT NOT NULL,opt4 TEXT NOT NULL,correct INT NOT NULL, vid INT NOT NULL, PRIMARY KEY(pid), FOREIGN KEY(vid) REFERENCES video(vid));

CREATE TABLE student ( sid integer NOT NULL, name varchar(20) NOT NULL, dob date NOT NULL, address TEXT, phone_number integer, highest_degree text, email text NOT NULL, password text NOT NULL, PRIMARY KEY(sid));

CREATE TABLE takes ( iid INTEGER NOT NULL, vid INTEGER NOT NULL,PRIMARY KEY(iid,vid));

CREATE TABLE instructor_courses ( iid INTEGER NOT NULL, cid INTEGER NOT NULL, PRIMARY KEY(iid,cid));

DELIMITER $$
CREATE TRIGGER checkrating BEFORE INSERT ON feedback
for each row
begin
if new.rating<0 OR new.rating>5 then
signal sqlstate '45000' set message_text = 'invalid rating';
end if;
end; $$

