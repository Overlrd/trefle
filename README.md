# Trefle-Api

*Trefle-API* is a simple python API wrapper for the [trefle](https://trefle.io./) botanic data API

```python
>>> from trefle_api import Trefle
>>> Client = Trefle(token="trefle_api_token")
>>> Query = Client.search("rose").in_("plants").filter(family="Rosaceae").sort_by(slug="asc")
>>> Query.get_json()
"{'data': [{'id': 265580, 'common_name': 'Field rose', 'slug': 'rosa-arvensis', 'scientific_name': 'Rosa arvensis'..."
>>> New_Query = Query.range(year=[2000, 2010]).exclude(common_name="null")
>>> New_Query.get_models()
"[[Plant(id=345576, name='', slug='physaria-purpurea', common_name='Rose bladderpod', scientific_name='Physaria purpurea', year=2002,..."
```

This package allows you to build simple to more complex queries to fetch data from the the [trefle](https://trefle.io./) RESTAPI <br>
Query tags :
 - `search()`
    <br> description : search a query  
    args : __q__ # **the string to use as query**
    returns : a copy of the `Query` class to allow chaining
 - `retrieve()`
    <br> description : retrieve an item based on it's slug or id  
    args : __slug__ or __id__ # a string representing the slug of a vegetable or it's id in the trefle api records  
    returns : a copy of the `Query` class to allow chaining

- `in_()`
 <br> description : select a category in which to search or retrieve  
 args __category__ # available categories are : 
  - kingdoms
  - subkingdoms
  - divisions
  - divisionclasses
  - division_orders
  - families
  - genus
  - plants
  - species

