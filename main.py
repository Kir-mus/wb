from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, login_required, logout_user
from datetime import date
from data import db_session
from data.jobs import Jobs
from data.users import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/blogs.sqlite")
login_manager = LoginManager()
login_manager.init_app(app)


class RegisterForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password_1 = PasswordField('пароль', validators=[DataRequired()])
    password_2 = PasswordField('еще раз', validators=[DataRequired()])
    surname = StringField('surname', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired()])
    pos = StringField('Pos', validators=[DataRequired()])
    spes = StringField('Spe', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    submit = SubmitField('setup')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password_1.data != form.password_2.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            position=form.pos.data,
            speciality=form.spes.data,
            address=form.address.data,
            age=form.age.data
        )
        user.set_password(form.password_1.data)
        session.add(user)
        session.commit()
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/works')
def works():
    session = db_session.create_session()
    jobsid = {}
    for jobs in session.query(Jobs):
        jobsid[str(jobs.id)] = [jobs.job, jobs.team_leader, jobs.work_size, jobs.collaborators, jobs.is_finished]
    return render_template('table.html', title='Журнал работ', jobsid=jobsid)


if __name__ == '__main__':
    app.run(port=7000, host='127.0.0.1')
