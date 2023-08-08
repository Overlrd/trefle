# Trefle-Api

*Trefle-API* is a simple python API wrapper for the [trefle](https://trefle.io./) botanic data API

```python
>>> from trefleapi import Client
>>> Query = Client(token=token)
>>> query = Query.search("rose").in_("plants").filter(family="Rosaceae").sort_by(slug="asc")
>>> query.get_json()
"{'data': [{'id': 265580, 'common_name': 'Field rose', 'slug': 'rosa-arvensis', 'scientific_name': 'Rosa arvensis'..."
>>> New_Query = query.range(year=[2000, 2010]).exclude(common_name="null")
>>> New_Query.get_models()
"[[Plant(id=345576, name='', slug='physaria-purpurea', common_name='Rose bladderpod', scientific_name='Physaria purpurea', year=2002,..."
```

This package allows you to build simple to more complex queries to fetch data from the [Trefle](https://trefle.io/) REST API.

## Query tags:

- `search()`
  - Description: Search a query.
  - Args:
    - `q`: The string to use as a query.
  - Returns: A copy of the `Query` class to allow chaining.
- `list()`
  - Description: List plants of a category
  - Args:
    - `category`: Check the list of [available categories](#Available-Categories).
- `retrieve()`
  - Description: Retrieve an item based on its slug or ID.
  - Args:
    - `slug` or `id`: A string representing the slug of a vegetable or its ID in the Trefle API records.
  - Returns: A copy of the `Query` class to allow chaining.

- `in_()`
  - Description: Select a category in which to search or retrieve.
  - Args:
    - `category`: Check the list of [available categories](#Available-Categories).

- `filter()`
  - Description: Filter the search or retrieval results based on specific criteria.
  - Args:
    - `**kwargs`: Key-value pairs representing the filtering criteria. The available criteria depend on the specific attributes or properties of the items being searched or retrieved.
  - Returns: A copy of the `Query` class to allow chaining with other methods.

- `exclude()`
  - Description: Exclude specific items from the search or retrieval results based on given criteria.
  - Args:
    - `**kwargs`: Key-value pairs representing the exclusion criteria. The available criteria depend on the specific attributes or properties of the items being searched or retrieved.
  - Returns: A copy of the `Query` class to allow chaining with other methods.

- `sort_by()`
  - Description: Sort the search or retrieval results based on a specified attribute or property.
  - Args:
    - `attribute`: The attribute or property based on which the results should be sorted.
  - Returns: A copy of the `Query` class to allow chaining with other methods.

- `range()`
  - Description: Limit the search or retrieval results to a specific range of values for a given attribute or property.
  - Args:
    - `attribute`: The attribute or property on which the range should be applied.
    - `list`: A list specifying the range. It takes two elements: the minimum value (inclusive) and the maximum value (inclusive).
  - Returns: A copy of the `Query` class to allow chaining with other methods.

- `get_json()`
  - Description: This function retrieves the JSON response of the API for the current query. It breaks the chaining of methods and returns the JSON data.
  - Args: None
  - Returns: The JSON response of the API.

- `get_models()`
  - Description: This function retrieves a list of data models containing the response items for the current query. It breaks the chaining of methods and returns the list of data models.
  - Args: None
  - Returns: A list of data models containing the response items.

Please note that both get_json() and get_models() functions should be called at the end of the query chain to retrieve the desired results. These functions break the chaining because they return the final results instead of a copy of the Query class.

## Specificities

The following are specificities of the query functionalities:

- **Limitation on calling 'search' and 'list' together**: It is not necessary to call both 'search' and 'list' methods in the same query. These methods serve different purposes and calling them together may lead to redundant or conflicting results.

- **Redundancy of using 'in_' after 'list'**: When using the 'list' method, it already accepts a category as a parameter. Therefore, it is redundant to subsequently call the 'in_' method to specify the category. The category provided in the 'list' method already takes care of filtering the results based on the desired category.

Please keep these specificities in mind to ensure optimal usage and avoid unnecessary method calls that may result in unintended consequences or redundant operations.

## Available Categories

The following are the available categories representing items in the vegetable (plants) world:

- **Kingdoms**: Represents the kingdoms of plants. (e.g., "Plantae")

- **Subkingdoms**: Represents the subkingdoms of plants.

- **Divisions**: Represents the divisions of plants.

- **Division Classes**: Represents the classes within plant divisions.

- **Division Orders**: Represents the orders within plant divisions.

- **Families**: Represents the families of plants.

- **Genus**: Represents the genus of plants.

- **Plants**: Represents individual plants.

- **Species**: Represents the species of plants.

- **Distributions**: Represents the geographic distributions of plants.

Please note that categories should be passed only in the `list` method or the `.in_` method. The '.in_' method allows selecting a specific category in which to search or retrieve items.

These categories provide a way to organize and classify different aspects of the vegetable world, allowing for more targeted queries and retrieval of specific plant-related information.
