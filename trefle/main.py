"""
Main file contains the wrappers
"""
VERSION = 'v1'
import inspect
from typing import Type
from models import Deserializer, Kingdom, SubKingdom, Family, Plant, Species
from utils import get_token, write_token
from URL import URLs
from rest_adapter import RestAdapter
from queryset import QuerySet

Des = Deserializer()

class Trefle(QuerySet):
    def __init__(self, token: str = None, q: str = None, category: str = 'plants', request_type: str = "list"):
        super().__init__(q=q, category=category, request_type=request_type)
        self.token = token
        write_token(token=self.token)
        self.Adapter = RestAdapter(api_key=get_token())
        self.Urls = URLs(version=VERSION)

    def _query(self):
        params, category, rq_type = self._build()
        url = self._build_url(rq_type, category)
        result, dataout = self.Adapter.get(url=url, ep_params=params)
        return result, dataout

    def _build_url(self, operation: str, category: str):
        operation_key = "".join([operation, category.capitalize()])
        url = getattr(self.Urls, operation_key)
        return url.path


Client = Trefle(token="fb7c8Funa_gZnYU5onH0Oj79uapv-vvUMZ9tDqU0JTo") 
r = Client.list("families")
r.show()
# data = r._query()
# print(len(data))
