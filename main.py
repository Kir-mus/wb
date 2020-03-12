from flask import Flask, render_template
from datetime import date
from data import db_session
from data.jobs import Jobs


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/jo.sqlite")
db_session.global_init("db/blogs.sqlite")


session = db_session.create_session()


@app.route('/works')
def works():
    jobsid = {}
    for jobs in session.query(Jobs):
        jobsid[str(jobs.id)] = [jobs.job, jobs.team_leader, jobs.work_size, jobs.collaborators, jobs.is_finished]
    return render_template('table.html', title='Журнал работ', jobsid=jobsid)


if __name__ == '__main__':
    app.run(port=7000, host='127.0.0.1')
