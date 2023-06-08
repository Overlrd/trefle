# Trefle-Api

*Trefle-API* is a simple python API wrapper for the [trefle](https://trefle.io./) botanic data API

```python
>>> from trefle_api import Trefle
>>> Client = Trefle(token="trefle_api_token")
>>> Query = Client.search("rose").in_("plants").filter(family="Rosaceae").sort_by(slug="asc")
>>> Query.get_json()
"{'data': [{'id': 265580, 'common_name': 'Field rose', 'slug': 'rosa-arvensis', 'scientific_name': 'Rosa arvensis'..."
>>> New_Query = Query.range(year=[1980, 2010]).exclude(common_name="null")
>>> New_Query.get_models()
"[Plant(id=361066, name='', slug='erythranthe-lewisii',common_name='Purple monkeyflower', scientific_name='Erythranthe lewisii', year=2012,..."
```

