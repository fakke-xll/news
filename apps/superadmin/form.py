from wtforms import StringField,Form,TextAreaField,IntegerField
from wtforms.validators import InputRequired,Length,EqualTo,Email

class LoginForm(Form):
    admin = StringField(validators=[InputRequired(message="请输入账户")])
    password = StringField(validators=[InputRequired()])

class UserManageForm(Form):
    user_id = IntegerField()
    name = StringField()
    email = StringField()
    password = StringField()
    is_delete = IntegerField()

class DepManageForm(Form):
    dep_id = IntegerField()
    name = StringField()
    email = StringField()
    password = StringField()
    is_delete = IntegerField()

class TagManageForm(Form):
    tag_id = IntegerField()
    name = StringField()
    is_delete = IntegerField()


class NewsManageForm(Form):
    news_id = IntegerField()
    title = StringField()
    department_name = StringField()
    tag_name = StringField()
    content = TextAreaField()
    is_delete = IntegerField()

class CommentManageForm(Form):
    comment_id = IntegerField()
    comment_content = StringField()
    is_delete = IntegerField()

class QuestionManageForm(Form):
    question_id = IntegerField()
    title = StringField()
    tag_name = StringField()
    content = TextAreaField()
    is_delete = IntegerField()

class AnswerManageForm(Form):
    answer_id = IntegerField()
    answer_content = StringField()
    is_delete = IntegerField()