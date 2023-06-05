from typing import List, Type
from utils import Q
from rest_adapter import RestAdapter
from utils import get_token

class QuerySet:
    ITEMS = ["kingdoms",
             "subkingdoms",
             "divisions",
             "divisionclasses",
             "divisionorders",
             "families",
             "genus",
             "plants",
             "species",
             "distributions"]
    OPERATIONS = ["list",
                  "search"]

    def __init__(self, q: str = None, category: str = 'plants', request_type: str = "list"):
        self.q = q
        self.page_id = None
        self.request_type = request_type
        self.category = category
        self.filters = {}
        self.excludes = {}
        self.sorts = {}
        self.ranges = {}

    def _copy_self(self, q=None, category=None, request_type=None):
        new_qs = self.__class__(token=get_token(), q=q, category=category, request_type=request_type)
        new_qs.filters = self.filters
        new_qs.excludes = self.excludes
        new_qs.sorts = self.sorts
        new_qs.ranges = self.ranges
        return new_qs

    def _query(self, Adapter):
        pass

    def search(self, q: str):
        new_qs = self._copy_self(q=q, category="serach", request_type='search')
        return new_qs

    def list(self, category: str):
        new_qs = self._copy_self(category=category, request_type="list")
        return new_qs

    def in_(self, category: str):
        self.category = category
        return self

    def filter(self, **kwargs):
        self._add_field("filters", kwargs)
        return self

    def sort_by(self, **kwargs):
        self._add_field("sorts", kwargs)
        return self

    def exclude(self, **kwargs):
        self._add_field("excludes", kwargs)
        return self

    def range(self, **kwargs):
        self._add_field("ranges", kwargs)
        return self

    def page(self, page: int):
        self.page_id = page
        return self

    def _add_field(self, field: str, data):
        field_val = {}
        if isinstance(data, dict):
            for key, value in data.items():
                field_val[key] = value
            current_value = getattr(self, field)
            field_val = field_val | current_value
            setattr(self, field, field_val)

    def show(self):
        print(f"{self.request_type=}")
        print(f"{self.category=}")
        print(f"{self.excludes=}")
        print(f"{self.filters=}")
        print(f"{self.q=}")
        print(f"{self.ranges=}")
        print(f"{self.sorts=}")

    def get_name_of(self):
        pass

    def _build(self):
        params = {}
        param_fields = [self.filters, self.excludes, self.sorts, self.ranges]
        param_fields_names = ["filter", "filter_not", "order", "range"]
        if self.request_type == "search":
            params["q"] = self.q
            params["page"] = self.page_id
            for field, field_name in zip(param_fields, param_fields_names):
                for key, value in field.items():
                    params["{}[{}]".format(field_name, key)] = value
        return params, self.category, self.request_type
