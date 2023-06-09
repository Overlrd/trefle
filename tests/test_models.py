from pathlib import Path
import json
from trefleapi.models import (Kingdom, SubKingdom, Division,
                              DivisionClass, Deserializer, DivisionOrder,
                              Family, Genus, Plant, Species)

model_list = [Kingdom, SubKingdom, Division, DivisionClass,
              DivisionOrder, Family, Genus, Plant, Species]

THIS_DIR = Path(__file__).parent
DATA_PATH = THIS_DIR / "data"


class TestDataModels:
    """ 
        As all the object returned by the trefle api always have an unique id and slug
        the test assert on these fields
    """
    def test_model_deserializer(self):
        for model in model_list:
            model_name = model.__name__.lower()
            print(model_name)
            with open(f'{DATA_PATH}/{model_name}_data.json', 'r') as f:
                json_string = json.dumps(json.load(f))
                model_instance = Deserializer().deserialize(model, json_string)
            assert type(model_instance.id) is int
            assert len(model_instance.slug) > 0
