from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import mysql.connector as sql
from mysql.connector import errorcode

application = app = Flask(__name__)
app.secret_key = os.urandom(24)

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
		#flash('That username is already taken')
		conn.close()
		return redirect(url_for('signup'))
	else:
		# Doesn't exist - add to users and redirect to bets page
		cursor.execute("insert into users values(%s, %s, 100.0)", (user, pw,))
		conn.commit()
		conn.close()
		# TODO: CREATE SESSION
		session['user'] = user
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
	
	# Establish SQL connection
	conn = sql.connect(user='thesportsbook', password='ultimate', host='cs252-lab6-mariadb.cuxhokshop3s.us-east-2.rds.amazonaws.com', database='lab6')
	cursor = conn.cursor(buffered=True)
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
		session['user'] = username
		return redirect(url_for('home_page'))
	else:
		# TODO: GIVE ALERT SAYING INVALID PASSWORD
		#flash('Invalid password')
		return redirect(url_for('login'))

@app.route("/home_page")
def home_page():
	if not 'user' in session:
		return redirect(url_for('index'))
		
	username = session['user']
	# Establish SQL connection
	conn = sql.connect(user='thesportsbook', password='ultimate', host='cs252-lab6-mariadb.cuxhokshop3s.us-east-2.rds.amazonaws.com', database='lab6')
	cursor = conn.cursor(buffered=True)
	cursor.execute("select balance from users where username = %s", (username,))
	balance = cursor.fetchone()[0]
	cursor.execute("select date, home_id, away_id, home_money_line, away_money_line, home_spread, away_spread, over_under from nba_schedule order by date limit 10")

	# Send bet list to home_page
	bet_list = cursor.fetchmany(size=10)
	conn.close()
	print(session['user'])
	return render_template("home_page.html", balance=balance, bet_list=bet_list)

@app.route("/home_page", methods=['POST'])
def home_page_post():
	if not 'user' in session:
		return redirect(url_for('index'))

	# Obtain betting inputs
	date = request.form["date"]
	team = request.form["teamname"]
	risk = float(request.form["amount"])
	type = request.form["Type of Bet"]
	
	# Establish SQL Connection
	username = session['user']
	conn = sql.connect(user='thesportsbook', password='ultimate', host='cs252-lab6-mariadb.cuxhokshop3s.us-east-2.rds.amazonaws.com', database='lab6')
	cursor = conn.cursor(buffered=True)
	
	cursor.execute("select balance from users where username = %s", (username,))
	balance = float(cursor.fetchone()[0])
	if risk > balance:
		# TODO: Notify that risk exceeds balance
		return redirect(url_for('home_page'))
	
	cursor.execute("insert into current_bets values(%s, %s, %s, %s, %s)", (username, date, team, type, risk,))
	cursor.execute("update users set balance = balance - %s where username = %s", (risk, username))
	conn.commit()
	
	# Return to page
	# TODO: SHOW CONFIRMATION WINDOW
	return redirect(url_for('home_page'))
	
@app.route("/user")
def user():
	if not 'user' in session:
		return redirect(url_for('index'))
	
	# Establish SQL Connection
	username = session['user']
	conn = sql.connect(user='thesportsbook', password='ultimate', host='cs252-lab6-mariadb.cuxhokshop3s.us-east-2.rds.amazonaws.com', database='lab6')
	cursor = conn.cursor(buffered=True)
	
	# Get balance
	cursor.execute("select balance from users where username = %s", (username,))
	balance = cursor.fetchone()[0]
	
	# Get current bets
	cursor.execute("select date, team_id, bet_type, risk from current_bets where username = %s", (username,))
	current_bet_list = cursor.fetchall()
	cursor.execute("select date, team_id, bet_type, risk, payout from past_bets where username = %s limit 20", (username,))
	past_bet_list = cursor.fetchall()
	conn.close()

	return render_template("user.html", username=username, balance=balance, current_bet_list=current_bet_list, past_bet_list=past_bet_list)
	
@app.route("/user", methods=['POST'])
def user_post():
	if not 'user' in session:
		return redirect(url_for('index'))
	
	# Get value to add
	deposit = request.form["funds"]
	
	# Establish SQL Connection
	username = session['user']
	conn = sql.connect(user='thesportsbook', password='ultimate', host='cs252-lab6-mariadb.cuxhokshop3s.us-east-2.rds.amazonaws.com', database='lab6')
	cursor = conn.cursor(buffered=True)
	
	# Add to user's balance
	cursor.execute("update users set balance = balance + %s", (deposit,))
	conn.commit()
	conn.close()

	return redirect(url_for('user'))
	
@app.route("/logout")
def logout():
	session.pop('user', None)
	return redirect(url_for('index'))

if __name__ == "__main__":
	application.debug = True
	application.run()
