"""
Main file contains the wrappers
"""
import json
from typing import Dict

from .api_operations import APIRoutes
from .models import Deserializer, Kingdom
from .queryset import QuerySet
from .rest_adapter import RestAdapter

VERSION = 'v1'


class Client(QuerySet):
    def __init__(self, token: str = None, q: str = None, category: str = 'plants', request_type: str = "list"):
        super().__init__(q=q, category=category, request_type=request_type)
        self.token = token
        self.Adapter = RestAdapter(api_key=self.token)
        self.Routes = APIRoutes(version=VERSION)

    def _query(self, params: Dict, category: str, rq_type: str):
        # when the request type is 'get' I simply add the id or slug directly in the url
        # as requested by the trefle API.
        # the rest of the parameters(if they users have given) are passed though as they don't affect the response
        url = self._get_url(rq_type, category)
        if rq_type == "get":
            id_or_slug = params["q"]
            url = url.format(id=id_or_slug)
        result, data_out = self.Adapter.get(url=url, ep_params=params)
        return result, data_out

    def _get_url(self, rq_type: str, category: str) -> str:
        # in the config file each operation is stored like 'operationCategory'
        operation = "".join([rq_type, category.capitalize()])
        url = getattr(self.Routes, operation)
        return url.path

    @staticmethod
    def _map_model(category: str):
        # map a category to a model
        # map the given name
        children = Kingdom.__subclasses__()
        for i in children:
            if i._category == category:
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
