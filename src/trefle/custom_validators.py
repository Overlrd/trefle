from typing import Any, List, Union

from .exceptions import TrefleException
from .settings import _api_settings

class Mapper:
    # intended to be a validator class
    # should check for each param if the given value is accepted by the API
    # for filter, filter_not,range,order supported fields check :
    # 'https://docs.trefle.io/reference/#tag/Plants/operation/searchPlants'
    # [TODO] extend the class for filter-range-filter_not.. field validation
    PARAM_FIELDS = ["q",
                    "page",
                    "filter",
                    "filter_not",
                    "order",
                    "range"]
    CATEGORIES = ["kingdoms",
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
                  "search",
                  "get"]
    def __init__(self) -> None:
        pass

    def __call__(self, operation: str, category:str):
        return self.check_op(operation=operation,category=category)
    @staticmethod
    def check_op(operation:str, category:str):
        settings_paths = _api_settings["paths"]
        operation_key = ''.join([operation, category.capitalize()])
        exist = settings_paths.get(operation_key, {})
        if exist:
            return operation, category
        else:
            raise  TrefleException("{} don't support the {} operation, please check the docs ...".format(category,operation))

    def check_cat(self, category: str):
        if category in self.CATEGORIES:
            return  category
        else:
            raise TrefleException("{} is not a correct category, please check the docs ...".format(category))
