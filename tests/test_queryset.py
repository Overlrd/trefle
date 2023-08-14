import pytest
from src.trefleapi import Client

@pytest.fixture
def simple_search_query_input():
    return dict(
        token="AZERTYUIO",
        query="tulip",
        category="plants",
        request_type="search"
    )

@pytest.fixture
def simple_search_query_output():
    return ({'q': 'tulip', 'page': 1, 'filter[author]': 'L.', 'filter_not[common_name]': 'null', 'order[name]': 'asc', 'range[year]': '1900,2000'}
            , 'plants', 'search')

@pytest.fixture
def simple_retrieve_query_build_output():
    return ({'q': 'rudolfiella-peruviana', 'page': 1}, 'plants', 'get')

def test_simple_search_query(simple_search_query_input, simple_search_query_output):
    data = simple_search_query_input
    client = Client(**data)
    query = client.filter(author="L.").range(year=[1900, 2000]).sort_by(name="asc").exclude(common_name="null")
    assert query._build() == simple_search_query_output

def test_simple_retrieve_query(simple_retrieve_query_build_output):
    client = Client("azerty")
    query = client.retrieve("rudolfiella-peruviana").in_("plants")
    assert query._build() == simple_retrieve_query_build_output