import data.db_session as db_session
from flask import Flask, render_template, redirect, request
import datetime
from data.user import User
from data.jobs import Jobs
from forms import RegisterForm

db_session.global_init("db/expedition.db")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ya_lyceum_secret'


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
    return redirect('/')


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
