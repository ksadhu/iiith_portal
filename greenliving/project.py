import MySQLdb
import sha
import smtplib
import time
from mod_python import Session
from mod_python.util import redirect
conn=MySQLdb.connect(host="localhost",db="test")
curs=conn.cursor()
curs.execute("create table if not exists account(name varchar(30),roomno varchar(10),hostel varchar(10),rollno bigint,email varchar(50),passwd varchar(50))")
de="no"
de1="none"
curs.execute("create table if not exists courier(courierid int,name varchar(30),roomno varchar(10),hostel varchar(10),type varchar(20),fromaddr varchar(100),date_arrvd date,recvd varchar(5) default '%s',receiver varchar(30) default '%s')"%(de,de1))
def account(req,name="",roomno="",hostel="",rollno=0,loginid="",pswd="",pswd1=""):
      if name!="" and roomno!="" and hostel!="" and rollno!=0 and pswd!="" and pswd1!="":
	p,p1=sha.new(pswd),sha.new(pswd1)
	q,q1=p.hexdigest(),p1.hexdigest()
	if q!=q1:
		redirect(req,'acntpage');
	curs.execute("select * from account")
	w=req.form.getlist("hostel")
	q2=curs.fetchall();
	k=0;
	for j in q2:
		if j[4]!=loginid and j[4]!=None:
			k=k+1;
	if k==len(q2):
			curs.execute("insert into account(name,roomno,hostel,rollno,email,passwd) values('%s','%s','%s','%d','%s','%s')" %(name,roomno,w[0],int(rollno),loginid,q))
	else:
		a=["","","","","",""]
		if hostel=="obh":
			a[0]="checked=\"checked\""
		elif hostel=="nbh":
			a[1]="checked=\"checked\""
		elif hostel=="gh":
			a[2]="checked=\"checked\""
		elif hostel=="obheb":
			a[3]="checked=\"checked\""
		elif hostel=="obhdb":
			a[4]="checked=\"checked\""
		elif hostel=="gheb":
			a[5]="checked=\"checked\""
		return"""
		<html>
		<head>
		<link rel="stylesheet" type="text/css" href="http://localhost/project/style.css">
		</head>
		<body bgcolor="skyblue">
		<center>
		<div id="container">
		<div id="main">
		<font color=red size=5 >	The email-id already exists! Please enter another email-id </font><br><br><br>
		<font color=darkgreen>Creating new Account for postal management portal<br><br>All the fields are compulsory</font>
		</div>
		<div id="gap">
		<table border=0 cellpadding=8>
		<form action='account' method='post'>
		<tr><td>
		Enter Name</td><td>
		<input type='text' name='name' value='%s'>
		</tr>
		<tr><td>
		Enter RoomNo</td><td>
		<input type='text' name='roomno' value='%s'>
		</tr>
		<tr><td>
		Enter Hostel</td><td>
		OBH: 
		<input type="radio" name="hostel" value="obh" '%s'>
		NBH: 
		<input type="radio" name="hostel" value="nbh" '%s'>
		GH: 
		<input type="radio" name="hostel" value="gh" '%s'>
		OBH-EB: 
		<input type="radio" name="hostel" value="obheb" '%s'>
		OBH-DB: 
		<input type="radio" name="hostel" value="obhdb" '%s'>
		GHEB: 
		<input type="radio" name="hostel" value="gheb" '%s'>
		</td>
		</tr>
		<tr><td>
		Enter RollNo</td><td>
		<input type='text' name='rollno' value='%d'>
		</tr>
		<tr><td>
		Enter emailId</td><td>
		<input type='text' name='loginid'>
		</tr>
		<tr><td>
		Type a Password</td><td>
		<input type='password' name='pswd'>
		</tr>
		<tr><td>
		Retype the Password</td><td>
		<input type='password' name='pswd1'>
		</tr>
		</table>
		</div>
		<div id="main1">
		create account 
		<input type='submit' name='signup' value='SignUp'><br>
		<a href="../project.py/login">Login Page</a>
		</div>
		</center>
		</body>
		</html>
			"""%(name,roomno,a[0],a[1],a[2],a[3],a[4],a[5],int(rollno))
	redirect(req,'login')
      else:
	      redirect(req,"acntpage")
