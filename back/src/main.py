from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import abort
from sqlalchemy import and_
import os
from datetime import datetime
from models import db, User, Tweet

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# -------------------------------------------------------- [ DataBase ] -----------------------------------------------#
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

# -------------------------------------------------------- [ Router ] -----------------------------------------------#
@app.route("/login/", methods=["POST"])
def login_post():
    req_data = request.get_json()
    if "username" not in req_data:
        return jsonify({"error": "Username is missing"}), 400
    if "password1" not in req_data:
        return jsonify({"error": "Password1 is missing"}), 400
    
    username = req_data["username"]
    password = req_data["password"]
    
    user = User.query.filter_by(username=username).first()
    if user is None or user.password != password:
        return jsonify({"error": "Invalid username or password"}), 401 
    
    return jsonify({"status": "Login in successfully"}), 201
        
@app.route("/signup/", methods=["POST"])
def signup_post():
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

    if password1 != password2:
        return jsonify({"error": "Passwords don't match"}), 400 
    if is_valid_username(username) or not is_valid_password(password1):
        return jsonify({"error": "Invalid username or password"}), 401
    
    new_user = User(username=username, password=password1)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "User created successfully"}), 201
    
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
        return jsonify({"error": "Tweet ID is invalid"}), 400 
    
    return jsonify({
        "id": tweet.id,
        "authorID": tweet.authorID,
        "date": tweet.date,
        "msg": tweet.msg
    })
    
@app.route("/<username>/", methods=["GET"])
def user_tweets_get(username=None):
    if not is_valid_username(username):
        return jsonify({"error": "Username is invalid"}), 400 
    
    userID = userID_from_username(username)
    return tweet_get_all_by_user(userID)
    
# -------------------------------------------- [ UTIL ] ------------------------------------------------- #

def userID_from_username(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return -1
    return user.id

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
        return jsonify({"error": "No tweets found for the specified authorID"}), 404

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

# -------------------------------------------- [ OLD ] ------------------------------------------------- #
if __name__ == "__main__":
	app.run(debug=True)