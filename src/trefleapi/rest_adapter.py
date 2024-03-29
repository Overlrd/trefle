import logging
from json import JSONDecodeError
from typing import Dict, Any

import requests

from .exceptions import TrefleException
from .models import Result


class RestAdapter:
    def __init__(self, token: str,
                 logger: logging.Logger = None):
        """
            Constructor for RestAdapter
            :param token:
            :param logger: (optional) If your app has a logger,
              pass it in here.
        """
        self._logger = logger or logging.getLogger(__name__)
        self._token = token

    def _make_request(self, http_method: str, url: str, ep_params=None,
                      data: Dict = None, **kwargs) -> (Result, Any):
        if kwargs:
            url = url.format(**kwargs)
        ep_params["token"] = self._token
        log_line_pre = f"method={http_method}, url={url}, params={ep_params.items()}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))

        # Log HTTP params and perform an HTTP request, catching and
        # re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(method=http_method, url=url,
                                        params=ep_params,
                                        json=data,
                                        timeout=None)
        except requests.exceptions.RequestException as exception:
            self._logger.error(msg=(str(exception)))
            raise TrefleException("Request Failed") from exception
        # Deserialize JSON output to Python object, or
        # return failed Result on exception
        try:
            data_out = response.text
        except (ValueError, JSONDecodeError) as exception:
            raise TrefleException("Bad JSON in response") from exception
        # If status_code in 200-299 range, return success Result with data,
        # otherwise raise exception
        is_success = 299 >= response.status_code >= 200  # 200 to 299 is OK
        log_line = log_line_post.format(is_success, response.status_code, response.reason)

        if is_success:
            self._logger.debug(msg=log_line)
            return Result(response.status_code, message=response.reason), data_out
        self._logger.error(msg=log_line)
        raise TrefleException(f"{response.status_code}: {response.reason}")

    def get(self, url: str, ep_params=None, **kwargs) -> Result:
        if ep_params is None:
            ep_params = {}
        return self._make_request(http_method='get', url=url, ep_params=ep_params,
                                  kwargs=kwargs)

    def post(self, url: str, ep_params=None, data: Dict = None,
             **kwargs) -> Result:
        if ep_params is None:
            ep_params = {}
        return self._make_request(http_method='post', url=url, ep_params=ep_params,
                                  data=data, kwargs=kwargs)
