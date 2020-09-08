from . import bp
from flask import views,render_template,redirect,request,session,url_for,g
from .forms import RegistForm,LoginForm,MypageForm,AddnewsForm,UserForm,CommentManageForm,NewslistForm,UpdatepwdForm,AddUserForm
from ..models import Department,News,Tag,User,Comment
from exts import db
from .decorators import login_required
import json


@bp.route('/')
@login_required
def index():
    g.users = User.query.filter(User.department_id == g.department.id ).order_by(User.id).all()
    g.news = News.query.filter(News.department_id == g.department.id).order_by(News.id).all() 
    news_number = 0
    for news in g.news:
        if news.is_delete == 0:
            for comment in news.comments:
                if comment.is_delete == 0:
                    news_number +=1
    g.news_number = news_number
    user_gender_list = [0,0,0]
    user_name_list = []
    user_comment_num_list = []
    for user in g.users:
        if user.is_delete == 0:
            if user.gender == '女':
                user_gender_list[0] += 1
            elif user.gender == "男":
                user_gender_list[1] += 1
            else:
                user_gender_list[2] += 1
    all_users = User.query.all()
    for user in g.users:
        i = 0
        if user.is_delete == 0:
            user_name_list.append(user.name)
            print(user.name)
            for comment in user.comments:
                print(comment.news.is_delete)
                if comment.is_delete == 0 and comment.news.department_id == g.department.id:
                    i += 1
            print(i)
            user_comment_num_list.append(i)

    g.user_gender_list = json.dumps(user_gender_list,ensure_ascii=False)
    g.user_name_list = json.dumps(user_name_list,ensure_ascii=False)
    g.user_comment_num_list = json.dumps(user_comment_num_list,ensure_ascii=False)
    return render_template('department/index.html')


@bp.route('/logout/')
@login_required
def logout():
    del session['department_id']
    print("logout")
    return redirect(url_for('department.login'))



class NewslistView(views.MethodView):

    decoreators = [login_required]
    def get(self):
        news = News.query.order_by(News.id).all()
        g.news = news
        tag = Tag.query.order_by(Tag.id).all()
        g.tag = tag
        return render_template('department/newslist.html')

    def post(self):
        form = NewslistForm(request.form)
        # print(form.tag_id.data)
        print(form.newsid.data)
        # print(form.title.data)
        # print(form.content.data)
        is_delete = form.is_delete.data
        print(is_delete) 
        print(11111111111111)
        if is_delete and form.newsid.data:
            news = News.query.get(form.newsid.data)
            news.is_delete = is_delete
            db.session.commit()
            return "删除成功"
        if form.validate():
            # print("nnnnnnnnnnnnnnnnnnnnnnnnnnnn")
            news_id = form.newsid.data
            tag = form.tag_id.data
            title = form.title.data
            content = form.content.data
            # is_delete = form.is_delete.data
            # print(is_delete)
            # print("*"*20)
            news = News.query.get(news_id)
            if news.tag_id != tag or news.title!= title or news.content!=content:
                news.title = title
                news.tag_id = tag
                news.content = content
                db.session.commit()
                return "修改成功"          
        return "新闻未发生修改"

class LoginView(views.MethodView):

    def get(self):
        return render_template('department/login.html')

    def post(self):
        form = LoginForm(request.form)
        # print(form.email.data)
        # print(form.password.data)
        if form.validate():
            email = form.email.data
            password = form.password.data
            # print(email)
            # print(password)
            department = Department.query.filter(Department.email == email , Department.password==password).first()
            g.department = department
            if department and department.is_delete==0:
                # g.department = department.name
                # print(g.cms_user)
                session['department_id'] = department.id
                return "登录成功"
            else:
                return "邮箱或密码错误"
        return "登录失败"

class RegistView(views.MethodView):
    def get(self):
        print('1111')
        return render_template('department/regist.html')

    def post(self):
        form = RegistForm(request.form)
        print(form.name.data)
        print(form.email.data)
        print(form.password.data)
        print(form.password2.data)
        print(form.validate())
        if form.validate():
            email = form.email.data
            name = form.name.data
            password = form.password.data
            print(name)
            department = Department(email=email,name=name,password=password)
            db.session.add(department)
            db.session.commit()
            return "注册成功"
        return "注册失败"

