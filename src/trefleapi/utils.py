from typing import List, Optional
from dataclasses import dataclass
from .exceptions import TrefleException
from .settings import API_SETTINGS

OPERATION_NOT_SUPPORTED = "{} don't support the {} operation, please check the docs ..."
INCORRECT_CATEGORY = "{} is not a correct category, please check the docs ..."

class InputCheck:
    """
    Intended to be a validator class that checks if the given values are accepted by the API.
    
    For the 'filter', 'filter_not', 'range', and 'order' supported fields, please refer to:
    https://docs.trefle.io/reference/#tag/Plants/operation/searchPlants
    
    """

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

    def __call__(self, operation: str, category: str):
        return self.check_op(operation=operation, category=category)

    def check_op(self, operation: str, category: str):
        category = self.check_cat(category)
        operations_paths = API_SETTINGS["routes"]
        operation_id = ''.join([operation, category.capitalize()])
        exist = operations_paths.get(operation_id, {})
        if exist:
            return operation, category
        else:
            raise TrefleException(OPERATION_NOT_SUPPORTED.format(category, operation))

    def check_cat(self, category: str):
        if category in self.CATEGORIES:
            return category
        else:
            raise TrefleException(INCORRECT_CATEGORY.format(category))





class Routes:
    """
    This class contains the available operations , their urls
    and their parameters of the trefle API
    """
    def __init__(self, version: str = 'v1'):
        self.api_version = version
        self.base_url = None
        self.parse_settings()

    def parse_settings(self):
        """
        Load the operations and routes from settings
        """
        url = API_SETTINGS['url'].format(version=self.api_version)
        setattr(self, 'base_url', url)

        routes = API_SETTINGS['routes']
        for i, operation in routes.items():
            operation['path'] = ''.join([self.base_url, operation['path']])
            op = Operation(**operation)
            setattr(self, i, op)



@dataclass
class Operation:
    """
    represents an operation
    """
    method: str
    path: str
    params: Optional[List]
