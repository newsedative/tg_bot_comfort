from data import db_session
from data.users import User


class BotDB:
    def __init__(self):
        db_session.global_init("db/user_data.db")
        self.user = User()
        self.db_sess = db_session.create_session()

    def check(self, id_u):
        q = self.db_sess.query(User).filter(User.user_id == id_u)
        return self.db_sess.query(q.exists()).scalar()

    def add_us(self, id_u):
        self.user.user_id = id_u
        self.db_sess.add(self.user)
        self.db_sess.commit()


bot_db = BotDB()