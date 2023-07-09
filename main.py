from db.crud import find_words
from db.database import SessionLocal, engine
from db.database import Base

Base.metadata.create_all(bind=engine)

myword = "абзац"

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print(find_words(SessionLocal(), myword))