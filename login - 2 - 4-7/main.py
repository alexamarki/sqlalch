import data.db_session as db_session
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import datetime
from data.user import User
from data.jobs import Jobs
from forms import RegisterForm, LoginForm, JobForm

db_session.global_init("db/expedition.db")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ya_lyceum_secret'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main():
    db_sess = db_session.create_session()
    query = db_sess.query(Jobs).all()
    return render_template('log.html', title='Works log', jobs=query)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if not form.validate_on_submit():
        return render_template('register.html', form=form, title='Registration')
    if form.password.data != form.r_password.data:
        return render_template('register.html', form=form, title='Registration - mismatching passwords')
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.email == form.login.data).first():
        return render_template('register.html', form=form, title='Registration - used email')
    registering_user = User(
        email=form.login.data,
        surname=form.name.data,
        name=form.name.data,
        age=form.age.data,
        position=form.position.data,
        speciality=form.speciality.data,
        address=form.address.data,
    )
    registering_user.set_password(form.password.data)
    db_sess.add(registering_user)
    db_sess.commit()
    return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('login.html', form=form, title='Log in')
    db_sess = db_session.create_session()
    logger = db_sess.query(User).filter(User.email == form.login.data).first()
    if logger and logger.check_password(form.password.data):
        login_user(logger, remember=form.remember_me.data)
        return redirect("/")
    return render_template('login.html', form=form, title='Log in - wrong password or email')


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@login_required
@app.route('/addjob', methods=['POST', 'GET'])
def addjob():
    form = JobForm()
    if not form.validate_on_submit():
        return render_template('job.html', form=form, title='Add Job')
    db_sess = db_session.create_session()
    job = Jobs(
        team_leader=form.team_leader.data,
        job=form.job.data,
        work_size=form.work_size.data,
        collaborators=form.collaborators.data,
        is_finished=form.is_finished.data
    )
    db_sess.add(job)
    db_sess.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
