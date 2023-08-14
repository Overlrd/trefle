API_SETTINGS = {
    'title': 'Trefle API v1',
    'version': '1.6.0',
    'url': 'https://trefle.io/api/{version}',
    'routes': {
        'listKingdoms': {
            'method': 'get',
            'path': '/kingdoms',
            'params': ['page']
        },
        'getKingdoms': {
            'method': 'get',
            'path': '/kingdoms/{id}',
            'params': ['id-required']
        },
        'listSubkingdoms': {
            'method': 'get',
            'path': '/subkingdoms',
            'params': ['page']
        },
        'getSubkingdoms': {
            'method': 'get',
            'path': '/subkingdoms/{id}',
            'params': ['id-required']
        },
        'listDivisions': {
            'method': 'get',
            'path': '/divisions',
            'params': ['page']
        },
        'getDivisions': {
            'method': 'get',
            'path': '/divisions/{id}',
            'params': ['id-required']
        },
        'listDivisionClasses': {
            'method': 'get',
            'path': '/division_classes',
            'params': ['page']
        },
        'getDivisionClasses': {
            'method': 'get',
            'path': '/division_classes{id}',
            'params': ['id-required']
        },
        'listDivisionOrders': {
            'method': 'get',
            'path': '/division_orders',
            'params': ['page']
        },
        'getDivisionOrders': {
            'method': 'get',
            'path': '/division_orders/{id}',
            'params': ['id-required']
        },
        'listFamilies': {
            'method': 'get',
            'path': '/families',
            'params': ['page']
        },
        'getFamilies': {
            'method': 'get',
            'path': '/families/{id}',
            'params': ['id-required']
        },
        'listGenus': {
            'method': 'get',
            'path': '/genus',
            'params': ['page', 'filter', 'order']
        },
        'getGenus': {
            'method': 'get',
            'path': '/genus/{id}',
            'params': ['id-required']
        },
        'listPlants': {
            'method': 'get',
            'path': '/plants',
            'params': ['page', 'range', 'order', 'filter_not', 'filter']
        },
        'getPlants': {
            'method': 'get',
            'path': '/plants/{id}',
            'params': ['id-required']
        },
        'searchPlants': {
            'method': 'get',
            'path': '/plants/search',
            'params': ['page', 'range', 'order', 'filter_not', 'filter', 'q-required']
        },
        'listSpecies': {
            'method': 'get',
            'path': '/species',
            'params': ['page', 'range', 'order', 'filter_not', 'filter']
        },
        'getSpecies': {
            'method': 'get',
            'path': '/species/{id}',
            'params': ['id-required']
        },
        'searchSpecies': {
            'method': 'get',
            'path': '/species/search',
            'params': ['page', 'range', 'order', 'filter_not', 'filter', 'q-required']
        },
        'listDistributions': {
            'method': 'get',
            'path': '/distributions',
            'params': ['page']
        },
        'getDistributions': {
            'method': 'get',
            'path': '/distributions/{id}',
            'params': ['id-required']
        }
    }
}
