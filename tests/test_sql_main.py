import sys

sys.path.append("src")

import pytest

from src import sql_main
from src import database


@pytest.mark.parametrize(
    "myword, myresult, include, exclude",
    [
        ("древо", ["древо"], "", ""),
        ("_ожка", ["ложка", "ножка"], "", ""),
        ("_ожка", ["ложка"], "л", ""),
        ("_ожка", ["ножка"], "", "л"),
        ("_ожка", ["ножка"], "н", "л"),
        ("_ожка", [], "", "лн"),
        ("_ожка", ["ложка", "ножка"], "ож", ""),
    ],
)
def test_return_list_of_words(
    myword: str, myresult: list[str], include: str, exclude: str
):
    new_search = sql_main.Search()
    new_search.append_exclude(exclude)
    new_search.append_include(include)
    new_search.set_myword(myword)
    assert new_search.returns_list_of_words() == myresult
