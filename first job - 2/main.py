import data.db_session as db_session
import datetime
from data.martians import User
from data.jobs import Jobs

db_session.global_init("db/expedition.db")

db_sess = db_session.create_session()

occupation_opt = Jobs(
    team_leader=1,
    job="deployment of residential modules 1 and 2",
    work_size=15,
    collaborators="2, 3",
    start_date=datetime.datetime.now(),
    is_finished=False
)
db_sess.add(occupation_opt)
db_sess.commit()

