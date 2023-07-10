import pytest

from db import sql_main
from db import database


@pytest.mark.parametrize(
    "myword, myresult", [
        ("древо", ["древо"]),
        ("_ожка", ["ложка", "ножка"]),
    ]
)
def test_return_list_of_words(myword, myresult):
    assert sql_main.returns_list_of_words(database.SessionLocal, myword) == myresult


