import json
import validators.url as valid_url

from trefle.URLs import URLs
from trefle.models import (Kingdom, SubKingdom, Division,
                           DivisionClass, Deserializer, DivisionOrder,
                           Family, Genus, Plant)

AllUrls = URLs()
model_list = [Kingdom, SubKingdom, Division, DivisionClass,
              DivisionOrder, Family, Genus, Plant]
MyDeserializer = Deserializer()


class TestUrls:
    """
    Use validators package to validate each url
    """
    def test_each_url(self):
        assert valid_url(AllUrls.client_side_token_url())
        assert valid_url(AllUrls.corrections_by_id_url().format(id=12))
        assert valid_url(AllUrls.corrections_url())
        assert valid_url(AllUrls.distribution_by_id_url().format(id=34))
        assert valid_url(AllUrls.distributions_url())
        assert valid_url(AllUrls.division_classes_url())
        assert valid_url(AllUrls.division_orders_url())
        assert valid_url(AllUrls.divisions_url())
        assert valid_url(AllUrls.families_url())
        assert valid_url(AllUrls.genus_url())
        assert valid_url(AllUrls.kingdoms_url())
        assert valid_url(AllUrls.plants_by_distributions_url().format(zone_id='RANDOM'))
        assert valid_url(AllUrls.plants_by_genus_url().format(genus_id=1234))
        assert valid_url(AllUrls.plants_url())
        assert valid_url(AllUrls.report_plants_url().format(id=1234))
        assert valid_url(AllUrls.report_species_url().format(id=1234))
        assert valid_url(AllUrls.search_plants_url())
        assert valid_url(AllUrls.search_species_url())
        assert valid_url(AllUrls.species_url())
        assert valid_url(AllUrls.subkingdoms_url())
        assert valid_url(AllUrls.submit_correction_url().format(record_id=1234))


class TestDataModels:
    def test_model_deserializer(self):
        for model in model_list:
            model_name = model.__name__.lower()
            with open(f'trefle/data/{model_name}_data.json', 'r') as f:
                json_string = json.dumps(json.load(f))
                model_instance = MyDeserializer.deserialize(model, json_string)
            assert model_instance.id is not None
