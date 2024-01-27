from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

# ----------------------------------------- [ Category ]----------------------------------------- #
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False, unique=True)
    password = db.Column(db.String(24), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Username {}>'.format(self.username)

# ----------------------------------------- [ Tweet ]----------------------------------------- #
class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authorID = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(24),  nullable=False)
    msg = db.Column(db.String(240),  nullable=False)
    
    def __init__(self, authorID, date, msg):
        self.authorID = authorID
        self.date = date
        self.msg = msg
    
    def __repr__(self):
        return '<Tweet {}>'.format(self.msg)
