from flask import Flask, render_template, redirect, abort, request, make_response, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from flask_restful import reqparse, abort, Api, Resource
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
import sqlalchemy_serializer
from requests import get, put, delete
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import date
from data import db_session
from data.jobs import Jobs
from data.users import User
from sqlalhimi.data import users_resource, jobs_resource
import jobs_api


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/jo.sqlite")
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
# для списка объектов
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
# для одного объекта
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:news_id>')
api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:news_id>')


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


class AddjobsForm(FlaskForm):
    job = StringField('Job title', validators=[DataRequired()])
    id_lead = IntegerField('Team leader id', validators=[DataRequired()])
    w_size = IntegerField('Work size', validators=[DataRequired()])
    coll = StringField('Collaborators', validators=[DataRequired()])
    finished = BooleanField('is job finished')
    submit = SubmitField('Add')


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
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, message=None)



@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = AddjobsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs()
        job.team_leader = form.id_lead.data
        job.job = form.job.data
        job.work_size = form.w_size.data
        job.collaborators = form.coll.data
        job.is_finished = form.finished.data
        current_user.jobs.append(job)
        session.merge(current_user)
        session.commit()
        return redirect('/works')
    return render_template('jobs.html', title='Создание работы', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/works")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, message=None)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = AddjobsForm()
    if request.method == "GET":
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == id,
                                         Jobs.user == current_user).first()
        if job:
            job.team_leader = form.id_lead.data
            job.job = form.job.data
            job.work_size = form.w_size.data
            job.collaborators = form.coll.data
            job.is_finished = form.finished.data
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == id,
                                         Jobs.user == current_user).first()
        if job:
            job.team_leader = form.id_lead.data
            job.job = form.job.data
            job.work_size = form.w_size.data
            job.collaborators = form.coll.data
            job.is_finished = form.finished.data
            session.commit()
            return redirect('/works')
        else:
            abort(404)
    return render_template('jobs.html', title='Редактирование работ', form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == id,
                                     Jobs.user == current_user).first()
    if job:
        session.delete(job)
        session.commit()
    else:
        abort(404)
    return redirect('/works')


@app.route('/')
@app.route('/works')
def works():
    session = db_session.create_session()
    jobsid = {}
    for jobs in session.query(Jobs):
        jobsid[str(jobs.id)] = [jobs.job, jobs.team_leader, jobs.work_size, jobs.collaborators, jobs.is_finished,
                                jobs.user]
    return render_template('table.html', title='Журнал работ', jobsid=jobsid)


if __name__ == '__main__':
    app.register_blueprint(jobs_api.blueprint)
    app.run(port=7000, host='127.0.0.1')
