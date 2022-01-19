from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.urls import url_parse

from models import users, get_user
from forms import LoginForm
from decorators import admin_required

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"

posts = []

@app.route("/")
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.name.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user_view')
@login_required
def user_view():
    return render_template('user.html')

@app.route('/admin_view')
@login_required
@admin_required
def admin_view():
    return render_template('admin.html')