def security(req,name="",roomno="",hostel="",type="",fromaddr="",date="",courid="",press="",testinput="",testinput1="",key="",taken=""):
      s1=Session.Session(req);
      to=""
      req.content_type="text/html\n"
      #f=testinput.split("-")
      #t=testinput1.split("-")
      if s1.is_new()!=1:
	if press=='Submit' :
	     if name!="" and roomno!="" and fromaddr!="" and date!="":
		curs.execute("select count(*) from courier")
		l=curs.fetchone();
		j=int(l[0])+1
		q=req.form.getlist("hostel")
		curs.execute("insert into courier(courierid,name,roomno,hostel,type,fromaddr,date_arrvd) values('%d','%s','%s','%s','%s','%s','%s')"%(j,name,roomno,q[0],type,fromaddr,date));
		curs.execute("select email from courier,account where account.roomno='%s' and account.hostel='%s'"%(roomno,hostel))
		to=curs.fetchone();
     		if to!=None:
			addr_from = "couriers@iiit.ac.in"
			addr_to =to
			server=smtplib.SMTP('192.168.36.200')
			msg = ("From: %s\r\nTo: %s\r\n\r\n"% (addr_from, addr_to))
			msg = msg + "Hi, A courier with name %s ,room number %s and %s hostel is received at the main building. The courier ID is %d. Please collect it from the main building"%(name,roomno,hostel,j)
			server.sendmail(addr_from, addr_to, msg)
			server.quit()
		redirect(req,"secpage")
	     else:
	     	redirect(req,"secpage")
	elif press=='logout':
		s1.delete();
     		redirect(req,"seclogin");
	elif press=='search' or (press=='find' and key==""):
	     	#frd=f[0]+f[1]+f[2];
       	     	#tod=tyear+tmonth+tday;
	    	j=req.form.getlist("taken")
	    	z="yes"
	     	x="no"
    	     	if j[0]=="all":
			curs.execute("select * from courier where date_arrvd >= '%s' and date_arrvd <= '%s'"%(testinput,testinput1));
	     	elif j[0]=="taken":	
			curs.execute("select * from courier where date_arrvd >= '%s' and date_arrvd <= '%s' and recvd='%s'"%(testinput,testinput1,z));
	     	elif j[0]=="nottaken":	
			curs.execute("select * from courier where date_arrvd >= '%s' and date_arrvd <= '%s' and recvd='%s'"%(testinput,testinput1,x));
		q="""
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<script language="JavaScript" src="http://localhost/ITWS3_group13project/greenliving/calendar_db.js"></script>
		<link rel="stylesheet" href="http://localhost/ITWS3_group13project/greenliving/calendar.css">
		<title>IIIT Postal Management System</title>	
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" type="text/css" href="http://localhost/greenliving/style.css" media="screen" />
		</head>
		<body>
		<div id="wrap">
		<div id="header">
		<center>
		<br><br><h4>Couriers made easy!!</h4>
		<img src="http://localhost/greenliving/tree.jpg" >
		<img src="http://localhost/greenliving/IIIT.jpg" >
		</center>
		</div>
		<div id="content">
		<div id="left">
		<center>
		<font color="green" size=4>The Couriers in the selected dates</font><br><br>
		<table width="80%%" border="1">
		<tr>
		<th>C-Id</th><th>Name</th><th>RoomNo</th><th>Hostel</th><th>Type</th><th>From</th><th>Date</th><th>Taken Or Not</th><th>Receiver</th>
		</tr>
		"""
		#req.write(q);
		while(1):
			s=curs.fetchone();
			if s==None:
				break;
			q+="""
			<tr>
			<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>
			<tr>
			""" %(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8])
			#req.write(p);
		q+="""
		</table>
		<br><br><br>
		<a href="../project.py/secpage">Click to go to mainpage</a>
		</center>
		</div>
		<div id="right">
		<center>
		<form action='security' method='post' >
		<input type='submit' name='press' value='logout'>
		</form><br>
		Search Couriers<br>
		<form name="testform" action='security' method="post">
		from :
		<input type="text" name="testinput" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput'
				});
		</script>
		<br><p></p>
		&nbsp;&nbsp;&nbsp;&nbsp;to :
		<input type="text" name="testinput1" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput1'
				});
		</script>
		<br><br>
		All: 
		<input type="radio" name="taken" value="all" checked="checked">
		Taken: 
		<input type="radio" name="taken" value="taken" >
		NotTaken: 
		<input type="radio" name="taken" value="nottaken" ><br>
		<input type="submit" name="press" value="search">
		</form><br><br>
		<form action="security" method="post">
		Search by name
		<input size="15" type="text" name="key">
		<input type="submit" name="press" value="find">
		</form><br>
		<form action="security" method='post'>
		Enter courierId to edit details<br>
		<input size="5" type='text' name="courid">&nbsp;&nbsp;&nbsp;
		<input type="submit" name="press" value='edit'>
		</form>
		</center>
		</div>
		<div style="clear:both;"> </div>
		</div>
		<div id="bottom"> </div>
		<div id="footer">
		&copy; Copyright by <a href="http://www.iiit.ac.in">IIIT-Hyderabad</a> | Design by <a href="http://web.iiit.ac.in/~hanumanth">Kumar</a>
		</div>
		</div>
		</body>
		</html>"""
		req.write(q);
	elif press=='find':
	      if key!="":
		curs.execute("select * from courier where name regexp '%s'"%(key));
		q="""
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<script language="JavaScript" src="http://localhost/ITWS3_group13project/greenliving/calendar_db.js"></script>
		<link rel="stylesheet" href="http://localhost/ITWS3_group13project/greenliving/calendar.css">
		<title>IIIT Postal Management System</title>	
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" type="text/css" href="http://localhost/greenliving/style.css" media="screen" />
		</head>
		<body>
		<div id="wrap">
		<div id="header">
		<center>
		<br><br><h4>Couriers made easy!!</h4>
		<img src="http://localhost/greenliving/tree.jpg" >
		<img src="http://localhost/greenliving/IIIT.jpg" >
		</center>
		</div>
		<div id="content">
		<div id="left">
		<center>
		<center>
		<font color="green" size=4>The Couriers for the keyword <font color=red>'%s'</font> are listed below</font><br><br>
		<table width="80%%" border="1">
		<tr>
		<th>C-Id</th><th>Name</th><th>RoomNo</th><th>Hostel</th><th>Type</th><th>From</th><th>Date</th><th>Taken Or Not</th><th>Receiver</th>
		</tr>
		"""%(key)
		#req.write(q);
		while(1):
			s=curs.fetchone();
			if s==None:
				break;
			q+="""
			<tr>
			<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>
			<tr>
			""" %(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8])
			#req.write(p);
		q+="""
		</table>
		<br><br><br>
		<a href="../project.py/secpage">Click to go to mainpage</a>
		</div>
		<div id="right">
		<center>
		<form action='security' method='post' >
		<input type='submit' name='press' value='logout'>
		</form><br>
		Search Couriers<br>
		<form name="testform" action='security' method="post">
		from :
		<input type="text" name="testinput" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput'
				});
		</script>
		<br><p></p>
		&nbsp;&nbsp;&nbsp;&nbsp;to :
		<input type="text" name="testinput1" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput1'
				});
		</script>
		<br><br>
		All: 
		<input type="radio" name="taken" value="all" checked="checked">
		Taken: 
		<input type="radio" name="taken" value="taken" >
		NotTaken: 
		<input type="radio" name="taken" value="nottaken" ><br>
		<input type="submit" name="press" value="search">
		</form><br><br>
		<form action="security" method="post">
		Search by name
		<input size="15" type="text" name="key">
		<input type="submit" name="press" value="find">
		</form><br>
		<form action="security" method='post'>
		Enter courierId to edit details<br>
		<input size="5" type='text' name="courid">&nbsp;&nbsp;&nbsp;
		<input type="submit" name="press" value='edit'>
		</form>
		</center>
		</div>
		<div style="clear:both;"> </div>
		</div>
		<div id="bottom"> </div>
		<div id="footer">
		&copy; Copyright by <a href="http://www.iiit.ac.in">IIIT-Hyderabad</a> | Design by <a href="http://web.iiit.ac.in/~hanumanth">Kumar</a>
		</div>
		</div>
		</body>
		</html>"""
		req.write(q);
	else:
	     if courid!="":	
		curs.execute("select * from courier where courierid='%d'" %(int(courid)))
		r=curs.fetchone();
		if r==None:
			req.write("""
			<html>
			<body color=skyblue>
			<body bgcolor="skyblue">
			<center>
			No Such CourierId Exists!<br><br><br>
			<a href="../project.py/secpage">Click to go to mainpage</a>
			</center>
			</body>
			</html>""")
		else:	
			a=["","","","","",""]
			if r[3]=="obh":
				a[0]="checked=\"checked\""
			elif r[3]=="nbh":
				a[1]="checked=\"checked\""
			elif r[3]=="gh":
				a[2]="checked=\"checked\""
			elif r[3]=="obheb":
				a[3]="checked=\"checked\""
			elif r[3]=="obhdb":
				a[4]="checked=\"checked\""
			elif r[3]=="gheb":
				a[5]="checked=\"checked\""
			b=["",""]
			if r[7]=="yes":
				b[0]="checked=\"checked\""
			if r[7]=="no":
				b[1]="checked=\"checked\""
			req.write("""
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<script language="JavaScript" src="http://localhost/ITWS3_group13project/greenliving/calendar_db.js"></script>
		<link rel="stylesheet" href="http://localhost/ITWS3_group13project/greenliving/calendar.css">
		<title>IIIT Postal Management System</title>	
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" type="text/css" href="http://localhost/greenliving/style.css" media="screen" />
		</head>
		<body>
		<div id="wrap">
		<div id="header">
		<center>
		<br><br><h4>Couriers made easy!!</h4>
		<img src="http://localhost/greenliving/tree.jpg" >
		<img src="http://localhost/greenliving/IIIT.jpg" >
		</center>
		</div>
		<div id="content">
		<div id="left">
		<center>
			<h3>Edit the courier Information</h3>
			<br>
			<table border=0 >
			<form action='edit1' method='post'>
			<tr><td>
			<input type="hidden" name="courid" value="%s">
			</td></tr>
			<tr><td>
			Enter Name<br></td><td>
			<input type='text' name='name' value='%s'></td>
			</tr>
			<tr><td>
			Enter RoomNo<br></td><td>
			<input type='text' name='roomno' value='%s'></td>
			</tr>
			<tr><td>
			Select Hostel<br></td><td>
			OBH: 
			<input type="radio" name="hostel" value="obh" "%s">
			NBH: 
			<input type="radio" name="hostel" value="nbh" "%s">
			GH: 
			<input type="radio" name="hostel" value="gh" "%s">
			OBH-EB: 
			<input type="radio" name="hostel" value="obheb" "%s">
			OBH-DB: 
			<input type="radio" name="hostel" value="obhdb" "%s">
		GHEB: 
		<input type="radio" name="hostel" value="gheb" '%s'>
			</td>
			</tr>
			<tr><td>
			Enter Type of Courier<br></td><td>
			<input type='text' name='type' value='%s'></td>
			</tr>
			<tr><td>
			Enter From Address<br></td><td>
			<input type='text' name='fromaddr' value='%s'></td>
			</tr>
			<tr><td>
			Enter Date Of Arrival(YYYY-MM-DD)<br></td><td>
			<input type='text' name='date' value='%s'></td>
			</tr>
			<tr><td>
			Is courier taken?<br>
			</td><td>
			Yes:
			<input type="radio" name="taken" value="yes" "%s">
			No:
			<input type="radio" name="taken" value="no" "%s">
			</td></tr>
			<tr><td>
			Receiver's name and rollNo<br></td><td>
			<input type='text' name='receiver' value='%s'></td>
			</tr>
			</table>
			<br><br>
			<input type='submit' name='press' value='submit'>
			</center><br>
			<a href="../project.py/secpage"><font color=red >click here to go back</font></a><br>
			</form>
			</div>
		<div id="right">
		<center>
		<form action='security' method='post' >
		<input type='submit' name='press' value='logout'>
		</form><br>
		Search Couriers<br>
		<form name="testform" action='security' method="post">
		from :
		<input type="text" name="testinput" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput'
				});
		</script>
		<br><p></p>
		&nbsp;&nbsp;&nbsp;&nbsp;to :
		<input type="text" name="testinput1" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput1'
				});
		</script>
		<br><br>
		All: 
		<input type="radio" name="taken" value="all" checked="checked">
		Taken: 
		<input type="radio" name="taken" value="taken" >
		NotTaken: 
		<input type="radio" name="taken" value="nottaken" ><br>
		<input type="submit" name="press" value="search">
		</form><br><br>
		<form action="security" method="post">
		Search by name
		<input size="15" type="text" name="key">
		<input type="submit" name="press" value="find">
		</form><br>
		<form action="security" method='post'>
		Enter courierId to edit details<br>
		<input size="5" type='text' name="courid">&nbsp;&nbsp;&nbsp;
		<input type="submit" name="press" value='edit'>
		</form>
		</center>
		</div>
		<div style="clear:both;"> </div>
		</div>
		<div id="bottom"> </div>
		<div id="footer">
		&copy; Copyright by <a href="http://www.iiit.ac.in">IIIT-Hyderabad</a> | Design by <a href="http://web.iiit.ac.in/~hanumanth">Kumar</a>
		</div>
		</div>
			</body></html>""" %(r[0],r[1],r[2],a[0],a[1],a[2],a[3],a[4],a[5],r[4],r[5],r[6],b[0],b[1],r[8]))
			
	     else:
		redirect(req,"secpage");
      else:
      		redirect(req,"seclogin");

