from . import bp
from flask import views,render_template,redirect,request,session,url_for,g
from .decorators import login_required
from ..models import SuperAdmin,Department,News,Tag,User,Comment,Question,Answer
from .form import (
    LoginForm,
    UserManageForm,
    DepManageForm,
    TagManageForm,
    NewsManageForm,
    CommentManageForm,
    QuestionManageForm,
    AnswerManageForm
    )
from exts import db
import json

#钩子函数，拿到session里的数据
@bp.before_request
def before_request():
    superadmin_id = session.get('admin_id')
    if superadmin_id:
        superadmin = SuperAdmin.query.get(superadmin_id)
        g.superadmin = superadmin

@bp.route('/')
@login_required
def index():
    g.departments = Department.query.all()
    g.newss = News.query.all()
    g.tags = Tag.query.all()
    g.users = User.query.all()
    departments_list = []
    departments_news_num = []
    
    for department in g.departments:
        i = 0
        if department.is_delete == 0:
            departments_list.append(department.name)
            for news in department.news:
                if news.is_delete == 0:
                    i += 1
            departments_news_num.append(i)

    Jdepartment_list = json.dumps(departments_list,ensure_ascii=False)
    Jdepartments_news_num = json.dumps(departments_news_num,ensure_ascii=False)
    g.department_list = Jdepartment_list
    g.department_news_list = Jdepartments_news_num

    user_num_list = []
    user_active_list = []
    for user in g.users:
        i = 0
        if user.is_delete == 0:
            user_num_list.append(user.name)
            for comment in user.comments:
                if comment.is_delete == 0:
                    i += 1
            for answer in user.answers:
                if answer.is_delete == 0:
                    i += 1
            user_active_list.append(i)
    Juser_num_list = json.dumps(user_num_list,ensure_ascii=False)
    Juser_active_list = json.dumps(user_active_list,ensure_ascii=False)
    g.user_num_list = Juser_num_list
    g.user_active_list = Juser_active_list
    return render_template('superadmin/index.html')

@bp.route('/logout/')
@login_required
def logout():
    del session['admin_id']
    print("logout")
    return redirect(url_for('superadmin.login'))

#登陆
class LoginView(views.MethodView):

    def get(self):
        return render_template('superadmin/login.html')

    def post(self):
        form = LoginForm(request.form)
        print(form)
        if form.validate():
            admin = form.admin.data
            password = form.password.data
            print(admin)
           
            superadmin = SuperAdmin.query.filter(SuperAdmin.name == admin , SuperAdmin.password==password).first()
            g.superadmin = superadmin
            if superadmin :
                # g.department = department.name
                # print(g.cms_user)
                session['admin_id'] = superadmin.id
                return "登录成功"
            else:
                return "邮箱或密码错误"
        return "登录失败"

#用户管理
class UserManageView(views.MethodView):
    decorators = [login_required]
    def get(self):
        g.users = User.query.order_by(User.addtime).all()
        return render_template('superadmin/usermanage.html')

    def post(self):
        form = UserManageForm(request.form)
        new_name = form.name.data
        email = form.email.data
        new_password = form.password.data
        is_delete = form.is_delete.data
        if form.validate():
            user = User.query.filter(User.email == email).first()
            if is_delete:
                user.is_delete = is_delete
                db.session.commit()
                return "删除成功"
            else:
                user.name = new_name
                user.password = new_password
                db.session.commit()
                return "修改成功"
        return "修改失败"

#部门管理
class DepManageView(views.MethodView):
    decorators = [login_required]
    def get(self):
        g.departments = Department.query.order_by(Department.addtime).all()
        return render_template('superadmin/depmanage.html')

    def post(self):
        form = DepManageForm(request.form)
        new_name = form.name.data
        email = form.email.data
        new_password = form.password.data
        is_delete = form.is_delete.data
        if form.validate():
            dep = Department.query.filter(Department.email == email).first()
            if is_delete:
                dep.is_delete = is_delete
                db.session.commit()
                return "删除成功"
            else:
                dep.name = new_name
                dep.password = new_password
                db.session.commit()
                return "修改成功"
        return "修改失败"

