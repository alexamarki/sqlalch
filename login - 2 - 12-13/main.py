import data.db_session as db_session
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import datetime
from data.user import User
from data.jobs import Jobs
from data.departments import Departments
from forms import RegisterForm, LoginForm, JobForm, DepartmentForm

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

@app.route('/departments')
def departments():
    db_sess = db_session.create_session()
    query = db_sess.query(Departments).all()
    return render_template('dep_list.html', title='List of Departments', departments=query)


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
        surname=form.surname.data,
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
    job.categories.append(form.hazard.data)
    db_sess.add(job)
    db_sess.commit()
    return redirect('/')

@login_required
@app.route('/editjob/<int:job_id>', methods=['POST', 'GET'])
def editjob(job_id):
    form = JobForm()
    db_sess = db_session.create_session()
    checker = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not checker or current_user.id not in (1, checker.team_leader):
        return redirect('/')
    if form.validate_on_submit():
        checker.team_leader = form.team_leader.data
        checker.job = form.job.data
        checker.work_size = form.work_size.data
        checker.collaborations = form.collaborators.data
        checker.is_finished = form.is_finished.data
        checker.hazard.remove(hazard)
        db_sess.commit()
        return redirect("/")
    return render_template('job.html', form=form, title='Edit Job')


@login_required
@app.route('/deletejob/<int:job_id>')
def deletejob(job_id):
    db_sess = db_session.create_session()
    checker = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if checker and current_user.id in (1, checker.team_leader):
        db_sess.delete(checker)
        db_sess.commit()
    return redirect("/")

@login_required
@app.route('/adddepartment', methods=['POST', 'GET'])
def adddepartment():
    form = DepartmentForm()
    if not form.validate_on_submit():
        return render_template('departments.html', form=form, title='Add department')
    db_sess = db_session.create_session()
    dep = Departments(
        chief=form.chief.data,
        title=form.title.data,
        members=form.members.data,
        email=form.email.data
    )
    db_sess.add(dep)
    db_sess.commit()
    return redirect('/departments')

@login_required
@app.route('/editdepartment/<int:dep_id>', methods=['POST', 'GET'])
def editdepartment(dep_id):
    form = DepartmentForm()
    db_sess = db_session.create_session()
    checker = db_sess.query(Departments).filter(Departments.id == dep_id).first()
    if not checker or current_user.id not in (1, checker.chief):
        return redirect('/departments')
    if form.validate_on_submit():
        checker.chief = form.chief.data,
        checker.title = form.title.data,
        checker.members = form.members.data,
        checker.email = form.email.data
        db_sess.commit()
        return redirect("/departments")
    return render_template('departments.html', form=form, title='Edit department')


@login_required
@app.route('/deletedepartment/<int:dep_id>')
def deletedepartment(dep_id):
    db_sess = db_session.create_session()
    checker = db_sess.query(Departments).filter(Departments.id == dep_id).first()
    if checker and current_user.id in (1, checker.chief):
        db_sess.delete(checker)
        db_sess.commit()
    return redirect("/departments")

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
