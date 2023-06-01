import logging
from json import JSONDecodeError
from typing import Dict, Callable

import requests
import requests.packages

from trefle.URL import URLs
from trefle.exceptions import TrefleException
from trefle.models import Result


class RestAdapter:
    def __init__(self, api_key: str, ver: str = 'v1',
                 ssl_verify: bool = True, urls: Callable = URLs,
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
        self.URLs = urls(ver)
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
