from flask import Flask, render_template, request, redirect, url_for
import mysql.connector as sql
from mysql.connector import errorcode

application = app = Flask(__name__)

@app.route('/')
def index():
	# MAIN PAGE OF APP - COINTAINS LINKS TO LOG-IN OR SIGN-UP
	return render_template("index.html") #return render_template('my-form.html')

@app.route("/signup")
def signup():
	# SIGN-UP PAGE - CONTAINS FIELDS TO CREATE USERNAME AND PASSWORD
	return render_template("signup.html")

@app.route("/signup", methods=['POST'])
def signup_post():
	# Obtain username and password
	user = request.form["username"]
	pw = request.form["password"]
	
	# Establish SQL connection
	conn = sql.connect(user='thesportsbook', password='ultimate', host='cs252-lab6-mariadb.cuxhokshop3s.us-east-2.rds.amazonaws.com', database='lab6')
	cursor = conn.cursor(buffered=True)
	cursor.execute("select * from users where username = %s", (user,))
	
	# Check if username exists
	if cursor.rowcount != 0:
		# Exists - redirect to signup
		# TODO: ADD ALERT SAYING INVALID USERNAME
		conn.close()
		return redirect(url_for('signup'))
	else:
		# Doesn't exist - add to users and redirect to bets page
		cursor.execute("insert into users values(%s, %s, 100.0)", (user, pw,))
		conn.commit()
		conn.close()
		# TODO: CREATE SESSION
		return redirect(url_for('home_page'))

@app.route("/login")
def login():
	# LOG-IN PAGE - CONTAINS FIELDS TO INPUT USERNAME AND PASSWORD
	return render_template("login.html")

@app.route("/login", methods=['POST'])
def login_post():
	# LOG-IN PAGE - NEED TO ACCEPT USERNAME AND PASSWORD, REDIRECT TO HOME PAGE IF SUCCESSFUL
	username = request.form["username"]
	pw = request.form["password"]
	
	print("%s %s" % (username, pw))
	# Establish SQL connection
	conn = sql.connect(user='thesportsbook', password='ultimate', host='cs252-lab6-mariadb.cuxhokshop3s.us-east-2.rds.amazonaws.com', database='lab6')
	cursor = conn.cursor(buffered=True)
	print ("Connected")
	cursor.execute("select * from users where username = %s", (username,))
	
	# Check if password is correct
	pwCorrect = False
	b = 0.0
	for(username, password, balance) in cursor:
		b = balance
		if password == pw:
			pwCorrect = True

	conn.close()
	if pwCorrect:
		# TODO: CREATE SESSION
		return redirect(url_for('home_page'))
	else:
		# TODO: GIVE ALERT SAYING INVALID PASSWORD
		return redirect(url_for('login'))

@app.route("/home_page")
def home_page():
	return render_template("home_page.html", bet_list, username)


if __name__ == "__main__":
	application.debug = True
	application.run()
