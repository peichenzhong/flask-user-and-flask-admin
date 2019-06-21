from flask import Flask,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_user  import login_required,UserManager,UserMixin,SQLAlchemyAdapter,current_user

from  flask_migrate import  Migrate,MigrateCommand
from  flask_script import Manager
from  flask_admin.contrib.fileadmin import  FileAdmin
from  flask_admin.base import AdminIndexView,expose
#from  flask_user import  UserManager,SQLAlchemyAdapter,current_user




from  flask import url_for
from  flask_admin import  Admin, form
from  flask_admin.contrib.sqla import  ModelView


app = Flask(__name__)

app.config['SECRET_KEY'] = "thisisasecret"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"
app.config["CSRF_ENABLED"]=True
app.config['USER_ENABLE_EMAIL'] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
app.config["SQLALCHEMY_COMMIT_TEARDOWN "]= True
db = SQLAlchemy(app)


'''
数据库版本迁移
'''
manager=Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)



class User(db.Model,UserMixin):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(50),nullable = False , unique = True)
    password = db.Column(db.String(255),nullable = False ,server_default = '')
    active = db.Column(db.Boolean(),nullable = False,server_default = "0")




db_adapter = SQLAlchemyAdapter(db,User)
user_namager=UserManager(db_adapter,app)

"admin"
admin=Admin(app)
db_adapter = SQLAlchemyAdapter(db,User)
#user_namage = UserManager(db_adapter,app)

class MyUserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return  url_for("index")






@app.route("/")
def  index():
    return "<h1>this is the home page!</h1>"



@app.route("/profile")
@login_required
def profile():
    return "<h1>this is the protected profile page!</h1>"



admin.add_view(MyUserView(User,db.session))

if __name__ == '__main__':
    manager.run(debug =True)