def edit1(req,courid=0,name="",roomno="",hostel="",type="",fromaddr="",date="",receiver=""):
      s1=Session.Session(req);
      if s1.is_new()!=1:
	w=req.form.getlist("taken");
	h=req.form.getlist("hostel");
	curs.execute("update courier set name='%s', roomno='%s', hostel='%s', type='%s', fromaddr='%s', date_arrvd='%s', recvd='%s', receiver='%s' where courierid='%s'"%(name,roomno,h[0],type,fromaddr,date,w[0],receiver,courid))
        redirect(req,"secpage");
      else:
      	redirect(req,"seclogin")
def edit2(req,name="",roomno="",hostel="",rollno="",loginid=""):
      se=Session.Session(req);
      if se.is_new()!=1:
	h=req.form.getlist("hostel");
	curs.execute("update account set name='%s', roomno='%s', hostel='%s', rollno='%s', email='%s' where email='%s'"%(name,roomno,h[0],rollno,loginid,se['user']))
	se['user']=loginid
	redirect(req,"home")
      else:
      	redirect(req,"login")
def seclogin(req):
	return """
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<title>IIIT Postal Management System</title>	
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" type="text/css" href="http://localhost/greenliving/style.css" media="screen" />
		</head>
		<body>
		<div id="wrap">
		<div id="header">
		<center>
		<br><br><h4>Couriers made easy!!</h4>
		<img src="http://localhost/greenliving/tree.jpg" >
		<img src="http://localhost/greenliving/IIIT.jpg" >
		</center>
		</div>
		<div id="content">
		<div id="left">
		<center>
	<font size="5">Welcome To Postal Management Portal</font><br><br><br>
	<form action='mainpage1' method='post'>
	Username
	<input type='text' name='user' ><br><br>
	Password
	<input type='password' name='pswd' ><br><br>
	<input type='submit' name='press' value='login'><br><br>
		</div>
		</center>
		<div id="right"> 
		<h3>Couriers</h3>
		<ul>
		<p>
		<img src="http://localhost/greenliving/security1.jpg">
		</p>
		</ul>
		</div>
		<div style="clear:both;"> </div>
		</div>
		<div id="bottom"> </div>
		<div id="footer">
		&copy; Copyright by <a href="http://www.iiit.ac.in">IIIT-Hyderabad</a> | Design by <a href="http://web.iiit.ac.in/~hanumanth">Kumar</a>
		</div>

		</div>
		</body>
		</html>"""
