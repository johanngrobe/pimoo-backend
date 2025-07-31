from enum import Enum


class ImpactEnum(str, Enum):
    positiv = "positiv"
    negativ = "negativ"
    kein_effekt = "kein_effekt"


class ImpactDurationEnum(str, Enum):
    kurzfristig = "kurzfristig"
    mittelfristig = "mittelfristig"
    langfristig = "langfristig"


class SpatialImpactEnum(str, Enum):
    lokal = "lokal"
    quartiersweit = "quartiersweit"
    stadtweit = "stadtweit"
