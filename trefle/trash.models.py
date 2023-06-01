class Image:
    def __init__(self, id: int, image_url: str, copyright: str) -> None:
        self.id = id
        self.image_url = image_url
        self.copyright = copyright

class Images:
    def __init__(
        self,
        flower: List[Image],
        leaf: List[Image],
        habit: List[Image],
        fruit: List[Image],
        bark: List[Image],
        other: List[Image],
    ) -> None:
        self.flower = flower
        self.leaf = leaf 
        self.habit = habit
        self.fruit = fruit 
        self.bark = bark 
        self.other = other 
        
"""
    Data models representing objects from the trefle api .
    The whole API structure is defined by the following classification:


    Kingdom
    -> Subkingdom
        -> Division
        -> Division class
            -> Division order
            -> Family
                -> Genus
                -> Plant
                    -> Species

    check https://docs.trefle.io/docs/guides/getting-started#the-trefle-structure

"""

class Kingdom:
    def __init__(self, 
            id: int,
            slug: str, 
            common_name: str = '', 
            name: str = '',
            scientific_name: str = '', 
            bibliography: str = '',
            author: str = '', 
            year: int = 0,
            links: dict = None,
                ) -> None:

        self.id = id
        self.name = name
        self.slug = slug
        self.common_name = common_name
        self.scientific_name = scientific_name
        self.bibliography = bibliography
        self.author = author
        self.year = year

    def __repr__(self):
        return f"{self.__class__.__name__} {self.id=} {self.scientific_name=} {self.common_name=}"


class SubKingdom(Kingdom):
    def __init__(self, id: int, name: str, slug: str, kingdom: Kingdom, **kwargs) -> None:
        super().__init__(id=id, name=name, slug=slug)
        self.kingdom = kingdom


class Division(Kingdom):
    def __init__(self, id: int, name: str, slug: str, subkingdom: SubKingdom, **kwargs) -> None:
        super().__init__(id=id, name=name, slug=slug)
        self.subkingdom = subkingdom


class DivisionClass(Kingdom):
    def __init__(self, id: int, name: str, slug: str,
                 division: Division, **kwargs) -> None:
        super().__init__(id=id, name=name, slug=slug)
        self.division = division


class DivisionOrder(Kingdom):
    def __init__(self, id: int, name: str, slug: str,
                 division_class: DivisionClass, **kwargs) -> None:
        super().__init__(id=id, name=name, slug=slug)
        self.division_class = division_class


class Family(Kingdom):
    def __init__(self, id: int, name: str, common_name: str, slug: str,
                 division_order: DivisionOrder = '', **kwargs) -> None:
        super().__init__(id=id, name=name, slug=slug, common_name=common_name)
        self.division_order = division_order


class Genus(Kingdom):
    def __init__(self, id: int, name: str, slug: str,
                 family: Family = '', **kwargs) -> None:
        super().__init__(id=id, name=name, slug=slug)
        self.family = family
        self.__dict__.update(kwargs)


class Species(Kingdom):
    def __init__(
        self,
        id: int,
        genus: Genus,
        family: Family,
        images: Images,
        duration=None,
        edible_part=None,
        vegetable=None,
        common_name: str = "",
        slug: str = "",
        scientific_name: str = "",
        year: int = 0,
        bibliography: str = "",
        author: str = "",
        status: str = "",
        rank: str = "",
        family_common_name: str = "",
        genus_id: int = 0,
        observations: str = "",
        image_url: str = "",
        edible: bool = "",
        common_names: Dict[str, List[str]] = "",
        **kwargs,
    ) -> None:
        super().__init__(
            id=id,
            common_name=common_name,
            scientific_name=scientific_name,
            slug=slug,
            bibliography=bibliography,
            author=author,
            year=year,
        )
        self.status = status
        self.rank = rank
        self.family_common_name = family_common_name
        self.genus_id = genus_id
        self.observations = observations
        self.vegetable = vegetable
        self.image_url = image_url
        self.genus = genus
        self.family = family
        self.duration = duration
        self.edible_part = edible_part
        self.edible = edible
        self.images = images
        self.common_names = common_names
        self.__dict__.update(kwargs)



class Plant(Kingdom):
    """
    A plant is the main species of a species, without all the forms, varieties, subspecies etc...\n
    For each plant, we have one main species and several other "sub" species (which can be subspecies, varieties,
    hybrids, cultivars etc...).\n
    Refer to \n https://docs.trefle.io/docs/guides/getting-started/#plant-and-species
    """

    def __init__(self, id: int, common_name: str, slug: str,
                 scientific_name: str, main_species_id: int, image_url: str,
                 year: int, bibliography: str, author: str,
                 family_common_name: str, genus_id: int, observations: str,
                 vegetable: bool, main_species: Species,
                 genus: Genus, family: Family, species: List[Species], **kwargs) -> None:
        super().__init__(id=id, common_name=common_name, scientific_name=scientific_name, slug=slug,
                         bibliography=bibliography, author=author, year=year)
        self.main_species_id = main_species_id
        self.image_url = image_url
        self.family_common_name = family_common_name
        self.genus_id = genus_id
        self.observations = observations
        self.vegetable = vegetable
        self.main_species = main_species
        self.genus = genus
        self.family = family
        self.species = species



class Serializer:
    """
    Convert JSON data into Python objects, passing required fields in mapping
    models.
    """
    def __init__(self, model, filepath='', data=None, models=None):
        self.model = model
        self.data = self._read_file(filepath) if data is None else data
        self.models = models or [Kingdom, SubKingdom, Division, DivisionOrder,
                                 DivisionClass, Family, Genus, Species, Plant]
        self.instance_list = {}
        self.merged_data = {}

    @staticmethod
    def _read_file(filepath: str, field: str = 'data') -> dict:
        with open(filepath, 'r') as file:
            filedata = json.load(file)
        return filedata.get(field, {})

    def _serialize_value(self, value):
        if isinstance(value, list):
            return [self._serialize_value(x) for x in value]
        else:
            return value

    def serialize(self, data=None):
        data = data or self.data
        for key, value in data.items():
            for model in self.models:
                instance_name = model.__name__.lower()
                if isinstance(value, dict) and instance_name in [key,f"main_{key}"]:
                    print(f"field {key} {type(value)}, match {instance_name}")
                    self.instance_list[instance_name] = model(**value)
                elif isinstance(value, list) and instance_name == key:
                    print(f"field {key} {type(value)}, match {instance_name}")
                    multiple_instances = []
                    for i in value:
                        if isinstance(i, dict):
                            multiple_instances.append(model(**self._serialize_value(i)))
                    self.instance_list[instance_name] = multiple_instances

        self.merged_data = {**data, **self.instance_list}
        instance = self.model(**self.merged_data)
        return instance
