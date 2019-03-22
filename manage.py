# coding:utf-8

from ihome import create_app,db
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate

# 创建flask应用对象
app=create_app("develop")

manager=Manager(app)
Migrate(app,db)
manager.add_command("db",MigrateCommand)

if __name__ == '__main__':
    manager.run()



