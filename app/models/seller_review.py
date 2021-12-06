from flask import current_app as app
from flask_wtf import FlaskForm
from flask_login import UserMixin
from .. import login


class seller_review:
    def __init__(self, rid, pid, uid, email, timestamp, rating, review):
        self.rid = rid
        self.sid = sid
        self.uid = uid
        self.email = email
        self.timestamp = timestamp
        self.rating = rating
        self.review = review

    