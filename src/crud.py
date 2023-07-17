from sqlalchemy.orm import Session
from sqlalchemy import and_, text

from src import models


def find_words(
    db: Session,
    expression: str,
    included_char_list: list[str] = [],
    excluded_char_list: list[str] = [],
) -> list[models.Word]:
    like_list = [models.Word.word.ilike(expression)] + [
        models.Word.word.ilike(letter) for letter in included_char_list
    ]
    not_like_list = [
        models.Word.word.not_ilike(expression_not)
        for expression_not in excluded_char_list
    ]
    return db.query(models.Word).filter(and_(*like_list, *not_like_list)).all()
    # return db.query(models.Word).filter(models.Word.word == expression).all()
