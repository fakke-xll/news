from flask_migrate import MigrateCommand,Migrate
from flask_script import Manager
from main import create_app
from exts import db
from apps.models import Department,User,Comment,News,Tag,Question,Answer

app = create_app()


manager = Manager(app)

Migrate(app,db)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()