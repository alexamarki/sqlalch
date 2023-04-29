import data.db_session as db_session
from data.martians import User
from data.jobs import Jobs

db_session.global_init("db/expedition.db")

db_sess = db_session.create_session()

captain = User(
    surname='Scott',
    name='Ridley',
    age=21,
    position='captain',
    speciality='research engineer',
    address='module_1',
    email='scott_chief@mars.org'
)
colonist_1 = User(
    surname='Smith',
    name='Anne',
    age=23,
    position='crew member',
    speciality='biotechnologist',
    address='module_3',
    email='smith_biotech@mars.org'
)
colonist_2 = User(
    surname='Maxwell',
    name='Jake',
    age=20,
    position='crew member',
    speciality='software engineer',
    address='module_2',
    email='maxwell_but_not_robert@aol.com'
)
colonist_3 = User(
    surname='Sully',
    name='Jane',
    age=26,
    position='defence',
    speciality='tactitian',
    address='module_1',
    email='sully_weaponry@mars.org'
)
db_sess.add(captain)
db_sess.add(colonist_1)
db_sess.add(colonist_2)
db_sess.add(colonist_3)
db_sess.commit()
