import pytest
from trefleapi import Client

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
def not_support_search_categories():
    return ["kingdoms","subkingdoms","divisions","divisionclasses","divisionorders","families","genus","distributions"]

@pytest.fixture
def support_search_categories():
    return ["plants","species"]
@pytest.fixture
def simple_retrieve_build_output():
    return ({'q': 'rudolfiella-peruviana', 'page': 1}, 'plants', 'get')


class TestQueryBuild:
    def test_direct_query_bulding(self, simple_query_input):
        data = simple_query_input
        client = Client(**data)
        assert client._q == data['q']
        assert client._category == data['category']
        assert client._request_type == data['request_type']

    def test_simple_query_building(self, simple_build_output, simple_query_input):
        data = simple_query_input
        client = Client(**data)
        base_class_token = client.token
        assert  base_class_token == simple_query_input["token"]
        query = client.filter(author="L.").range(year=[1900, 2000]).sort_by(name="asc").exclude(common_name="null")
        assert query.token == base_class_token
        built = query._build()
        assert isinstance(built, tuple)
        assert built == simple_build_output

    def test_retrieve_query_bulding(self, simple_retrieve_build_output):
        client = Client("AZERTYUIOPOP")
        Q = client.retrieve("rudolfiella-peruviana").in_("plants")
        assert Q._build() == simple_retrieve_build_output

    def test_range_filtering(self):
        client = Client("AZERTYUIOP")
        Q = client.search("rose").in_("plants").filter(family="Rosaceae").sort_by(slug="asc").range(year=[1980, 2010]).exclude(common_name="null")
        R = Q._build()
        assert R

    def test_retrieve_family(self):
        client = Client("AZERTYUIOP")
        Q = client.retrieve("1").in_("families")._build()
        assert Q

    def test_search_no_search_support_categories(self, not_support_search_categories):
        client = Client("AZERTYUIOP")
        for i in not_support_search_categories:
            with pytest.raises(Exception) as e_info:
                Q = client.search("foo").in_(i)._build()

    def test_seach_support_categories(self, support_search_categories):
        client = Client("AZERTYUIOP")
        for i in support_search_categories:
            Q = client.search("foo").in_(i)._build()
            assert Q
