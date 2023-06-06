from typing import Dict, List, Type
from .models import Kingdom
from .rest_adapter import RestAdapter
from .utils import get_token
from .validators_ import Check
C = Check()

class QuerySet:
    """
    ## QuerySet
        A class representing a query set for building complex queries.\n
        Inspired by 'https://github.com/ecederstrand/exchangelib/blob/master/exchangelib/queryset.py'\n
        Support chaining methods\n
        the `_build` method generate a dictionnary intended for request parameters containing\n
        the current attributes of the class instance\n
        the `get_json_response` and `get_data_models` are empty and intended to be overwrited by \n
        the `Trefle` main class. i keep them here for simplicity\n
        Returns:\n
            QuerySet: An instance of the `QuerySet` class representing a query set.\n
    """
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
        self._q = q
        self._page_id = None
        self._request_type = request_type
        self._category = category
        self._filters = {}
        self._excludes = {}
        self._sorts = {}
        self._ranges = {}

    def _copy_self(self, q=None, category=None, request_type=None):
        # function to copy the current class
        # serve the purpose of creating a copy of the current class instance with the option to override
        # specific attributes
        # facilitate bulding variations of the query and chaining operations
        new_qs = self.__class__(token=get_token(), q=q, category=category, request_type=request_type)
        new_qs._filters = self._filters
        new_qs._excludes = self._excludes
        new_qs._sorts = self._sorts
        new_qs._ranges = self._ranges
        return new_qs

    def _query(self, params: Dict, category: str, rq_type: str):
        pass

    def search(self, q: str):
        """
        ## search
            If called after `list` (which is to be avoided), it will preserve filters, sorters, excludes, and ranges.\n
            It will update the request type to `search`.\n
            `Args`:
                `q` (str): The name of the item to search.

            Returns:
                `QuerySet` : Returns an updated copy of self to allow chaining with other functions.

            Example:
                `Client.search('tulip').in_('plants').exclude(key=value)`
        """
        new_qs = self._copy_self(q=q, request_type="search")
        return new_qs

    def list(self, category: str):
        """
        ## list
            If called after `search` (which is to be avoided),
            it will preserve filters, sorters, excludes, and ranges.\n
            It will update the request type to `list`.\n
            Args:
                category (str): The name of the category to list. Available categories:\n
                    - "kingdoms"
                    - "subkingdoms"
                    - "divisions"
                    - "divisionclasses"
                    - "divisionorders"
                    - "families"
                    - "genus"
                    - "plants"
                    - "species"
                    - "distributions"

            Returns:
                QuerySet: An updated copy of self to allow chaining with other functions.

            Example:
                `Client.list('plants').filter(key=value)`
        """
        new_qs = self._copy_self(category=C(category), request_type="list")
        return new_qs

    def in_(self, category: str):
        """
        ## in_ \n
            use only with `search` as `list` already contains a category

            Args:
                category (str): the caterory to search in. Available categories:\n
                    - "kingdoms"
                    - "subkingdoms"
                    - "divisions"
                    - "divisionclasses"
                    - "divisionorders"
                    - "families"
                    - "genus"
                    - "plants"
                    - "species"
                    - "distributions"

            Returns:
                QuerySet: An updated copy of self to allow chaining with other functions.

            Example:
                `Client.search('tulip').in_('plants').exclude(key=value)`
        """
        self._category = C(category)
        return self

    def filter(self, **kwargs):
        """
        ## filter\n
            Adds filter parameters to the query.\n
            Can be called multiple time - will update the filter if exists\n
            Args:\n
                **kwargs: Key-value pairs representing filter parameters.\n
                for a complete list of available filter check :\n
                'https://docs.trefle.io/reference/#tag/Plants/operation/searchPlants'\n
            Returns:\n
                self: Returns an updated copy of self to allow chaining with other functions.\n
            Example:\n
                `Client.list('plants').filter(key0=value0, key1=value1).filter(key2=value2)`\n
        """
        self._add_field("_filters", kwargs)
        return self

    def sort_by(self, **kwargs):
        """
        ## sort_by\n
            Adds sorting parameters to the query.\n
            Args:\n
                **kwargs: Key-value pairs representing sorting parameters.\n
            Returns:\n
                self: Returns an updated copy of self to allow chaining with other functions.\n
            Example:\n
                `Client.list('plants').filter(key0=value0, key1=value1).sort_by(name='asc')`
        """
        self._add_field("_sorts", kwargs)
        return self

    def exclude(self, **kwargs):
        """
        ## exclude\n
            Filters out specific values from the query results.\n
            Args:\n
                **kwargs: Key-value pairs representing exclude parameters.\n
            Returns:\n
                self: Returns an updated copy of self to allow chaining with other functions.\n
            Example:\n
                `Client.list('plants').filter(key0=value0).exclude(key1=value1, key2=value2)`
        """
        self._add_field("_excludes", kwargs)
        return self

    def range(self, **kwargs):
        """
        ## range\n
            Sets range parameters for the query.\n
            for a complete list of available ranges check:\n
            'https://docs.trefle.io/reference/#tag/Plants/operation/searchPlants'\n
            Args:\n
                **kwargs: Key-value pairs representing range parameters.\n
            Returns:\n
                self: Returns an updated copy of self to allow chaining with other functions.\n
            Example:\n
                `Client.list('plants').filter(key0=value0).range(year=[1900, 2000])`
        """
        self._add_field("_ranges", kwargs)
        return self

    def page(self, page: int):
        """
        ## page\n
            Sets the page number for pagination.\n
            Args:\n
                page (int): The page number to set.\n
            Returns:\n
                self: Returns an updated copy of self to allow chaining with other functions.\n
        """
        self._page_id = page
        return self

    def _add_field(self, field: str, data):
        # the code for updating fields started to out of the DRY principe
        # this method update a given attribute value
        field_val = {}
        if isinstance(data, dict):
            for key, value in data.items():
                field_val[key] = value
            current_value = getattr(self, field)
            field_val = field_val | current_value
            setattr(self, field, field_val)

    def show(self):
        """
        ## show\n
            Displays the current state of the query.\n
            Prints the values of different query parameters, including:\n
            - Request type
            - Category
            - Excludes
            - Filters
            - Search query
            - Ranges
            - Sorts

            This method is useful for debugging and inspecting the query parameters.\n
            Returns:
                None
        """
        print(f"{self._request_type=}")
        print(f"{self._category=}")
        print(f"{self._excludes=}")
        print(f"{self._filters=}")
        print(f"{self._q=}")
        print(f"{self._ranges=}")
        print(f"{self._sorts=}")

    def get_data_models(self) -> List[Kingdom]:
        """
        ## get_data_models\n
            Retrieves data models from the JSON response of the API.\n
            Returns:\n
                List[model]: A list of models with a length equal to the number of items in the request response.
        """
        pass

    def get_json_response(self) -> Dict:
        """
        ## get_json_response: Retrieves the formatted JSON response from the API.\n
        Args:\n
            None\n
        Returns:\n
            dict: A Python dictionary containing the JSON response from the API.\n
            Keys:\n
                - 'data': The response body, which can be a list of items or a single item.\n
                - 'links' (absent when getting an item by ID): The API routes of the current request,
                including the first and last pages of the search results.\n
                - 'meta': Contains the total count of items in the results (across all pages).
        """
        pass

    def _build(self):
        # create a dict with the class attributes
        # in order to do multiple sorting-filtering-excuding , the trefle API,
        # waits for prams structured like 'api_url/?token=token&filter[baz]=bar&filter[foo]=baz'
        # it's the reason why i wrote the implementation of line 267
        params = {}
        param_fields = [self._filters, self._excludes, self._sorts, self._ranges]
        param_fields_names = ["filter", "filter_not", "order", "range"]
        if self._request_type == "search":
            params["q"] = self._q
            params["page"] = self._page_id
            for field, field_name in zip(param_fields, param_fields_names):
                for key, value in field.items():
                    params["{}[{}]".format(field_name, key)] = value
        return params, self._category, self._request_type
