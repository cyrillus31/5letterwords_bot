from sqlalchemy.orm import Session

from db import models

def find_words(db: Session, expression: str):
    # return db.query(models.Word).filter(models.Word.word.ilike(expression)).all()
    return db.query(models.Word).filter(models.Word.word == expression).all()

