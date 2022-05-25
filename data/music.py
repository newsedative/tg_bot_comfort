import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Music(SqlAlchemyBase):
    __tablename__ = 'music_of_nature'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')