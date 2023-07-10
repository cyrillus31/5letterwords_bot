from crud import find_words
from database import SessionLocal, engine
from database import Base

# Base.metadata.create_all(bind=engine)


myword = "_ожка"

def returns_list_of_words(myword):
    result = []
    for word in find_words(SessionLocal(), myword):
        result.append(word.word)
    print(result)
    return result

returns_list_of_words(myword)