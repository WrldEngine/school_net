from .database import db

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, unique=True, nullable=False)
    grade = db.Column(db.Integer)
    grade_symbol = db.Column(db.Text)
    password = db.Column(db.Text)

class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    username = db.Column(db.Text, unique=True)
    subject = db.Column(db.Text)
    password = db.Column(db.Text)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.Text)
    task_name = db.Column(db.Text)
    task_photo = db.Column(db.BLOB)
    task_desc = db.Column(db.Text)

class SendAns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer)

    answer_photo = db.Column(db.BLOB)
    answer_desc = db.Column(db.Text)
    from_author = db.Column(db.Text)
    to_teacher = db.Column(db.Text)
    status = db.Column(db.Boolean)