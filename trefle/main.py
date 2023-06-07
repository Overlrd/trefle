"""
Main file contains the wrappers
"""
VERSION = 'v1'
import json
from typing import Dict
from .models import Deserializer, Kingdom
from .utils import get_token, write_token
from .URL import URLs
from .rest_adapter import RestAdapter
from .queryset import QuerySet

class Trefle(QuerySet):
    def __init__(self, token: str = None, q: str = None, category: str = 'plants', request_type: str = "list"):
        super().__init__(q=q, category=category, request_type=request_type)
        self.token = token
        write_token(token=self.token)
        self.Adapter = RestAdapter(api_key=get_token())
        self.Urls = URLs(version=VERSION)

    def _query(self, params: Dict, category: str, rq_type: str):
        url = self._get_url(rq_type, category)
        result, dataout = self.Adapter.get(url=url, ep_params=params)
        return result, dataout

    def _get_url(self, operation: str, category: str):
        operation_key = "".join([operation, category.capitalize()])
        url = getattr(self.Urls, operation_key)
        return url.path

    def _map_model(self, name: str):
        # map a category to a model
        # categories are in plural ex: species, plants, kingdoms
        # so i remove the last letter
        # it should work , unless the category names are changed
        # and even if the validator_ Check will trow a value error to the user
        childrens = Kingdom.__subclasses__()
        for i in childrens:
            if i.__name__.lower() == name[:-1]:
                return i

    def get_data_models(self):
        params, category, rq_type = self._build()
        model = self._map_model(category)
        _, data = self._query(params, category, rq_type)
        models = Deserializer.deserialize(model, data)
        return models

    def get_json_response(self):
        params, category, rq_type = self._build()
        _, data = self._query(params, category, rq_type)
        data = json.loads(data)
        return data