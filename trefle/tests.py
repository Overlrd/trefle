import json
from pathlib import Path
import validators.url as valid_url

from trefle.URLs import URLs
from trefle.models import Kingdom, SubKingdom, Division, DivisionClass, DivisionOrder, Family, Plant

AllUrls = URLs()
model_list = [Kingdom, SubKingdom, Division, DivisionClass, DivisionOrder, Family, Plant]

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
    def test_data_models(self):
        for model in model_list:
            _path = "data/{}_data.json".format(model.__name__.lower())
            model_data = self.get_model_data(_path)
            feed_model = model(**model_data)
            assert isinstance(feed_model,model)
    
    @staticmethod
    def get_model_data(filepath, field='data'):
        with open(filepath,'r') as f:
            data = json.load(f)
            return data.get(field,data)
            

