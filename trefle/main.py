"""
Main file contains the wrappers
"""
VERSION = 'v1'

from utils import get_token, write_token
from URL import URLs
from rest_adapter import Query, RestAdapter

class Trefle:
    def __init__(self, token):
        self.token = token
        write_token(token=self.token)
        self.Adapter = RestAdapter(api_key=self.token)
        self.Urls = URLs(version=VERSION)

    def listKingdoms(self, page: int = None):
        url = self.Urls.listKingdoms.path
        print(url)
        result = self.Adapter.get(url=url)
        return result

if __name__ == '__main__':
    print("starting trefle module")
    token = get_token()
    print(token)
    Client = Trefle(token=token)
    r = Client.listKingdoms()
    print(r)