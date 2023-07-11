from src.crud import find_words
from src.database import SessionLocal, engine
from src.database import Base

# Base.metadata.create_all(bind=engine)


myword = "_ожка"

def returns_list_of_words(myword):
    result = []
    for word in find_words(SessionLocal(), myword.lower()):
        result.append(word.word)
    return result
