import data.db_session as db_session
from flask import Flask, render_template, redirect, request
import datetime
from data.user import User
from data.jobs import Jobs

db_session.global_init("db/expedition.db")

app = Flask(__name__)


@app.route('/')
def main():
    db_sess = db_session.create_session()
    query = db_sess.query(Jobs).all()
    return render_template('log.html', title='Works log', jobs=query)


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
