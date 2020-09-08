
from wtforms import StringField,Form,TextAreaField,IntegerField
from wtforms.validators import InputRequired,Length,EqualTo,Email

class RegistForm(Form):
    name = StringField(validators=[InputRequired(message="请输入用户名"),Length(1,50)])
    email = StringField(validators=[InputRequired(message="请输入邮箱"),Email()])
    password = StringField(validators=[InputRequired(),Length(6,100)])
    password2 = StringField(validators=[EqualTo('password')])


class LoginForm(Form):
    email = StringField(validators=[InputRequired(message="请输入邮箱"),Email()])
    password = StringField(validators=[InputRequired(),Length(6,100)])

class MypageForm(Form):
    name = StringField(validators=[InputRequired(message="请输入用户名"),Length(1,50)])
    info = TextAreaField()

class AddnewsForm(Form):
    tag = IntegerField(validators=[InputRequired()])
    title = StringField(validators=[InputRequired(message="请输入标题"),Length(1,50)])
    content = TextAreaField()

class NewslistForm(Form):
    newsid = IntegerField(validators=[InputRequired()])
    tag_id = IntegerField(validators=[InputRequired()])
    title = StringField(validators=[InputRequired(message="请输入标题"),Length(1,50)])
    content = TextAreaField()
    is_delete = IntegerField()

class UpdatepwdForm(Form):
    oldpwd = StringField(validators=[InputRequired(),Length(6,100)])
    newpwd1 =  StringField(validators=[InputRequired(),Length(6,100)])
    newpwd2 =  StringField(validators=[EqualTo('newpwd1')])

class AddUserForm(Form):
    name1 = StringField(validators=[InputRequired(message="请输入用户名"),Length(1,50)])
    email1 = StringField(validators=[InputRequired(message="请输入邮箱"),Email()])
    phone1 = StringField(validators=[InputRequired(message="请输入手机号"),Length(11,11,message="请输入正确格式手机号")])
    password1 = StringField(validators=[InputRequired(),Length(6,100)])
    password2 = StringField(validators=[EqualTo('password')])
    gender1 = StringField(validators=[InputRequired(message="请选择性别"),Length(1,10)])
    role1 = StringField(validators=[InputRequired(message="请选择性别"),Length(1,10)])

class CommentManageForm(Form):
    comment_id = IntegerField()
    comment_content = StringField()
    is_delete = IntegerField()

class UserForm(Form):
    user_id = IntegerField()
    name = StringField()
    email = StringField()
    password1 = StringField()
    password2 = StringField()
    info = TextAreaField()
    is_delete = IntegerField()
    gender = StringField()