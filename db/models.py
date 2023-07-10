from sqlalchemy import Boolean, Column, Integer, String

import database


class Word(database.Base):
    __tablename__ = "words"

    frequency = Column(Integer, primary_key=False)
    word = Column(String, unique=False, primary_key=True)
