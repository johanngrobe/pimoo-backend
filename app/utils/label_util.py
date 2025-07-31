# Translation for ClimateImpactEnum values to German labels
KLIMACHECK_KLIMARELEVANZ_LABELS = {
    "positiv": "positiv",
    "negativ": "negativ",
    "kein_effekt": "keine Auswirkung",
}


KLIMACHECK_AUSWIRKUNG_LABELS = {
    -2: "stark negativ",
    -1: "negativ",
    1: "positiv",
    2: "stark positiv",
}


KLIMACHECK_AUSWIRKUNG_DAUER_LABELS = {
    "kurzfristig": "< 1 Jahr",
    "mittelfristig": "1-5 Jahre",
    "langfristig": "> 5 Jahre",
}


MOBILITAETSCHECK_AUSWIRKUNG_RAEUMLICH_LABELS = {
    "lokal": "lokal",
    "quartiersweit": "quartiersweit",
    "stadtweit": "stadtweit",
}


MOBILITAETSCHECK_AUSWIRKUNG_TICKMARK_LABELS = {
    "-3": "negativ",
    "0": "neutral",
    "3": "positiv",
}


def label_klimacheck_klimarelevanz(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    if value is None:
        return "Keine Angabe"
    return KLIMACHECK_KLIMARELEVANZ_LABELS.get(
        value, value
    )  # Fallback to the original value if not found


def label_klimacheck_auswirkung(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    if value is None:
        return "Keine Angabe"
    return KLIMACHECK_AUSWIRKUNG_LABELS.get(
        value, value
    )  # Fallback to the original value if not found


def label_klimacheck_auswirkung_dauer(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    if value is None:
        return "Keine Angabe"
    return KLIMACHECK_AUSWIRKUNG_DAUER_LABELS.get(
        value, value
    )  # Fallback to the original value if not found


def label_mobilitaetscheck_auswirkung_raeumlich(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    if value is None:
        return "Keine Angabe"
    return MOBILITAETSCHECK_AUSWIRKUNG_RAEUMLICH_LABELS.get(
        value, value
    )  # Fallback to the original value if not found


def label_mobilitaetscheck_auswirkung_tickmarks(value: str) -> str:
    """
    Translate the ClimateImpactEnum value into a readable German label.
    """
    if value is None:
        return "Keine Angabe"
    return MOBILITAETSCHECK_AUSWIRKUNG_TICKMARK_LABELS.get(
        value, value
    )  # Fallback to the original value if not found
