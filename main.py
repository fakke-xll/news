from apps import department_bp,front_bp,superadmin_bp
from flask import Flask
import config
from exts import db

##自己写的过滤器，用于计算回复、评论等数量
def mylen(args):
    len_arg = []
    for arg in args:
        if not arg.is_delete:
            len_arg.append(arg)
    return len(len_arg)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    env = app.jinja_env
    env.filters['mylen'] = mylen

    app.register_blueprint(department_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(superadmin_bp)
    db.init_app(app)
    
    return app


if __name__ == '__main__':
    print("heello")
    app = create_app()
    app.run()
