from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from hashlib import md5
from flask.ext.login import UserMixin, LoginManager, login_user, current_user, login_required, logout_user

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

app.secret_key = 'c6c482b268b0a985f9b19c03419e246a'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = "login"



class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, uname, email ,password):
        self.username = uname
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = md5(password.encode()).hexdigest()

@login_manager.user_loader
def load_user(user_name):
    return User.query.get(user_name)

# redirect to login view - login_required
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route('/')
@login_required
def home():
    db.create_all()
    return render_template('admin/home/index.html')

@app.route('/user')
@login_required
def user():
    lstuser = User.query.all()
    return render_template('admin/user/index.html', lstuser = lstuser)



@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ''
    if(request.method == 'POST'):
        username = request.form['username']
        password = md5(request.form['password'].encode()).hexdigest()

        user = User.query.filter_by(username = username, password = password).first()
        if (user):
            login_user(user = user)
        else: error_message = 'Wrong User Name or Password!'

    if (current_user.is_authenticated):
        return redirect('/')
    return render_template('admin/login/index.html', error_message = error_message)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/register', methods=['POST'])
def register():
    uname = request.form['username']
    email = request.form['email']
    password = request.form['password']

    user = User(uname, email, password)
    db.session.add(user)
    db.session.commit()

    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
