import json
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Union

from .exceptions import TrefleException


class Result:
    def __init__(self, status_code: int, message: str = ''):
        """
        Result returned from low-level RestAdapter
        :param status_code: Standard HTTP Status code
        :param message: Human readable result
        """
        self.status_code = status_code
        self.message = str(message)


@dataclass
# unused should represent images in models
# [TODO] complete it
class ModelImage:
    id: int
    image_url: str
    copyright: str


@dataclass
class Kingdom:
    _category = "kingdoms"
    id: int
    name: str
    slug: str
    links: Dict

    @staticmethod
    def from_json(data) -> 'Kingdom':
        return Kingdom(**data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} {self.id=} {self.slug=}"


@dataclass
class SubKingdom(Kingdom):
    _category = "subkingdoms"
    kingdom: Kingdom

    @staticmethod
    def from_json(data) -> 'SubKingdom':
        kingdom = Kingdom.from_json(data.pop('kingdom'))
        return SubKingdom(kingdom=kingdom, **data)


@dataclass
class Division(Kingdom):
    _category = "divisions"
    subkingdom: SubKingdom

    @staticmethod
    def from_json(data) -> 'Division':
        subkingdom = SubKingdom.from_json(data.pop('subkingdom'))
        return Division(subkingdom=subkingdom, **data)


@dataclass
class DivisionClass(Kingdom):
    _category = "divisionclasses"
    division: Division

    @staticmethod
    def from_json(data) -> 'DivisionClass':
        division = Division.from_json(data.pop('division'))
        return DivisionClass(division=division, **data)


@dataclass
class DivisionOrder(Kingdom):
    _category = "divisionorders"
    division_class: DivisionClass

    @staticmethod
    def from_json(data) -> 'Kingdom':
        division_class = DivisionClass.from_json(data.pop('division_class'))
        return DivisionOrder(division_class=division_class, **data)


@dataclass
class Family(Kingdom):
    _category = "families"
    common_name: str
    division_order: Union[DivisionOrder, str] = None

    @staticmethod
    def from_json(data: Dict) -> 'Kingdom':
        division_order = data.pop('division_order', None)
        if isinstance(division_order, dict):
            division_order = DivisionOrder.from_json(division_order)
        return Family(division_order=division_order, **data)


@dataclass
class Genus(Kingdom):
    _category = "genus"
    family: Union[Family, str] = None

    @staticmethod
    def from_json(data) -> 'Kingdom':
        family = data.pop('family')
        if isinstance(family, dict):
            family = Family.from_json(family)
        return Genus(family=family, **data)


@dataclass
class Species(Kingdom):
    _category = "species"
    common_name: str
    scientific_name: str
    year: int
    bibliography: str
    author: str
    status: str
    rank: str
    family_common_name: str
    genus_id: str
    image_url: str
    genus: str
    family: str
    observations: Optional[str] = None
    vegetable: Optional[str] = None
    edible: Optional[bool] = None
    duration: Optional[List] = None
    edible_part: Optional[List] = None
    images: Optional[Dict] = None
    common_names: Optional[Dict] = None
    distribution: Optional[Dict] = None
    distributions: Optional[Dict] = None
    flower: Optional[Dict] = None
    foliage: Optional[Dict] = None
    fruit_or_seed: Optional[Dict] = None
    specifications: Optional[Dict] = None
    growth: Optional[Dict] = None
    synonyms: Optional[List[Dict]] = None
    sources: Optional[List[Dict]] = None

    @staticmethod
    def from_json(data) -> 'Species':
        data['name'] = ""
        return Species(**data)


@dataclass
class Plant(Kingdom):
    _category = "plants"
    common_name: str
    scientific_name: str
    year: int
    bibliography: str
    author: str
    family_common_name: str = None
    image_url: str = None
    genus_id: int = None
    status: str = None
    rank: str = None
    synonyms: List[str] = None
    vegetable: bool = None
    observations: str = None
    main_species: Union[Species, str] = None
    main_species_id: int = None
    genus: Union[Genus, str] = None
    family: Union[Family, str] = None
    species: List[Species] = None
    subspecies: List[Any] = None
    varieties: List[Any] = None
    hybrids: List[Any] = None
    forms: List[Any] = None
    subvarieties: List[Any] = None
    sources: List[Dict] = None

    @staticmethod
    def from_json(data: Dict) -> 'Kingdom':
        data['name'] = ""
        multi_species = []
        main_species = data.pop('main_species', None)
        genus = data.pop('genus', None)
        family = data.pop('family', None)
        species = data.pop('species', None)

        if species is not None:
            multi_species.append(Species.from_json(x) for x in species)

        return Plant(main_species=main_species, genus=genus, family=family,
                     species=multi_species, **data)


@dataclass
class Distribution(Kingdom):
    _category = "distributions"
    tdwg_code: str = None
    tdwg_level: str = None
    species_count: str = None
    parent: Any = None
    children: Any = None

    @staticmethod
    def from_json(data) -> 'Kingdom':
        parent = data.pop("parent", None)
        children = data.pop("children", None)
        if parent is not None:
            parent = Distribution(**parent)
        if children is not None:
            children = Distribution(**children)
        return Distribution(parent=parent, children=children, **data)


class Deserializer:
    def __init__(self) -> None:
        self.model = None
        self.field = None
        self.models_out = []

    def deserialize(self, model: type[Kingdom], json_string: str, field: Optional[str] = 'data'):
        self._set_model(model)
        self._set_field(field)
        data = json.loads(json_string, object_hook=self._custom_hook)
        if isinstance(data, list):
            self._return_multiple_instances(self.model, data)
            return self.models_out
        return model.from_json(data)

    def _custom_hook(self, obj):
        assert isinstance(obj, dict)
        if self.field is not None:
            if self.field not in obj:
                return obj
            return obj[self.field]
        else:
            raise TrefleException("Error no field found !")

    def _set_model(self, model):
        self.model = model

    def _set_field(self, field):
        self.field = field

    def _return_multiple_instances(self, model: Kingdom, data):
        try:
            for i in data:
                self.models_out.append(model.from_json(i))
            return True
        except Exception as e:
            raise TrefleException(f"error deserializing multiple instances of {model.__class__.__name__}") from e
