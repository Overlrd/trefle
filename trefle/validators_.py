from typing import Any, List, Union
from exceptions import TrefleException

class Check:
    # intended to be a validator class
    # should check for each param if the given value is accepted by the API
    # for filter, filter_not,range,order supported fileds check :
    # 'https://docs.trefle.io/reference/#tag/Plants/operation/searchPlants'
    # [TODO] extend the class for filter-range-filter_not.. field validation
    PARAM_FIELDS = ["q",
                    "page",
                    "filter",
                    "filter_not",
                    "order",
                    "range"]
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

    def __init__(self) -> None:
        pass

    def _map(self, item: str, items: List):
        if item in items:
            return item
        else:
            raise TrefleException("{} don't map any expected field".format(item))

    def check(self, q: Union[List, str], to_check: str):
        if isinstance(to_check, str):
            to_check = getattr(self, '{}'.format(to_check.upper()))
        out = []
        if isinstance(q, list):
            for i in q:
                out.append(self._map(i, to_check))
            return out
        else:
            return self._map(q, to_check)

    def __call__(self, q: Union[str, List], to_check: str = None) -> Any:
        if not to_check:
            to_check = self.PARAM_FIELDS + self.ITEMS + self.OPERATIONS
        return self.check(q=q, to_check=to_check)
