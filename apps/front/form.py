
from wtforms import StringField,Form,TextAreaField,IntegerField
from wtforms.validators import InputRequired,Length,EqualTo,Email

class CommentForm(Form):
    content = TextAreaField()
    

class RegistForm(Form):
    username = StringField(validators=[InputRequired(message="请输入用户名"),Length(1,50)])
    email = StringField(validators=[InputRequired(message="请输入邮箱"),Email()])
    password1 = StringField(validators=[InputRequired(),Length(6,100)])
    password2 = StringField(validators=[EqualTo('password1')])
    department_id = IntegerField(validators=[InputRequired()])

class LoginForm(Form):
    email = StringField(validators=[InputRequired(message="请输入邮箱"),Email()])
    password = StringField(validators=[InputRequired(),Length(6,100)])

class AddquestionForm(Form):
    tag = IntegerField(validators=[InputRequired()])
    title = StringField(validators=[InputRequired(message="请输入标题"),Length(1,50)])
    content = TextAreaField()

class AnswerForm(Form):
    content = TextAreaField()

class ModifiyAnswerForm(Form):
    answer_id = IntegerField(validators=[InputRequired()])
    answer = TextAreaField()
    is_delete = IntegerField()

class DeleteCommentForm(Form):
    comment_id = IntegerField(validators=[InputRequired()])
    is_delete = IntegerField()

class MypageForm(Form):
    user_id = IntegerField()
    name= StringField(validators=[InputRequired(),Length(1,50)])
    gender = StringField()
    department_name = StringField()
    info = TextAreaField()
    old_password = StringField(validators=[Length(6,100)])
    new_password1 = StringField(validators=[Length(6,100)])
    new_password2 = StringField(validators=[EqualTo('new_password1')])

   

    