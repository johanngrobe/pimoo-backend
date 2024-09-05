# Translation for ClimateImpactEnum values to German labels
CLIMATE_IMPACT_LABELS = {
    "positive": "positiv",
    "negative": "negativ",
    "no_effect": "keine Auswirkung"
}

CLIMATE_IMPACT_GHG_LABELS ={
        -2: 'stark negativ',
        -1: 'negativ',
        1: 'positiv',
        2: 'stark positiv'
    }

CLIMATE_IMPACT_DURATION_LABELS = {
    "short": '< 1 Jahr',
    "medium": '1-5 Jahre',
    "long": '> 5 Jahre'
}


MOBILITY_SPATIAL_IMPACT_LABELS = {
    'locally': 'lokal',
    'districtwide': 'Quartier/Stadtteil',
    'citywide': 'Stadt'
}

MOBILITY_IMPACT_TICKMARK_LABELS = {
    "-3": 'negativ',
    "0": 'neutral',
    "3": 'positiv'
    }

def label_climate_impact(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    return CLIMATE_IMPACT_LABELS.get(value, value)  # Fallback to the original value if not found


def label_climate_impact_ghg(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    return CLIMATE_IMPACT_GHG_LABELS.get(value, value)  # Fallback to the original value if not found

def label_climate_impact_duration(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    return CLIMATE_IMPACT_DURATION_LABELS.get(value, value)  # Fallback to the original value if not found

def label_mobility_spatial_impact(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    return MOBILITY_SPATIAL_IMPACT_LABELS.get(value, value)  # Fallback to the original value if not found

def label_mobility_impact(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    return MOBILITY_IMPACT_TICKMARK_LABELS.get(value, value)  # Fallback to the original value if not found