class MypageView(views.MethodView):

    decorators = [login_required]

    def get(self):
        # print('*******************')
        # if hasattr(g,'department'):
        #     print('*******************')
        #     print(g.department)
        return render_template('department/mypage.html')

    def post(self):
        form = MypageForm(request.form)
        # print(form.info.data)
        # print("form.info.data")
        if form.validate():
            name = form.name.data
            info = form.info.data
            department = Department.query.get(g.department.id)
            if department.name != name or department.info != info:
                department.name = name
                department.info = info
                db.session.commit()
                return "部门信息修改成功"
            return "未修改信息"
        return "修改失败"

class AddnewsView(views.MethodView):

    decorators = [login_required]
    def get(self):
        tags = Tag.query.order_by(Tag.id).all()
        g.tags = tags
        return render_template('department/addnews.html')

    def post(self):
        form = AddnewsForm(request.form)
        if form.validate():
            tag_id = form.tag.data
            title = form.title.data
            content = form.content.data
            print(tag_id, content, title)
            print(0000000000000000000000)
            news = News(title=title,content=content,tag_id=tag_id,department_id = g.department.id)
            db.session.add(news)
            db.session.commit()
            return "新闻发布成功"
        else:
            return "请输入新闻标题和内容"

class UpdatepwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('department/updatepwd.html')

    def post(self):
        form = UpdatepwdForm(request.form)
        if form.validate():
            newpwd = form.newpwd1.data
            department = Department.query.get(g.department.id)
            department.password = newpwd
            db.session.commit()
            return "修改成功"
        return "未修改"

class UserView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('department/users.html')

    def post(self):
        form = UserForm(request.form)
        name = form.name.data
        email = form.email.data
        password = form.password1.data
        is_delete = form.is_delete.data
        gender = form.gender.data
        user_id = form.user_id.data
        print(email)
        print(user_id)
        print(is_delete)
        if form.validate():
            if email:
                user = User(name = name,email=email,password=password,gender=gender,department_id= g.department.id)
                db.session.add(user)
                db.session.commit()
                return "添加成功"
            if is_delete and user_id:
                user = User.query.filter(User.id == user_id).first()
                user.is_delete = is_delete
                db.session.commit()
                return "删除成功"
            if user_id :
                user = User.query.filter(User.id == user_id).first()
                
                user.name = name
                user.gender = gender
                if password:
                    user.password = password
                db.session.commit()
                return "修改成功"
        return "修改失败"
        

        

        
        

class CommentmanageView(views.MethodView):
    decorators = [login_required]
    def get(self):
        g.comments = Comment.query.filter(Department.id == g.department.id).order_by(-Comment.addtime).all()
        return render_template('department/commentmanage.html')
    def post(self):
        form = CommentManageForm(request.form)
        if form.validate():
            comment_id = form.comment_id.data
            comment = Comment.query.filter(Comment.id == comment_id).first()
            is_delete = form.is_delete.data
            if is_delete:
                comment.is_delete = is_delete
                db.session.commit()
                return "删除成功"
            else:
                comment_content = form.comment_content.data
                comment.content = comment_content
                db.session.commit()
                return "修改成功"
        return "修改失败"

#钩子函数，拿到session里的数据
@bp.before_request
def before_request():
    department_id = session.get('department_id')
    print("depatid-----------+++++++++++++++---------")
    print(department_id)
    if department_id:
        department = Department.query.get(department_id)
        print("depatid--------------------")
        g.department = department
  

bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/regist/',view_func=RegistView.as_view('regist'))
bp.add_url_rule('/mypage/',view_func=MypageView.as_view('mypage'))
bp.add_url_rule('/addnews/',view_func=AddnewsView.as_view('addnews'))
bp.add_url_rule('/newslist/',view_func=NewslistView.as_view('newslist'))
bp.add_url_rule('/updatepwd/',view_func=UpdatepwdView.as_view('updatepwd'))
bp.add_url_rule('/user/',view_func=UserView.as_view('user'))
bp.add_url_rule('/commentmanage/',view_func=CommentmanageView.as_view('commentmanage'))