def mainpage1(req,user="",pswd=""):
	d=sha.new(pswd)
	q=d.hexdigest()
	req.content_type="text/html\n"
	if user=="security" and q=="a80ab8297c253117a00c428adae954c8f8e4b6ac":
		s1=Session.Session(req);
		s1.save();
		redirect(req,"secpage");
	else:
		a="""<html>
			<body bgcolor=skyblue>
			sorry, wrong username or password
			<a href="../project.py/seclogin">Click here to go back to login page!</a>
			</body>
			</html>
			"""
		req.write(a);		

def login(req):
		return """
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<title>IIIT Postal Management System</title>	
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" type="text/css" href="http://localhost/greenliving/style.css" media="screen" />
		</head>
		<body>
		<div id="wrap">
		<div id="header">
		<center>
		<br><br><h4>Couriers made easy!!</h4>
		<img src="http://localhost/greenliving/tree.jpg" >
		<img src="http://localhost/greenliving/IIIT.jpg" >
		</center>
		</div>
		<div id="content">
		<div id="left">
		<center>
		login with e-mailId and password you provided when you created account <br><br>
		<table border=0 cellpadding=8>
		<form action='mainpage' method='post'>
		<tr><td>
		EmailId </td><td>
		<input type='text' name='user' >
		</td></tr>
		<tr><td>
		Password</td><td>
		<input type='password' name='pswd' ></td></tr>
		</table><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		<input type='submit' name='press' value='login'><br><br>
		New User? SignUp Now!
		<input type='submit' name='press' value='signup'><br><br>
		</form>
		</center>
		</div>
		<div id="right"> 
		<h3>Couriers</h3>
		<ul>
		<p>
		<img src="http://localhost/greenliving/image1.jpg">
		</p>
		</ul>
		</div>
		<div style="clear:both;"> </div>
		</div>
		<div id="bottom"> </div>
		<div id="footer">
		&copy; Copyright by <a href="http://www.iiit.ac.in">IIIT-Hyderabad</a> | Design by <a href="http://web.iiit.ac.in/~hanumanth">Kumar</a>
		</div>

		</div>
		</body>
		</html>"""

