from flask import Flask

def say_hello(username = "World"):
	return '<p>Hello %s!</p>\n' % username

header_text = '''
	<html>\n
<style>
h1 {
	text-align: center
}

button{
	background-color: #ebebeb;
	color: black;
	padding: 14px 20px;
	margin: 8px 0;
	border: none;
	cursor: pointer;
	width: 100%;
}

.modal {
	display: none;
	position: fixed;
	z-index: 1;
	left: 0;
	top: 0;
	color: #C0C0C0;
	width: 100%;
	height: 100%;
	overflow: auto;
	background-color: rgb(0,0,0);
	background-color: rgba(0,0,0,0.4);
	padding-top: 60px;
}
.imgcontainer{
	text-align: center;
	margin: 24px 0 12px 0;
	position: relative;
}

img.avatar{
	width: 40%
	border-radius: 50%;
}

.container{
	padding: 16px;
}

span.psw{
	float: right;
	padding-top: 16px;
}

.modal-content{
	background: -webkit-linear-gradient(top,  #0f182b 0%,#db2028 33%,#db2028 66%,#db2028 100%);
	margin: 5px auto;
	border: 1px solid #888;
	width: 70%;
}

.close{
	position: absolute;
	right: 25px;
	top: 0;
	color: #000;
	font-size: 35px;
	font-weight: bold;
}

.close:hover,
.close:focus{
	color: red;
	cursor: pointer;
}

.animate{
	-webkit-animation: animatezoom 0.6s;
	animation: animatezoom 0.6s;
}

@-webkit-keyframes animatezoom{
	from{-webkit-transform: scale(0)}
	to{-webkit-transform: scale(1)}
	}
</style>
\n
	<head> <title>Welcome to the Ultimate Sports Book! </title> </head>\n<body>'''

instructions = '''
	<p><em> This is a thing</em>: So now were building a program, yay!</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'
application = Flask(__name__)

webpage = '''
	<h1>Welcome to the Ultimate Sportsbook</h1>
   <button type="button" onclick="signup()">Signup</button>
   <p></p>
   <button onclick="document.getElementById('login_page').style.display='block'" style="width:auto;">Login</button>
<div id="login_page" class="modal">
	<span onclick=document.getElementById('login_page').style.display='none'"
		class "close" title="Close Modal">&times;</span>
		<form class="modal-content animate" action="/action_page.php">
		<div class="container">
			<label for="uname"><b>Username:</b></label>
			<input type="text" placeholder="Enter Username" name="uname" required><br>
			<label for="uname"><b>Password:</b></label>
			<input type="password" id="passInput" placeholder="Enter Password" name="psw" required>
			<br>
			<input type="checkbox" onclick="showPass()">Show Password<br>
			<button type="submit">Login</button>
			<label>
				<input type="checkbox" checked="checked" name="remember"> Remember Me
			</label>
		</div>

		<div class="container" style="background: -webkit-linear-gradient(top,  #db2028 0%,#db2028 33%,#0f182b 66%,#0f182b 100%)">
			<button type="button" onclick="document.getElementById('login_page').style.display='none'"
			class="cancelbtn">Cancel</button>
			<span class="psw">Forgot <a href="#">password?</a></span>
		</div>
		</form>
</div>






<script>
var login_modal = document.getElementById('login_page');

window.onclick = function(event) {
    if (event.target == login_modal) {
        login_modal.style.display = "none";
    }
}
function showPass(){
	var x = document.getElementById("passInput");
	if (x.type==="password"){
		x.type = "text";
	}
	else{
		x.type="password";
	}
}
</script>
'''

application.add_url_rule('/', 'index', (lambda: header_text + say_hello()+ webpage + footer_text))

application.add_url_rule('/<username>', 'hello', (lambda username: header_text+ say_hello(username)+ home_link+ footer_text))

if __name__ == "__main__":
	application.debug = True
	application.run()
