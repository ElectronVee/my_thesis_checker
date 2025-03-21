from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Thesis(db.Model):
    __tablename__ = 'thesis'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), nullable=False)
    class_number = db.Column(db.String(20), nullable=False)
    student_name = db.Column(db.String(50), nullable=False)
    thesis_title = db.Column(db.String(200))
    advisor = db.Column(db.String(50))
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    other_info = db.Column(db.Text)

    files = db.relationship('File', backref='thesis', lazy=True)
    check_results = db.relationship('CheckResult', backref='thesis', lazy=True)


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    thesis_id = db.Column(db.Integer, db.ForeignKey('thesis.id'), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_name = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(300), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)


class CheckResult(db.Model):
    __tablename__ = 'check_results'
    id = db.Column(db.Integer, primary_key=True)
    thesis_id = db.Column(db.Integer, db.ForeignKey('thesis.id'), nullable=False)
    check_item = db.Column(db.String(100), nullable=False)
    result = db.Column(db.Boolean, nullable=False)
    message = db.Column(db.Text)
    check_date = db.Column(db.DateTime, default=datetime.utcnow)