def process(req,press="",testinput="",testinput1=""):
      	req.content_type="text/html\n"
	se=Session.Session(req);
	if se.is_new()!=1 :
		if press=="Logout":
			se.delete();
			redirect(req,"login");
		elif press=="Edit":
			curs.execute("select * from account where email='%s'"%(se['user']))
			d=curs.fetchone();
			if d!=None:
				a=["","","","","",""]
				if d[2]=="obh":
					a[0]="checked=\"checked\""
				elif d[2]=="nbh":
					a[1]="checked=\"checked\""
				elif d[2]=="gh":
					a[2]="checked=\"checked\""
				elif d[2]=="obheb":
					a[3]="checked=\"checked\""
				elif d[2]=="obhdb":
					a[4]="checked=\"checked\""
				elif d[2]=="gheb":
					a[5]="checked=\"checked\""
				return """
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<script language="JavaScript" src="http://localhost/ITWS3_group13project/greenliving/calendar_db.js"></script>
		<link rel="stylesheet" href="http://localhost/ITWS3_group13project/greenliving/calendar.css">
		<title>IIIT Postal Management System</title>	
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" type="text/css" href="http://localhost/greenliving/style.css" media="screen" />
		</head>
		<body>
		<div id="wrap">
		<div id="header">
		<center>
		<br><br><h4>Couriers made easy!!</h4>
		<img src="http://localhost/greenliving/tree.jpg" >
		<img src="http://localhost/greenliving/IIIT.jpg" >
		</center>
		</div>
		<div id="content">
		<div id="left">

			<h3>Edit your Profile</h3>
			<table border=0>
			<form action='edit2' method='post'>
			<tr><td>
			Enter Name</td><td>
			<input type='text' name='name' value='%s'><br><br>
			</tr>
			<tr><td>
			Enter RoomNo</td><td>
			<input type='text' name='roomno' value='%s'><br><br>
			</tr>
			<tr><td>
			Enter Hostel</td><td>
			OBH: 
			<input type="radio" name="hostel" value="obh" "%s">
			NBH: 
			<input type="radio" name="hostel" value="nbh" "%s">
			GH: 
			<input type="radio" name="hostel" value="gh" "%s">
			OBH-EB: 
			<input type="radio" name="hostel" value="obheb" "%s">
			OBH-DB: 
			<input type="radio" name="hostel" value="obhdb" "%s">
		GHEB: 
		<input type="radio" name="hostel" value="gheb" "%s">
			</td>
			</tr>
			<tr><td>
			Enter RollNo</td><td>
			<input type='text' name='rollno' value='%d'><br><br>
			</tr>
			<tr><td>
			Enter emailId</td><td>
			<input type='text' name='loginid' value='%s'><br><br>
			</td></tr>
			</table><br>
			<input type='submit' name='Update' value='Update'><br><br>
			<a href="../project.py/home">Click to go to home</a> 
		
		</div>
		<div id="right"> 
		<h3>Options</h3>
		<ul>
			<form action='process' method='post' >
			<input type='submit' name='press' value='Logout' class='button'><br><br>
			<input type='submit' name='press' value='Edit' class='button'><br><br>
			<input type='submit' name='press' value='ChangePassword' class='button'><br><br>
		<form name="testform" action='security' method="post">
		from :
		<input type="text" name="testinput" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput'
				});
		</script>
		<br><p></p>
		&nbsp;&nbsp;&nbsp;&nbsp;to :
		<input type="text" name="testinput1" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput1'
				});
		</script>
		<br><br>
			<input type='submit' name='press' value='Search' class='button'><br>
			</form>
		</ul>
		</div>
		<div style="clear:both;"> </div>
		</div>
		<div id="bottom"> </div>
		<div id="footer">
		&copy; Copyright by <a href="http://www.iiit.ac.in">IIIT-Hyderabad</a> | Design by <a href="http://web.iiit.ac.in/~hanumanth">Kumar</a>
		</div>
		</div>
			</center>
			</body>
			</html>"""%(d[0],d[1],a[0],a[1],a[2],a[3],a[4],a[5],int(d[3]),d[4])
		elif press=="Search":
			#frd=fyear+fmonth+fday;
			#tod=tyear+tmonth+tday;
			curs.execute("select * from courier where date_arrvd >= '%s' and date_arrvd <= '%s'"%(testinput,testinput1));
			q="""
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<script language="JavaScript" src="http://localhost/ITWS3_group13project/greenliving/calendar_db.js"></script>
		<link rel="stylesheet" href="http://localhost/ITWS3_group13project/greenliving/calendar.css">
		<title>IIIT Postal Management System</title>	
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" type="text/css" href="http://localhost/greenliving/style.css" media="screen" />
		</head>
		<body>
		<div id="wrap">
		<div id="header">
		<center>
		<br><br><h4>Couriers made easy!!</h4>
		<img src="http://localhost/greenliving/tree.jpg" >
		<img src="http://localhost/greenliving/IIIT.jpg" >
		</center>
		</div>
		<div id="content">
		<div id="left">
			<center>
			<h3>The Courier Information between the Selected dates</h3>
			<table width="80%%" border="1">
			<tr>
		<th>C-Id</th><th>Name</th><th>RoomNo</th><th>Hostel</th><th>Type</th><th>From</th><th>Date</th><th>Taken Or Not</th><th>Receiver</th>
				</tr>
			"""
		#	req.write(q);
			while(1):
				s=curs.fetchone();
				if s==None:
					break;
				q+="""
				<tr>
				<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>
				<tr>
				""" %(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8])
				#req.write(p);
			q+="""
			</table>
			<br><br>
			<a href="../project.py/home">Click to go to home</a>
			</center>
		</div>
		<div id="right"> 
		<h3>Options</h3>
		<ul>
			<form name="testform" action='process' method='post' >
			<input type='submit' name='press' value='Logout' class='button'><br><br>
			<input type='submit' name='press' value='Edit' class='button'><br><br>
			<input type='submit' name='press' value='ChangePassword' class='button'><br><br>
		from :
		<input type="text" name="testinput" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput'
				});
		</script>
		<br><p></p>
		&nbsp;&nbsp;&nbsp;&nbsp;to :
		<input type="text" name="testinput1" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput1'
				});
		</script>
		<br><br>
			<input type='submit' name='press' value='Search' class='button'><br>
			</form>
		</ul>
		</div>
		<div style="clear:both;"> </div>
		</div>
		<div id="bottom"> </div>
		<div id="footer">
		&copy; Copyright by <a href="http://www.iiit.ac.in">IIIT-Hyderabad</a> | Design by <a href="http://web.iiit.ac.in/~hanumanth">Kumar</a>
		</div>
		</div>
			</center>
			</body>
			</html>"""
			req.write(q);
		elif press=="ChangePassword":
			redirect(req,"chpasswd");
	else:
		redirect(req,"login")
def chpasswd(req):			
		se=Session.Session(req)
		if se.is_new()!=1:
			return """
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<script language="JavaScript" src="http://localhost/ITWS3_group13project/greenliving/calendar_db.js"></script>
		<link rel="stylesheet" href="http://localhost/ITWS3_group13project/greenliving/calendar.css">
		<title>IIIT Postal Management System</title>	
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" type="text/css" href="http://localhost/greenliving/style.css" media="screen" />
		</head>
		<body>
		<div id="wrap">
		<div id="header">
		<center>
		<br><br><h4>Couriers made easy!!</h4>
		<img src="http://localhost/greenliving/tree.jpg" >
		<img src="http://localhost/greenliving/IIIT.jpg" >
		</center>
		</div>
		<div id="content">
		<div id="left">
			<center>
			<br><h3>Changing password</h3><br>
			<table border=0 cellpadding=10>
			<form action="paswd" method="post">
			<tr><td>
			Type Current Password: </td>
			<td><input type="password" name="curpas" >
			</td></tr>
			<tr><td>
			Choose New Password: </td>
			<td><input type="password" name="newpas" >
			</td></tr>
			<tr><td>
			Retype New Password: </td>
			<td><input type="password" name="newpas1" >
			</td></tr>
			</table>
			<input type="submit" name="submit" value="submit">
			</form>
			<br>
			<br>
			<a href="../project.py/home">Click to go home</a>
			</center>
		</div>
		<div id="right"> 
		<h3>Options</h3>
		<ul>
			<form name="testform" action='process' method='post' >
			<input type='submit' name='press' value='Logout' class='button'><br><br>
			<input type='submit' name='press' value='Edit' class='button'><br><br>
			<input type='submit' name='press' value='ChangePassword' class='button'><br><br>
		from :
		<input type="text" name="testinput" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput'
				});
		</script>
		<br><p></p>
		&nbsp;&nbsp;&nbsp;&nbsp;to :
		<input type="text" name="testinput1" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput1'
				});
		</script>
		<br><br>
			<input type='submit' name='press' value='Search' class='button'><br>
			</form>
		</ul>
		</div>
		<div style="clear:both;"> </div>
		</div>
		<div id="bottom"> </div>
		<div id="footer">
		&copy; Copyright by <a href="http://www.iiit.ac.in">IIIT-Hyderabad</a> | Design by <a href="http://web.iiit.ac.in/~hanumanth">Kumar</a>
		</div>
		</div>
			</center>
			</body>
			</html>"""
		else:
			redirect(req,"login")

