# coding=utf-8

import datetime as dt
from app import db


class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer(), primary_key=True)  # record id
    content = db.Column(db.String, unique=True)  # record content
    update_time = db.Column(
        db.DateTime, nullable=False, default=dt.datetime.utcnow)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Record %r>' % self.id
