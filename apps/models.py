from exts import db
from datetime import datetime

class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(100),nullable=False)
    addtime = db.Column(db.DateTime,default=datetime.now)
    is_delete =db.Column(db.Boolean,default=0 )
    info =  db.Column(db.Text)

    news = db.relationship('News', backref='department')
    users = db.relationship('User', backref='department')

class SuperAdmin(db.Model):
    __tablename__ = 'superadmin'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(100),nullable=False)
    addtime = db.Column(db.DateTime,default=datetime.now)

class News(db.Model):
    __tablename = 'news'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text,nullable=False)
    addtime = db.Column(db.DateTime,default=datetime.now)
    is_delete =db.Column(db.Boolean,default=0 )

    tag_id = db.Column(db.Integer,db.ForeignKey('tag.id'))
    department_id = db.Column(db.Integer,db.ForeignKey('department.id'))

    comments = db.relationship('Comment', backref='news')


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False,unique=True)
    addtime = db.Column(db.DateTime,default=datetime.now)
    is_delete =db.Column(db.Boolean,default=0 )

    news = db.relationship('News',backref='tag')
    questions = db.relationship('Question',backref='tag')


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False,unique=True)
    
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(100),nullable=False)
    gender = db.Column(db.String(10),nullable=False,default='保密')
    addtime = db.Column(db.DateTime,default=datetime.now)
    info =  db.Column(db.Text,nullable=True)
    is_delete =db.Column(db.Boolean,default=0 )

    department_id =  db.Column(db.Integer,db.ForeignKey('department.id'))#属于哪个部门
    
    comments = db.relationship('Comment', backref='user')
    answers = db.relationship('Answer', backref='user')
    questions = db.relationship('Question', backref='user')


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text,nullable=False)
    addtime = db.Column(db.DateTime,default=datetime.now)
    is_delete =db.Column(db.Boolean,default=0 )

    news_id = db.Column(db.Integer,db.ForeignKey('news.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text,nullable=False)
    addtime = db.Column(db.DateTime,default=datetime.now)
    is_delete =db.Column(db.Boolean,default=0 )

    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    tag_id = db.Column(db.Integer,db.ForeignKey('tag.id'))
    
    answers = db.relationship('Answer', backref='question')


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text,nullable=False)
    addtime = db.Column(db.DateTime,default=datetime.now)
    is_delete =db.Column(db.Boolean,default=0 )
    
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))




