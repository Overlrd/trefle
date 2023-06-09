import json
import validators.url as valid_url
from random import randrange

from trefleapi.settings import Paths
from trefleapi.api_operations import APIRoutes

api_operations_path = Paths['api_settings']
Routes = APIRoutes()


class TestUrls:
    """
    Use validators package to validate each url
    """
    def test_each_url(self):
        with open(api_operations_path, 'r') as f:
            test_data = json.load(f)
            test_paths = test_data['paths']
            for i in test_paths:
                url = getattr(Routes, i)
                assert url
                for j in url.params:
                    if 'required' in j:
                        r = j.split('-')[0]
                        r_dict = {r: randrange(0, 99)}
                        assert valid_url(url.path.format(**r_dict))
