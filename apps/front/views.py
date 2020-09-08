from . import bp
from flask import render_template,g,views,request,jsonify,redirect,url_for,session
from ..models import Department,News,Tag,User,Comment,Question,Answer
from .decorators import login_required
from .form import (
    RegistForm,
    LoginForm,
    CommentForm,
    AddquestionForm,
    AnswerForm,
    ModifiyAnswerForm,
    DeleteCommentForm,
    MypageForm,

)
from exts import db
# import qiniu
# import os


@bp.route('/')
@login_required
def index():
    return render_template('front/index.html')

#新闻详情页
class NewsDetailView(views.MethodView):
    def get(self,news_id):
        g.news_detail = News.query.filter(News.id == news_id).first()
        g.comments = Comment.query.filter(Comment.news_id == news_id).order_by(Comment.addtime).all()
        
        print("=======================")
        return render_template('front/newsdetail.html')

    def post(self,news_id):
        form = CommentForm(request.form)
        if form.validate() :
            content = form.content.data
            # newsid = form.news_id.data
            comment = Comment(content=content, user_id = g.current_user.id, news_id=news_id)
            db.session.add(comment)
            db.session.commit()
            return "评论成功"
        return "评论添加失败"



@bp.before_request
def before_request():
    g.newses = News.query.order_by(-News.addtime).all()
    g.departments = Department.query.order_by(Department.id).all()
    g.tags = Tag.query.order_by(Tag.id).all()
    g.users = User.query.filter().all()
    current_user_id = session.get('current_user_id')
    if current_user_id:
        current_user = User.query.get(current_user_id)
        g.current_user = current_user
        print('current_user_id:',current_user_id)

    # print('this is user')
    # print(g.user)

# 注册
class RegistView(views.MethodView):
    def get(self):
        return render_template('front/regist.html')

    def post(self):
        form = RegistForm(request.form)
        print("----------------------------------")
        print(form)
        if form.validate():
            print("---------+++++++++++-------------------------")
            username = form.username.data
            email = form.email.data
            password = form.password1.data
            
            department_id = form.department_id.data
            print(username,email,password,department_id)
            user = User(name=username, email=email,password=password,department_id=department_id)
            db.session.add(user)
            db.session.commit()
            print("注册成功")
            return "注册成功"
        return "注册失败"

#退出登录
@bp.route('/logout/')
@login_required
def logout():
    del session['current_user_id']
    # print("logout")
    return redirect(url_for('front.login'))

#登录
class LoginView(views.MethodView):
    def get(self):
        return render_template('front/login.html')

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = User.query.filter(User.email == email,User.password == password).first()
            if user and user.is_delete==0:
                session['current_user_id'] = user.id    
                print(user.id,"用户id")
                return "登录成功"
            return "密码或邮箱错误"
        return "登录失败"


#个人账户页面
class MypageView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('front/mypage.html')
    
    def post(self):
        form = MypageForm(request.form)
        user_id = form.user_id.data
        name = form.name.data
        gender = form.gender.data
        department_name = form.department_name.data
        info = form.info.data
        old_password = form.old_password.data
        new_password1 = form.new_password1.data    
        user = User.query.filter(User.id == user_id ).first()
        print(user_id,name,gender,department_name,info,old_password,new_password1)
        if old_password and new_password1:
            print(new_password1)
            user.password = new_password1
            db.session.commit()
            return "修改成功"
        if name and gender and department_name:
            department = Department.query.filter(Department.name == department_name).first()
            department_id = department.id
            user.department_id = department_id
            if  user.name != name or user.gender != gender or user.info != info:
                user.name = name
                user.gender = gender
                user.info = info 
                db.session.commit()
                return "修改成功"
        return "操作失败"
        
        


#选择新闻栏目
class TagNewsView(views.MethodView):
    decorators = [login_required]
    def get(self,tag_id):
        g.tag_news = News.query.filter(News.tag_id == tag_id).all()
        return render_template('front/tagnews.html')

    def post(self):
        pass

#选择部门的新闻
class DepNewsView(views.MethodView):
    decorators = [login_required]
    def get(self,department_id):
        g.dep_news = News.query.filter(News.department_id == department_id).all()
        return render_template('front/depnews.html')

    def post(self):
        pass

