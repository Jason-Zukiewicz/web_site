# region -- [IMPORTS] --------------------------------------------------------------------------------------------------
from flask import Flask, request, jsonify, session, url_for, redirect, g, render_template_string
from flask_cors import CORS
from werkzeug.exceptions import abort
from sqlalchemy import and_
import os
from datetime import datetime
from models import db, User, Tweet
from functools import wraps

app = Flask(__name__)

def handle_preflight():
    response = jsonify()
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# endregion -- [IMPORTS]

# region -- [DataBase] --------------------------------------------------------------------------------------------------
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'dev key'
app.config.from_object(__name__)
db.init_app(app)

@app.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()

    # Create sample users
    jay = User(username="jay", password="pass")
    db.session.add(jay)

    joel = User(username="joel", password="pass")
    db.session.add(joel)

    db.session.commit()

    print('Initialized the database.')
# endregion -- [DataBase]

# region -- [Router]  --------------------------------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    title = "Welcome to My Flask App"
    content = "This is some content for the homepage."

    # HTML string without a separate template file
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Our Website</title>
    </head>
    <body>
    
        <h1>This is the home page</h1>
        <p>Content will go here</p>
    </body>
    </html>
    """

    # Render the HTML string
    return render_template_string(html_content, title=title, content=content)

@app.route('/login/', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return handle_preflight()
    
    # Parse request 
    req_data = request.get_json()
    if "username" not in req_data:
        return jsonify({"error": "Username is missing"}), 400
    if "password" not in req_data:
        return jsonify({"error": "Password is missing"}), 400
    username = req_data["username"]
    password = req_data["password"]
    
    # Check values
    user = User.query.filter_by(username=username).first()
    if user is None or user.password != password:
        return jsonify({"error": "Invalid username or password"}), 401 
    
    # Set Cookies and return
    session['user_id'] = user.id
    return jsonify({"message": "Login in successfully", "userId": user.id, "userName": user.username}), 201
 
@app.route("/logout/")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route("/signup/", methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        return handle_preflight()
    
    print("INSIDE SIGNUP")
    # Parse request 
    req_data = request.get_json()
    if "username" not in req_data:
        return jsonify({"error": "Username is missing"}), 400
    if "password1" not in req_data:
        return jsonify({"error": "Password1 is missing"}), 400
    if "password2" not in req_data:
        return jsonify({"error": "Password2 is missing"}), 400
    username = req_data["username"]
    password1 = req_data["password1"]
    password2 = req_data["password2"]

    # Check values
    if password1 != password2:
        return jsonify({"error": "Passwords don't match"}), 400 
    if is_valid_username(username) or not is_valid_password(password1):
        return jsonify({"error": "Invalid username or password"}), 401

    # Add to DB
    new_user = User(username=username, password=password1)
    db.session.add(new_user)
    db.session.commit()
    
    # Set Cookies and return
    session['user_id'] = new_user.id
    return jsonify({"message": "User created successfully"}), 201
    
@app.route("/tweet/", methods=["POST"])
def tweet_post():
    req_data = request.get_json()
    
    if "authorID" not in req_data:
        return jsonify({"error": "authorID is missing"}), 400
    if "msg" not in req_data:
        return jsonify({"error": "MSG is missing"}), 400
    
    authorID = req_data["authorID"]  
    msg = req_data["msg"]    
    date = datetime.now().strftime("%Y-%m-%d")
    
    print("GOT DATA")

    #if not is_valid_username(authorID):
    #   return jsonify({"error": "Username not valid"}), 400 

    if not is_valid_msg(msg):
        return jsonify({"error": "Message not valid"}), 400 
    
    print("CHECKED  DATA")
    
    new_tweet = Tweet(authorID=authorID, date=date, msg=msg)
    db.session.add(new_tweet)
    db.session.commit()
    return jsonify({"status": "Tweet created successfully", 
                    "authorID": authorID,
                    "date": date,
                    "id":new_tweet.id}), 201

@app.route("/tweet/<tweetID>", methods=["GET"])
def tweet_get_by_id(tweetID=None):
    tweet = Tweet.query.filter_by(id=tweetID).first()
    if tweet is None:
        return jsonify({"message": "Tweet not found"}), 200  # Return a success response with a message

    return jsonify({
        "id": tweet.id,
        "authorID": tweet.authorID,
        "date": tweet.date,
        "msg": tweet.msg
    })
    


@app.route("/tweets/<userId>/", methods=["GET"])
def user_tweets_get(userId=None):
    if not is_valid_userId(userId):
        return jsonify({"error": "userId is invalid"}), 400 
    
    return tweet_get_all_by_user(userId)


# endregion -- [Router]

# region -- [UTIL]  --------------------------------------------------------------------------------------------------
def userID_from_username(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return -1
    return user.id

def is_valid_userId(userId):
	if User.query.filter_by(id=userId).first() is None:
		return False
	return True

def is_valid_username(username):
	if User.query.filter_by(username=username).first() is None:
		return False
	return True

def is_valid_password(password):
    if password is None:
        return False
    return True

def is_valid_msg(msg):
    size = len(msg)
    if 1 > size or  size > 240:
        return False
    return True

def tweet_get_all_by_user(authorID):
    tweets = Tweet.query.filter_by(authorID=authorID).all()
    
    if not tweets:
        return jsonify({"error": "No tweets found for the specified authorID"}), 400

    # Return a list of tweets as JSON
    return jsonify([
        {
            "id": tweet.id,
            "authorID": tweet.authorID,
            "date": tweet.date,
            "msg": tweet.msg
        }
        for tweet in tweets
    ])


# endregion -- [UTIL] 

# region -- [ Cookies ]  --------------------------------------------------------------------------------------------------

# authentication,
# session management
# sensitive information
@app.before_request
def before_request():
    g.user = None
    if 'user.if' in session:
        user = User.query.get([session['user_id']])
        if user:
            g.user = user

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view            

@app.route("/protected/")
@login_required
def protected():
    return "This is a protected route." 
# endregion -- [ Cookies ] 

# region -- [ MAIN ]  --------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
# endregion -- [ MAIN ] 