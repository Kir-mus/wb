from flask import render_template, Flask, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    id_1 = StringField('id_Астронавта', validators=[DataRequired()])
    password_1 = PasswordField('Пароль_Астронавта', validators=[DataRequired()])
    id_2 = StringField('id_Капитана', validators=[DataRequired()])
    password_2 = PasswordField('Пароль_Капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


@app.route('/loginn', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Аварийный доступ', form=form)


@app.route('/login')
def du_log():
    return render_template('login_h.html', title='Аварийный доступ')


@app.route("/distribution")
def distribution():
    companion_list = ['Бравый', 'Серый', 'Кувалда', 'Влад']
    return render_template('distribution.html', title='Размещение')


if __name__ == '__main__':
    app.run(port=7000, host='127.0.0.1')
