import pytest

from trefle import Trefle


@pytest.fixture
def simple_query_input():
    return dict(
        token="AZERTYUIO",
        q="tulip",
        category="plants",
        request_type="search"
    )


@pytest.fixture
def simple_build_output():
    return ({'q': 'tulip', 'page': 1, 'filter[author]': 'L.', 'filter_not[common_name]': 'null', 'order[name]': 'asc', 'range[year]': '1900,2000'}
            , 'plants', 'search')


@pytest.fixture
def simple_retrieve_build_output():
    return ({'q': 'rudolfiella-peruviana', 'page': 1}, 'plants', 'get')


class TestQueryset:
    def test_direct_query_bulding(self, simple_query_input):
        data = simple_query_input
        Client = Trefle(**data)
        assert Client._q == data['q']
        assert Client._category == data['category']
        assert Client._request_type == data['request_type']

    def test_simple_query_building(self, simple_build_output, simple_query_input):
        data = simple_query_input
        Client = Trefle(**data)
        base_class_token = Client.token
        assert  base_class_token == simple_query_input["token"]
        query = Client.filter(author="L.").range(year=[1900, 2000]).sort_by(name="asc").exclude(common_name="null")
        assert query.token == base_class_token
        built = query._build()
        assert isinstance(built, tuple)
        assert built == simple_build_output

    def test_retrieve_query_bulding(self, simple_retrieve_build_output):
        Client = Trefle("AZERTYUIOPOP")
        Q = Client.retrieve("rudolfiella-peruviana").in_("plants")
        assert Q._build() == simple_retrieve_build_output

    def test_range_filtering(self):
        Client = Trefle("AZERTYUIOP")
        Q = Client.search("rose").in_("plants").filter(family="Rosaceae").sort_by(slug="asc").range(year=[1980, 2010]).exclude(common_name="null")
        R = Q._build()
        assert R
