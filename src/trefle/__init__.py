from .main import Trefle
fake_token = "AZERTYUIOP"

class TestQueryset:
    fake_data = dict(
        token="AZERTYUIOP",
        q="tulip",
        category="plants",
        request_type="search"
    )

    def test_direct_querying(self):
        Client = Trefle(**self.fake_data)
        assert Client.show()