def paswd(req,curpas="",newpas="",newpas1=""):
	se=Session.Session(req);
	if se.is_new()!=1:
		curs.execute("select passwd from account where email='%s'"%(se['user']))
		a=curs.fetchone();
		c=sha.new(curpas);
		o=c.hexdigest();
		if o!=a[0]:
			return"""	
			<html>
			<body bgcolor="skyblue">
			<center><br><br>Incorrect Password<br><br>
			<a href="../project.py/chpasswd">Click to go back!</a>
			<br><br>
			<a href="../project.py/home">Click to go home!</a>
			</center></body></html>"""
		else:
			p,q=sha.new(newpas),sha.new(newpas1);
			if p.hexdigest()!=q.hexdigest():
				return """
				<html>
				<body bgcolor="skyblue">
				<center><br><br>Newpasswords did not match<br><br>
				<a href="../project.py/chpasswd">Click to go back!</a>
				<br><br>
				<a href="../project.py/home">Click to go home!</a>
				</center></body></html>"""
			else:
			 	curs.execute("update account set passwd='%s' where passwd='%s'"%(p.hexdigest(),o))
				return"""
			 	<html>
				<body bgcolor="skyblue">
				<center><br><br>password was successfully changed<br>
				<br><br>
				<a href="../project.py/home">Click to go home!</a>
				</center></body></html>"""
	else:
	   redirect(req,"login");
	
def home(req):
		se=Session.Session(req)
		req.content_type="text/html\n"
		if se.is_new()!=1:
			curs.execute("select * from courier,account where account.email='%s' and account.roomno=courier.roomno and account.hostel=courier.hostel"%(se['user']));
			q="""
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<script language="JavaScript" src="http://localhost/ITWS3_group13project/greenliving/calendar_db.js"></script>
		<link rel="stylesheet" href="http://localhost/ITWS3_group13project/greenliving/calendar.css">
		<title>IIIT Postal Management System</title>	
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" type="text/css" href="http://localhost/greenliving/style.css" media="screen" />
		</head>
		<body>
		<div id="wrap">
		<div id="header">
		<center>
		<br><br><h4>Couriers made easy!!</h4>
		<img src="http://localhost/greenliving/tree.jpg" >
		<img src="http://localhost/greenliving/IIIT.jpg" >
		</center>
		</div>
		<div id="content">
		<div id="left">
			<h2>Your Courier Information is shown below</h2><br>
			<table border="1" > 
			<tr>
		<th>C-Id</th><th>Name</th><th>RoomNo</th><th>Hostel</th><th>Type</th><th>From</th><th>Date</th><th>Taken Or Not</th><th>Receiver</th>
				</tr>
			"""
			req.write(q);
			c=0;
			r=0;
			while(1):
				s=curs.fetchone();
				if s==None:
					break;
				if s[7]=="yes":
					r=r+1;
				c=c+1;	
				p="""
				<tr>
				<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>
				</tr>
				""" %(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8])
				req.write(p);
			w="""
			</table><br><br>
			<h4>You have collected <font color='green' size=5>%s</font> couriers of <font color='red' size=5>%s</font> total couriers received</h4>
		</div>
		<div id="right"> 
		<h3>Options</h3>
		<ul>
			<form name="testform" action='process' method='post' >
			<input type='submit' name='press' value='Logout' class='button'><br><br>
			<input type='submit' name='press' value='Edit' class='button'><br><br>
			<input type='submit' name='press' value='ChangePassword' class='button'><br><br>
		from :
		<input type="text" name="testinput" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput'
				});
		</script>
		<br><p></p>
		&nbsp;&nbsp;&nbsp;&nbsp;to :
		<input type="text" name="testinput1" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput1'
				});
		</script>
		<br><br>
			<input type='submit' name='press' value='Search' class='button'><br>
			</form>
		</div>
		<div style="clear:both;"> </div>
		</div>
		<div id="bottom"> </div>
		<div id="footer">
		&copy; Copyright by <a href="http://www.iiit.ac.in">IIIT-Hyderabad</a> | Design by <a href="http://web.iiit.ac.in/~hanumanth">Kumar</a>
		</div>
		</div>
			</html>"""%(r,c)
			req.write(w);
		else:
			redirect(req,"login");

def mainpage(req,user="",pswd="",press=""):
      if press=="login":	
	req.content_type="text/html\n"
	curs.execute("select passwd from account where email='%s'" %(user));
	s=curs.fetchone();
	if s!=None:
		w=sha.new(pswd);
		u=w.hexdigest();
		if u!=s[0]:
			return"""	
			<html>
			<body bgcolor="skyblue">
			<center><br><br>Incorrect Password<br><br>
			<a href="../project.py/login">Click to go back!</a>
			<br><br>
			</center></body></html>"""
			#redirect(req,"login");
		else:
			se=Session.Session(req);
			se['user']=user;
			se.save();
			redirect(req,"home")
	else :
			return"""	
			<html>
			<body bgcolor="skyblue">
			<center><br><br>Invalid E-mail Id<br><br>
			<a href="../project.py/login">Click to go back!</a>
			<br><br>
			</center></body></html>"""
		#redirect(req,"login");
      elif press=="signup":
      		redirect(req,"acntpage");
      else:
      		redirect(req,"login");

