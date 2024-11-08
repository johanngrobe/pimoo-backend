from enum import Enum


class ImpactEnum(str, Enum):
    positive = "positive"
    negative = "negative"
    no_effect = "no_effect"


class ImpactDurationEnum(str, Enum):
    short = "short"
    medium = "medium"
    long = "long"


class SpatialImpactEnum(str, Enum):
    locally = "locally"
    districtwide = "districtwide"
    citywide = "citywide"


class RoleEnum(str, Enum):
    ADMINISTRATION = "administration"
    POLITICIAN = "politician"