#栏目管理
class TagManageView(views.MethodView):
    decorators = [login_required]
    def get(self):
        g.tags = Tag.query.order_by(Tag.addtime).all()
        return render_template('superadmin/tagmanage.html')

    def post(self):
        form = TagManageForm(request.form)
        tag_id = form.tag_id.data
        is_delete = form.is_delete.data
        name = form.name.data
        if name :
            tag = Tag(name = name)
            db.session.add(tag)
            db.session.commit()
            return "添加成功"
        if form.validate() and is_delete:
            tag = Tag.query.filter(Tag.id == tag_id).first() 
            tag.is_delete = is_delete
            db.session.commit()
            return "删除成功"
        return "操作失败"

#新闻管理
class NewsManageView(views.MethodView):
    decorators = [login_required]
    def get(self):
        g.newss = News.query.order_by(News.addtime).all()
        g.tags = Tag.query.all()
        g.departments = Department.query.all()
        return render_template('superadmin/newsmanage.html')

    def post(self):   
        form = NewsManageForm(request.form)
        if form.validate():
            news_id = form.news_id.data
            print(news_id)
            news = News.query.filter(News.id == news_id).first()
            is_delete = form.is_delete.data
            if is_delete:
                news.is_delete = is_delete
                db.session.commit()
                return "删除成功"
            else:
                title = form.title.data
                content = form.content.data
                tag_name = form.tag_name.data
                department_name = form.department_name.data
                tag_id = Tag.query.filter(Tag.name==tag_name).first().id
                department_id = Department.query.filter(Department.name ==department_name).first().id
                news.title = title
                news.content = content
                news.tag_id = tag_id
                news.department_id = department_id
                db.session.commit()
                return "修改成功"
        return "修改失败"
 
#评论管理
class CommentManageView(views.MethodView):
    decorators = [login_required]
    def get(self):
        g.comments = Comment.query.order_by(Comment.addtime).all()
        return render_template('superadmin/commentmanage.html')

    def post(self):  
        form = CommentManageForm(request.form)
        if form.validate():
            comment_id = form.comment_id.data
            print(comment_id)
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

class QuestionManageView(views.MethodView):
    decorators = [login_required]
    def get(self):
        g.questions = Question.query.order_by(Question.addtime).all()
        g.tags = Tag.query.all()
        g.users = User.query.all()
        return render_template('superadmin/questionmanage.html')
    
    def post(self):
        form = QuestionManageForm(request.form)
        if form.validate():
            question_id = form.question_id.data
            question = Question.query.filter(Question.id == question_id).first()
            is_delete = form.is_delete.data
            if is_delete:
                question.is_delete = is_delete
                db.session.commit()
                return "删除成功"
            else:
                title = form.title.data
                content = form.content.data
                tag_name = form.tag_name.data
                tag_id = Tag.query.filter(Tag.name==tag_name).first().id
                question.title = title
                question.content = content
                question.tag_id = tag_id
                db.session.commit()
                return "修改成功"
        return "修改失败"


class AnswerManageView(views.MethodView):
    decorators = [login_required]
    def get(self):
        g.answers = Answer.query.order_by(Answer.addtime).all()
        return render_template('superadmin/answermanage.html')

    def post(self):  
        form = AnswerManageForm(request.form)
        if form.validate():
            answer_id = form.answer_id.data
            answer = Answer.query.filter(Answer.id == answer_id).first()
            is_delete = form.is_delete.data
            if is_delete:
                answer.is_delete = is_delete
                db.session.commit()
                return "删除成功"
            else:
                answer_content = form.answer_content.data
                print(answer_content)
                answer.content = answer_content
                db.session.commit()
                return "修改成功"
        return "修改失败"


bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/user/',view_func=UserManageView.as_view('usermanage'))
bp.add_url_rule('/dep/',view_func=DepManageView.as_view('depmanage'))
bp.add_url_rule('/tag/',view_func=TagManageView.as_view('tagmanage'))
bp.add_url_rule('/news/',view_func=NewsManageView.as_view('newsmanage'))
bp.add_url_rule('/comment/',view_func=CommentManageView.as_view('commentmanage'))
bp.add_url_rule('/question/',view_func=QuestionManageView.as_view('questionmanage'))
bp.add_url_rule('/answer/',view_func=AnswerManageView.as_view('answermanage'))