# Translation for ClimateImpactEnum values to German labels
CLIMATE_IMPACT_LABELS = {
    "positiv": "positiv",
    "negativ": "negativ",
    "kein_effekt": "keine Auswirkung",
}


CLIMATE_IMPACT_GHG_LABELS = {
    -2: "stark negativ",
    -1: "negativ",
    1: "positiv",
    2: "stark positiv",
}


CLIMATE_IMPACT_DURATION_LABELS = {
    "kurzfristig": "< 1 Jahr",
    "mittelfristig": "1-5 Jahre",
    "langfristig": "> 5 Jahre",
}


MOBILITY_SPATIAL_IMPACT_LABELS = {
    "lokal": "lokal",
    "quartiersweit": "quartiersweit",
    "stadtweit": "stadtweit",
}


MOBILITY_IMPACT_TICKMARK_LABELS = {"-3": "negativ", "0": "neutral", "3": "positiv"}


def label_climate_impact(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    if value is None:
        return "Keine Angabe"
    return CLIMATE_IMPACT_LABELS.get(
        value, value
    )  # Fallback to the original value if not found


def label_climate_impact_ghg(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    if value is None:
        return "Keine Angabe"
    return CLIMATE_IMPACT_GHG_LABELS.get(
        value, value
    )  # Fallback to the original value if not found


def label_climate_impact_duration(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    if value is None:
        return "Keine Angabe"
    return CLIMATE_IMPACT_DURATION_LABELS.get(
        value, value
    )  # Fallback to the original value if not found


def label_mobility_spatial_impact(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    if value is None:
        return "Keine Angabe"
    return MOBILITY_SPATIAL_IMPACT_LABELS.get(
        value, value
    )  # Fallback to the original value if not found


def label_mobility_impact(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    if value is None:
        return "Keine Angabe"
    return MOBILITY_IMPACT_TICKMARK_LABELS.get(
        value, value
    )  # Fallback to the original value if not found
