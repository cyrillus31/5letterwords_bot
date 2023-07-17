from src.crud import find_words
from src.database import SessionLocal, engine
from src.database import Base

# Base.metadata.create_all(bind=engine)


class Search:
    def __init__(
        self, myword: "str" = "", include: str = "", exclude: str = ""
    ) -> None:
        self.myword = myword
        self.include = include
        self.exclude = exclude

    def append_include(self, additional: "str"):
        self.include += additional.lower().strip()

    def append_exclude(self, additional: "str"):
        self.exclude += additional.lower().strip()

    def status(self):
        return (self.include, self.exclude)

    def set_myword(self, myword):
        self.myword = myword.lower().strip()

    def returns_list_of_words(self) -> list[str]:
        include = [f"%{letter}%" for letter in self.include]
        exclude = [f"%{letter}%" for letter in self.exclude]

        list_of_orm_objects = find_words(
            SessionLocal(),
            self.myword.lower(),
            included_char_list=include,
            excluded_char_list=exclude,
        )

        result = []
        for word in list_of_orm_objects:
            result.append(word.word)
        return result