def acntpage(req):	
		return """
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<title>IIIT Postal Management System</title>	
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" type="text/css" href="http://localhost/greenliving/style.css" media="screen" />
		</head>
		<body>
		<div id="wrap">
		<div id="header">
		<center>
		<br><br><h4>Couriers made easy!!</h4>
		<img src="http://localhost/greenliving/tree.jpg" >
		<img src="http://localhost/greenliving/IIIT.jpg" >
		</center>
		</div>
		<div id="content">
		<div id="left">
		<center>
		<font color=darkgreen>Creating new Account for postal management portal<br><br>All the fields are compulsory</font>
		<br><br><table border=0 cellpadding=10>
		<form action='account' method='post'>
		<tr><td>
		Enter Name</td><td>
		<input type='text' name='name'>
		</tr>
		<tr><td>
		Enter RoomNo</td><td>
		<input type='text' name='roomno'>
		</tr>
		<tr><td>
		Enter Hostel</td><td>
		OBH: 
		<input type="radio" name="hostel" value="obh" checked="checked">
		NBH: 
		<input type="radio" name="hostel" value="nbh" >
		GH: 
		<input type="radio" name="hostel" value="gh" >
		OBH-EB: 
		<input type="radio" name="hostel" value="obheb" >
		OBH-DB: 
		<input type="radio" name="hostel" value="obhdb" >
		GHEB: 
		<input type="radio" name="hostel" value="gheb" >
		</td>
		</tr>
		<tr><td>
		Enter RollNo</td><td>
		<input type='text' name='rollno'>
		</tr>
		<tr><td>
		Enter emailId</td><td>
		<input type='text' name='loginid'>
		</tr>
		<tr><td>
		Type a Password</td><td>
		<input type='password' name='pswd'>
		</tr>
		<tr><td>
		Retype the Password</td><td>
		<input type='password' name='pswd1'>
		</tr>
		</table><br>
		create account 
		<input type='submit' name='signup' value='SignUp'><br><br>
		<a href="../project.py/login">Login Page</a>
		</center>
		</div>
		<div id="right">
		<h3>Couriers</h3>
		<ul>
		<p>
		<img src="http://localhost/greenliving/image1.jpg" >
		</p>
		</ul>
		</div>
		<div style="clear:both;"> </div>
		</div>
		<div id="bottom"> </div>
		<div id="footer">
		&copy; Copyright by <a href="http://www.iiit.ac.in">IIIT-Hyderabad</a> | Design by <a href="http://web.iiit.ac.in/~hanumanth">Kumar</a>
		</div>
		</div>
			</html>"""
def taken(req):
		s1=Session.Session(req);
		req.content_type="text/html\n"
		if s1.is_new()!=1:
			d="yes"
			curs.execute("select * from courier where recvd='%s'"%(d))
			q="""
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<script language="JavaScript" src="http://localhost/ITWS3_group13project/greenliving/calendar_db.js"></script>
		<link rel="stylesheet" href="http://localhost/ITWS3_group13project/greenliving/calendar.css">
		<title>IIIT Postal Management System</title>	
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" type="text/css" href="http://localhost/greenliving/style.css" media="screen" />
		</head>
		<body>
		<div id="wrap">
		<div id="header">
		<center>
		<br><br><h4>Couriers made easy!!</h4>
		<img src="http://localhost/greenliving/tree.jpg" >
		<img src="http://localhost/greenliving/IIIT.jpg" >
		</center>
		</div>
		<div id="content">
		<div id="left">
			<h2>Couriers taken are shown below</h2><br>
			<table border="1" > 
			<tr>
		<th>C-Id</th><th>Name</th><th>RoomNo</th><th>Hostel</th><th>Type</th><th>From</th><th>Date</th><th>Taken Or Not</th><th>Receiver</th>
				</tr>
			"""
			#req.write(q);
			while(1):
				s=curs.fetchone();
				if s==None:
					break;
				q+="""
				<tr>
				<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>
				</tr>
				""" %(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8])
				#req.write(q);
			q+="""
		</table>
		<br><br><br>
		<a href="../project.py/secpage">Click to go to mainpage</a>
		</center>
		</div>
		<div id="right">
		<center>
		<form action='security' method='post' >
		<input type='submit' name='press' value='logout'>
		</form><br>
		Search Couriers<br>
		<form name="testform" action='security' method="post">
		from :
		<input type="text" name="testinput" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput'
				});
		</script>
		<br><p></p>
		&nbsp;&nbsp;&nbsp;&nbsp;to :
		<input type="text" name="testinput1" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput1'
				});
		</script>
		<br><br>
		All: 
		<input type="radio" name="taken" value="all" checked="checked">
		Taken: 
		<input type="radio" name="taken" value="taken" >
		NotTaken: 
		<input type="radio" name="taken" value="nottaken" ><br>
		<input type="submit" name="press" value="search">
		</form><br><br>
		<form action="security" method="post">
		Search by name
		<input size="15" type="text" name="key">
		<input type="submit" name="press" value="find">
		</form><br>
		<form action="security" method='post'>
		Enter courierId to edit details<br>
		<input size="5" type='text' name="courid">&nbsp;&nbsp;&nbsp;
		<input type="submit" name="press" value='edit'>
		</form>
		</center>
		</div>
		<div style="clear:both;"> </div>
		</div>
		<div id="bottom"> </div>
		<div id="footer">
		&copy; Copyright by <a href="http://www.iiit.ac.in">IIIT-Hyderabad</a> | Design by <a href="http://web.iiit.ac.in/~hanumanth">Kumar</a>
		</div>
		</div>
		</body>
		</html>"""
			req.write(q);
		else:
			redirect(req,"seclogin");
