"""
Main file contains the wrappers
"""
VERSION = 'v1'
import json
from typing import Dict

from .api_operations import APIRoutes
from .models import Deserializer, Kingdom
from .queryset import QuerySet
from .rest_adapter import RestAdapter


class Trefle(QuerySet):
    def __init__(self, token: str = None, q: str = None, category: str = 'plants', request_type: str = "list"):
        super().__init__(q=q, category=category, request_type=request_type)
        self.token = token
        # write_token(token=self.token)
        # self.Adapter = RestAdapter(api_key=get_token())
        self.Adapter = RestAdapter(api_key=self.token)
        self.Urls = APIRoutes(version=VERSION)

    def _query(self, params: Dict, category: str, rq_type: str):
        # when the request type is 'get' I simply add the id or slug directly in the url
        # as requested by the trefle API.
        # the rest of the parameters are passed though as they don't affect the response
        url = self._get_url(rq_type, category)
        print("query params :", params)
        if rq_type == "get":
            id_or_slug = params["q"]
            url = url.format(id=id_or_slug)
        result, data_out = self.Adapter.get(url=url, ep_params=params)
        return result, data_out

    def _get_url(self, operation: str, category: str) -> str:
        operation_key = "".join([operation, category.capitalize()])
        url = getattr(self.Urls, operation_key)
        return url.path

    def _map_model(self, name: str):
        # map a category to a model
        # categories are in plural ex: species, plants, kingdoms
        # so i remove the last letter
        # it should work , unless the category names are changed
        # and even if the validator_ Check will trow a value error to the user
        children = Kingdom.__subclasses__()
        for i in children:
            if i.__name__.lower() == name[:-1]:
                return i

    def get_models(self):
        params, category, rq_type = self._build()
        model = self._map_model(category)
        _, data = self._query(params, category, rq_type)
        models = Deserializer().deserialize(model=model, json_string=data)
        return models

    def get_json(self):
        params, category, rq_type = self._build()
        _, data = self._query(params, category, rq_type)
        data = json.loads(data)
        return data
