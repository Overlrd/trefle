import json
import validators.url as valid_url
from random import randrange

from trefle.URL import URLs
from trefle.models import (Kingdom, SubKingdom, Division,
                           DivisionClass, Deserializer, DivisionOrder,
                           Family, Genus, Plant, Species)

model_list = [Kingdom, SubKingdom, Division, DivisionClass,
              DivisionOrder, Family, Genus, Plant, Species]
api_settings_file_path = "trefle/api_settings.json"

AllUrls = URLs(settings_path=api_settings_file_path)
AllUrls.parse_settings()
MyDeserializer = Deserializer()


class TestUrls:
    """
    Use validators package to validate each url
    """
    def test_each_url(self):
        with open(api_settings_file_path, 'r') as f:
            test_data = json.load(f)
            test_paths = test_data['paths']
            for i in test_paths:
                url = getattr(AllUrls, i)
                assert url
                for j in url.params:
                    if 'required' in j:
                        r = j.split('-')[0]
                        r_dict = {r: randrange(0, 99)}
                        assert valid_url(url.path.format(**r_dict))

class TestDataModels:
    def test_model_deserializer(self):
        for model in model_list:
            model_name = model.__name__.lower()
            with open(f'trefle/data/{model_name}_data.json', 'r') as f:
                json_string = json.dumps(json.load(f))
                model_instance = MyDeserializer.deserialize(model, json_string)
            assert model_instance.id is not None
