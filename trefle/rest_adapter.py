import logging
from json import JSONDecodeError
from typing import Dict, Callable, Optional, List

import requests
import requests.packages

from exceptions import TrefleException
from models import Result


class RestAdapter:
    def __init__(self, api_key: str, ver: str = 'v1',
                 ssl_verify: bool = True,
                 logger: logging.Logger = None):
        """
            Constructor for RestAdapter
            :param api_key:
            :param ver:
            :param ssl_verify: Normally set to True, but if having SSL/TLS
              cert validation issues, can turn off with False
            :param logger: (optional) If your app has a logger,
              pass it in here.
        """
        self._logger = logger or logging.getLogger(__name__)
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def _make_request(self, http_method: str, url: str, ep_params: Dict = None,
                      data: Dict = None, **kwargs) -> Result:
        url = url.format(**kwargs)
        headers = {'x-api-key': self._api_key}
        log_line_pre = f"method={http_method}, url={url}, params={ep_params}"
        log_line_post = ', '.join((log_line_pre,
                                   "success={}, status_code={}, message={}"))

        # Log HTTP params and perform an HTTP request, catching and
        # re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(method=http_method, url=url,
                                        verify=self._ssl_verify,
                                        headers=headers, params=ep_params,
                                        json=data)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise TrefleException("Request Failed") from e
        # Deserialize JSON output to Python object, or
        # return failed Result on exception
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            raise TrefleException("Bad JSON in response") from e
        # If status_code in 200-299 range, return success Result with data,
        # otherwise raise exception
        is_success = 299 >= response.status_code >= 200  # 200 to 299 is OK
        log_line = log_line_post.format(is_success, response.status_code,
                                        response.reason)
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(response.status_code, message=response.reason,
                          data=data_out)
        self._logger.error(msg=log_line)
        raise TrefleException(f"{response.status_code}: {response.reason}")

    def get(self, url: str, ep_params: Dict = None, **kwargs) -> Result:
        return self._make_request(http_method='get', url=url, ep_params=ep_params,
                                  kwargs=kwargs)

    def post(self, url: str, ep_params: Dict = None, data: Dict = None,
             **kwargs) -> Result:
        return self._make_request(http_method='post', url=url, ep_params=ep_params,
                                  data=data, kwargs=kwargs)


class Query:
    def __init__(self, q: Optional[str], id_: Optional[str], page: Optional[int]):
        self.q = q
        self.id_ = id_
        self.page = page
        self.filters = None
        self.filter_not = None
        self.orders = None
        self.ranges = None

    def filter_(self, field: str, values: List[str]) -> 'Query':
        """### Filter query results based on as fields values\n
        Full list of filters : https://docs.trefle.io/reference/#tag/Plants/operation/listPlants

        Args:
            field (str): the field to filter on
            values (List[str]): the values to filter on , can be a single or many values

        Returns:
            Query: the Query object
        """
        self.filters[field] = values
        return self

    def range_(self, field: str, minval: int = None, maxval: int = None) -> 'Query':
        """ ### filter on a range of values

        Args:
            field (str): the field filter by range on \n
            minval (int, optional): the minimum value of the range. Defaults to 0.\n
            maxval (int, optional): the maximum value of the range. Defaults to None.\n
        Note:
            ``Can specify only min or max value``

        Returns:
            Query: the Query object
        """

        self.ranges[field] = f"{minval}" if not maxval else f",{maxval}"
        return self

    def order(self, field: str, order: bool = False) -> 'Query':
        """_summary_

        Args:
            field (str): the field to sort by
            order (bool, optional): the order to sort in ('ascending:True','descending:False'). Defaults to False.
        Note:
            *Can perform multiple sorting by calling method again*
            check : https://docs.trefle.io/docs/guides/sorting#multiple-sorting
        """
        self.orders[field] = "asc" if order else "desc"
        return self

    def exclude_null(self, field: str) -> 'Query':
        """### Exclude null values\n

        Args:
            field (str): the field to filter on\n

        Returns:
            Query: the Query object
        """
        self.filter_not[field] = "null"
        return self