class Mycomment(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('front/mycomment.html')

    def post(self):
        form = DeleteCommentForm(request.form)
        is_delete = form.is_delete.data
        if is_delete and form.validate() :
            comment_id = form.comment_id.data
            comment = Comment.query.get(comment_id)
            comment.is_delete = is_delete
            db.session.commit()
            return "删除成功" 
        return "删除失败"

class Myanswer(views.MethodView):
    decorators = [login_required]
    def get(self):
        g.answers = Answer.query.filter(Answer.user_id == g.current_user.id).order_by(Answer.addtime).all()
        return render_template('front/myanswer.html')

    def post(self):
        form1 = ModifiyAnswerForm(request.form)
        new_answer = form1.answer.data
        is_delete = form1.is_delete.data
        if is_delete and form1.validate() :
            answer_id = form1.answer_id.data
            answer = Answer.query.get(answer_id)
            answer.is_delete = is_delete
            db.session.commit()
            return "删除成功"
        elif form1.validate() :
            answer_id = form1.answer_id.data
            answer = Answer.query.get(answer_id)
            if new_answer :
                answer.content = form1.answer.data
            else :
                answer.is_delete = 1
            db.session.commit()
            return "修改成功"
       
        
        return "修改失败"

class Questionlist(views.MethodView):
    decorators = [login_required]
    def get(self):
        g.questions = Question.query.order_by(Question.id).all()
        return render_template('front/questionlist.html')

    def post(self):
        pass

class Myquestion(views.MethodView):
    def get(self):
        g.questions = Question.query.filter(Question.user_id == g.current_user.id).order_by(Question.addtime).all()
        return render_template('front/myquestion.html')
    def post(self):
        pass

class Addquestion(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('front/addquestion.html')
    
    def post(self):
        form = AddquestionForm(request.form)
        print(form)
        if form.validate():
            tag_id = form.tag.data
            title = form.title.data
            content = form.content.data
            print(tag_id, content, title)
            print(0000000000000000000000)
            question = Question(title=title,content=content,tag_id=tag_id,user_id = g.current_user.id)
            db.session.add(question)
            db.session.commit()
            return "新闻发布成功"
        else:
            return "请输入新闻标题和内容"

class QuestionDetailView(views.MethodView):
    decorators = [login_required]
    def get(self,question_id):
        g.question_detail = Question.query.filter(Question.id == question_id).first()
        g.answers = Answer.query.filter(Answer.question_id == question_id).order_by(Answer.addtime).all()
        
        print("g.question_detail")
        return render_template('front/questiondetail.html')

    def post(self,question_id):
        form = AnswerForm(request.form)
        if form.validate() :
            content = form.content.data
            # newsid = form.news_id.data
            answer = Answer(content=content, user_id = g.current_user.id, question_id=question_id)
            db.session.add(answer)
            db.session.commit()
            return "回复成功"
        return "回复失败"

bp.add_url_rule('/regist/',view_func=RegistView.as_view('regist')) 
bp.add_url_rule('/login/',view_func=LoginView.as_view('login')) 
bp.add_url_rule('/mypage/',view_func=MypageView.as_view('mypage')) 
bp.add_url_rule('/myanswer/',view_func=Myanswer.as_view('myanswer')) 
bp.add_url_rule('/mycomment/',view_func=Mycomment.as_view('mycomment')) 
bp.add_url_rule('/questionlist/',view_func=Questionlist.as_view('questionlist'))
bp.add_url_rule('/addquestion/',view_func=Addquestion.as_view('addquestion'))
bp.add_url_rule('/myquestion/',view_func=Myquestion.as_view('myquestion'))
bp.add_url_rule('/tag/<tag_id>/',view_func=TagNewsView.as_view('tagnews'))
bp.add_url_rule('/dep/<department_id>/',view_func=DepNewsView.as_view('depnews'))
bp.add_url_rule('/newsdetail/<news_id>/',view_func=NewsDetailView.as_view('newsdetail'))
bp.add_url_rule('/questiondetail/<question_id>/',view_func=QuestionDetailView.as_view('questiondetail'))