def nottaken(req):
		s1=Session.Session(req);
		req.content_type="text/html\n"
		if s1.is_new()!=1:
			d="no"
			curs.execute("select * from courier where recvd='%s'"%(d))
			q="""
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<script language="JavaScript" src="http://localhost/ITWS3_group13project/greenliving/calendar_db.js"></script>
		<link rel="stylesheet" href="http://localhost/ITWS3_group13project/greenliving/calendar.css">
		<title>IIIT Postal Management System</title>	
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" type="text/css" href="http://localhost/greenliving/style.css" media="screen" />
		</head>
		<body>
		<div id="wrap">
		<div id="header">
		<center>
		<br><br><h4>Couriers made easy!!</h4>
		<img src="http://localhost/greenliving/tree.jpg" >
		<img src="http://localhost/greenliving/IIIT.jpg" >
		</center>
		</div>
		<div id="content">
		<div id="left">
			<h2>Couriers not yet taken are shown below</h2><br>
			<table border="1" > 
			<tr>
		<th>C-Id</th><th>Name</th><th>RoomNo</th><th>Hostel</th><th>Type</th><th>From</th><th>Date</th><th>Taken Or Not</th><th>Receiver</th>
				</tr>
			"""
			#req.write(q);
			while(1):
				s=curs.fetchone();
				if s==None:
					break;
				q+="""
				<tr>
				<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>
				</tr>
				""" %(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8])
				#req.write(q);
			q+="""
		</table>
		<br><br><br>
		<a href="../project.py/secpage">Click to go to mainpage</a>
		</center>
		</div>
		<div id="right">
		<center>
		<form action='security' method='post' >
		<input type='submit' name='press' value='logout'>
		</form><br>
		Search Couriers<br>
		<form name="testform" action='security' method="post">
		from :
		<input type="text" name="testinput" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput'
				});
		</script>
		<br><p></p>
		&nbsp;&nbsp;&nbsp;&nbsp;to :
		<input type="text" name="testinput1" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput1'
				});
		</script>
		<br><br>
		All: 
		<input type="radio" name="taken" value="all" checked="checked">
		Taken: 
		<input type="radio" name="taken" value="taken" >
		NotTaken: 
		<input type="radio" name="taken" value="nottaken" ><br>
		<input type="submit" name="press" value="search">
		</form><br><br>
		<form action="security" method="post">
		Search by name
		<input size="15" type="text" name="key">
		<input type="submit" name="press" value="find">
		</form><br>
		<form action="security" method='post'>
		Enter courierId to edit details<br>
		<input size="5" type='text' name="courid">&nbsp;&nbsp;&nbsp;
		<input type="submit" name="press" value='edit'>
		</form>
		</center>
		</div>
		<div style="clear:both;"> </div>
		</div>
		<div id="bottom"> </div>
		<div id="footer">
		&copy; Copyright by <a href="http://www.iiit.ac.in">IIIT-Hyderabad</a> | Design by <a href="http://web.iiit.ac.in/~hanumanth">Kumar</a>
		</div>
		</div>
		</body>
		</html>"""
			req.write(q);
		else:
			redirect(req,"seclogin");
def secpage(req):
	s1=Session.Session(req);
	if s1.is_new()!=1:
		curs.execute("select * from courier")
		c=0;
		r=0;
		while(1):
			s=curs.fetchone();
			if s==None:
				break;
			if s[7]=="yes":
				r=r+1;
			c=c+1;
			#now = time.localtime(time.time())
			#year, month, day, hour, minute, second, weekday, yearday, daylight = now
		return """
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<script language="JavaScript" src="http://localhost/ITWS3_group13project/greenliving/calendar_db.js"></script>
		<link rel="stylesheet" href="http://localhost/ITWS3_group13project/greenliving/calendar.css">
		<script type="text/javascript">
		<!--
		var currentTime = new Date()
		var month = currentTime.getMonth() + 1
			var day = currentTime.getDate()
		var year = currentTime.getFullYear()
		var finaldate = year + "-" + month + "-" + day
		//-->
		</script>
		<title>IIIT Postal Management System</title>	
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" type="text/css" href="http://localhost/greenliving/style.css" media="screen" />
		</head>
		<body>
		<div id="wrap">
		<div id="header">
		<center>
		<br><br><h4>Couriers made easy!!</h4>
		<img src="http://localhost/greenliving/tree.jpg" >
		<img src="http://localhost/greenliving/IIIT.jpg" >
		</center>
		</div>
		<div id="content">
		<div id="left">
		<center><br><br>
		<font size=5 color=green>Details of Courier</font>
		<table border=0>
		<form action='security' method='post'>
		<tr><td>
		Enter Name</td><td>
		<input type='text' name='name'>
		</tr>
		<tr><td>
		Enter RoomNo</td><td>
		<input type='text' name='roomno'>
		</tr>
		<tr><td>
		Enter Hostel</td><td>
		OBH: 
		<input type="radio" name="hostel" value="obh" checked="checked">
		NBH: 
		<input type="radio" name="hostel" value="nbh" >
		GH: 
		<input type="radio" name="hostel" value="gh" >
		OBH-EB: 
		<input type="radio" name="hostel" value="obheb" >
		OBH-DB: 
		<input type="radio" name="hostel" value="obhdb" >
		GHEB: 
		<input type="radio" name="hostel" value="gheb" >
		</td>
		</tr>
		<tr><td>
		Enter Type of Courier</td><td>
		<input type='text' name='type'></td>
		</tr>
		<tr><td>
		Enter From Address</td><td>
		<input type='text' name='fromaddr'></td>
		</tr>
		<tr><td>
		Date Of Arrival(YYYY-MM-DD)</td><td>
		<input type='text' name='date' ></td>
		</tr>
		<tr><td>
		<input type='submit' name='press' value='Submit'>
		</td></tr>
		</table>
		</form>
		<font color=green size=3>Total number of Couriers = <font color =blue >%d</font></font><br><br>
		<font color=green size=3>Number of Couriers that are taken = <a href="taken"><font color = black >%d</a></font></font><br><br>
		<font color=green size=3>Number of Couriers not yet taken = <a href="nottaken"><font color = red >%d</a></font></font><br><br>
		</div>
		<div id="right">
		<center>
		<form action='security' method='post' >
		<input type='submit' name='press' value='logout'>
		</form><br>
		Search Couriers<br>
		<form name="testform" action='security' method="post">
		from :
		<input type="text" name="testinput" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput'
				});
		</script>
		<br><p></p>
		&nbsp;&nbsp;&nbsp;&nbsp;to :
		<input type="text" name="testinput1" size="10"/>
		<script language="JavaScript">
		new tcal ({
				// form name
				'formname': 'testform',
				// input name
				'controlname': 'testinput1'
				});
		</script>
		<br><br>
		All: 
		<input type="radio" name="taken" value="all" checked="checked">
		Taken: 
		<input type="radio" name="taken" value="taken" >
		NotTaken: 
		<input type="radio" name="taken" value="nottaken" ><br>
		<input type="submit" name="press" value="search">
		</form><br><br>
		<form action="security" method="post">
		Search by name
		<input size="15" type="text" name="key">
		<input type="submit" name="press" value="find">
		</form><br>
		<form action="security" method='post'>
		Enter courierId to edit details<br>
		<input size="5" type='text' name="courid">&nbsp;&nbsp;&nbsp;
		<input type="submit" name="press" value='edit'>
		</form>
		</center>
		</div>
		<div style="clear:both;"> </div>
		</div>
		<div id="bottom"> </div>
		<div id="footer">
		&copy; Copyright by <a href="http://www.iiit.ac.in">IIIT-Hyderabad</a> | Design by <a href="http://web.iiit.ac.in/~hanumanth">Kumar</a>
		</div>
		</div>
		</body>
		</html>"""%(c,r,c-r)
	else:
		redirect(req,"seclogin");
