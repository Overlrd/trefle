from dataclasses import dataclass
from typing import List, Dict, Optional, Any
import json

from .exceptions import TrefleException


class Result:
    def __init__(self, status_code: int, message: str = '',
                 data: List[Dict] = None):
        """
        Result returned from low-level RestAdapter
        :param status_code: Standard HTTP Status code
        :param message: Human readable result
        :param data: Python List of Dictionaries (or
            maybe just a single Dictionary on error)
        """
        self.status_code = status_code
        self.message = str(message)
        self.data = data if data else []


@dataclass
class Kingdom:
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
    kingdom: Kingdom

    @staticmethod
    def from_json(data) -> 'SubKingdom':
        kingdom = Kingdom.from_json(data.pop('kingdom'))
        return SubKingdom(kingdom=kingdom, **data)


@dataclass
class Division(Kingdom):
    subkingdom: SubKingdom

    @staticmethod
    def from_json(data) -> 'Division':
        subkingdom = SubKingdom.from_json(data.pop('subkingdom'))
        return Division(subkingdom=subkingdom, **data)


@dataclass
class DivisionClass(Kingdom):
    division: Division

    @staticmethod
    def from_json(data) -> 'DivisionClass':
        division = Division.from_json(data.pop('division'))
        return DivisionClass(division=division, **data)


@dataclass
class DivisionOrder(Kingdom):
    division_class: DivisionClass

    @staticmethod
    def from_json(data) -> 'Kingdom':
        division_class = DivisionClass.from_json(data.pop('division_class'))
        return DivisionOrder(division_class=division_class, **data)


@dataclass
class Family(Kingdom):
    common_name: str
    division_order: Optional[DivisionOrder] = None

    @staticmethod
    def from_json(data) -> 'Kingdom':
        if 'division_order' in data:
            division_order = DivisionOrder.from_json(data.pop('division_order'))
        else:
            division_order = None
        return Family(division_order=division_order, **data)


@dataclass
class Genus(Kingdom):
    family: Optional[Family] = None

    @staticmethod
    def from_json(data) -> 'Kingdom':
        if 'family' in data:
            family = Family.from_json(data.pop('family'))
        else:
            family = None
        return Genus(family=family, **data)


@dataclass
class Species(Kingdom):
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
    observations: Optional[str]
    vegetable: Optional[str]
    edible: Optional[bool]
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
    common_name: str
    scientific_name: str
    main_species_id: int
    image_url: str
    year: int
    bibliography: str
    author: str
    family_common_name: str
    genus_id: int
    observations: str
    vegetable: bool
    main_species: Species
    genus: Genus
    family: Family
    species: List[Species]
    subspecies: List[Any]
    varieties: List[Any]
    hybrids: List[Any]
    forms: List[Any]
    subvarieties: List[Any]
    sources: List[Dict]

    @staticmethod
    def from_json(data) -> 'Kingdom':
        data['name'] = ""
        multi_species = []
        main_species = Species.from_json(data.pop('main_species'))
        genus = Genus.from_json(data.pop('genus'))
        family = Family.from_json(data.pop('family'))
        multi_species.append(Species.from_json(x) for x in data.pop('species'))
        return Plant(main_species=main_species, genus=genus, family=family,
                     species=multi_species, **data)


class Deserializer:
    def __init__(self) -> None:
        self.model = None
        self.field = None

    def deserialize(self, model: type[Kingdom], json_string: str, field: Optional[str] = 'data'):
        self._set_model(model)
        self._set_field(field)
        data = json.loads(json_string, object_hook=self.custom_hook)
        return model.from_json(data)

    def custom_hook(self, obj):
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
