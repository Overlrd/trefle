from dataclasses import dataclass, field
import json
from typing import List, Dict, Optional, Any


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

@dataclass(kw_only=True)
class Kingdom:
    """
    Represents the kingdom object
    https://docs.trefle.io/reference/#tag/Kingdoms
    """
    id: int 
    name: str = ""
    slug: str
    links: dict



@dataclass
class SubKingdom(Kingdom):
    kingdom: Kingdom


@dataclass
class Division(Kingdom):
    subkingdom: SubKingdom


@dataclass 
class DivisionClass(Kingdom):
    division: Division


@dataclass 
class DivisionOrder(Kingdom):
    division_class: DivisionClass


@dataclass
class Family(Kingdom):
    common_name: str
    division_order: DivisionOrder


@dataclass 
class Genus(Kingdom):
    family:Family


@dataclass 
class Plant(Kingdom):
    common_name: None
    image_url: None
    scientific_name: Optional[str] = None
    main_species_id: Optional[int] = None
    year: Optional[int] = None
    bibliography: Optional[str] = None
    author: Optional[str] = None
    family_common_name: Optional[str] = None
    genus_id: Optional[int] = None
    observations: Optional[str] = None
    vegetable: Optional[bool] = None
    main_species: Optional = None
    genus: Optional[Genus] = None
    family: Optional[Family] = None
    species: Optional = None
    subspecies: Optional[List[Any]] = None
    varieties: Optional[List[Any]] = None
    hybrids: Optional[List[Any]] = None
    forms: Optional[List[Any]] = None
    subvarieties: Optional[List[Any]] = None
    sources: Optional[List[Dict]] = None

@dataclass 
class Species(Kingdom):
    duration: None
    edible_part: None
    common_name: Optional[str] = None
    scientific_name: Optional[str] = None
    year: Optional[int] = None
    bibliography: Optional[str] = None
    author: Optional[str] = None
    status: Optional[str] = None
    rank: Optional[str] = None
    family_common_name: Optional[str] = None
    genus_id: Optional[int] = None
    observations: Optional[str] = None
    vegetable: Optional[bool] = None
    image_url: Optional[str] = None
    genus: Optional[str] = None
    family: Optional[str] = None
    edible: Optional[bool] = None
    images: Optional[Images] = None
    common_names: Optional[Dict[str, List[str]]] = None
    distribution: Optional[Distribution] = None
    distributions: Optional[Distributions] = None
    flower: Optional[Flower] = None
    foliage: Optional[Foliage] = None
    fruit_or_seed: Optional[FruitOrSeed] = None
    specifications: Optional[Specifications] = None
    growth: Optional[Growth] = None
    links: Optional[DataLinks] = None
    synonyms: Optional[List[Synonym]] = None
    sources: Optional[List[Source]] = None
