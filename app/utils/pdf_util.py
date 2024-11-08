def get_display_impact(value, target):
    """
    Konvertiert die Wirkungsrichtung und -Stärke in eine Textbeschreibung

    Args:
        num (int): Wirkungsrichtung und -Stärke
        tangiert (bool, optional): Ob ein Ziel tangiert ist oder nicht. Defaults to True.

    Returns:
        str: Textbeschreibung der Wirkungsrichtung und -Stärke
    """
    if not target:
        return {"label": "Ziel nicht tangiert",
                "color": {"r": 229, "g": 229, "b": 229}}

    if value < -2.5:
        return {"label": "stark negativ",
                "color": {"r": 255, "g": 16, "b": 16}}
    elif value <= -1.5:
        return {"label": "negativ",
                "color": {"r": 255, "g": 95, "b": 95}}
    elif value < 0:
        return {"label": "leicht negativ",
                "color": {"r": 255, "g": 175, "b": 175}}
    elif value == 0:
        return {"label": "neutral",
                "color": {"r": 255, "g": 255, "b": 255}}
    elif value <= 0.5:
        return {"label": "leicht positiv",
                "color": {"r": 176, "g": 222, "b": 171}}
    elif value <= 1.5:
        return {"label": "positiv",
                "color": {"r": 97, "g": 189, "b": 88}}
    elif value > 1.5:
        return {"label": "stark positiv",
                "color": {"r": 18, "g": 157, "b": 5}}
    else:
        return {"label": "keine Angabe",
                "color": {"r":None, "g":None, "b":None}}

    # if not target:
    #     return {"label": "Ziel nicht tangiert",
    #             "color": [229, 229, 229]}

    # if value < -2.5:
    #     return {"label": "stark negativ",
    #             "color": [255, 16, 16]}
    # elif value <= -1.5:
    #     return {"label": "negativ",
    #             "color": [255, 95, 95]}
    # elif value < 0:
    #     return {"label": "leicht negativ",
    #             "color": [255, 175, 175]}
    # elif value == 0:
    #     return {"label": "neutral",
    #             "color": [255,255,255]}
    # elif value <= 0.5:
    #     return {"label": "leicht positiv",
    #             "color": [176, 222, 171]}
    # elif value <= 1.5:
    #     return {"label": "positiv",
    #             "color": [97, 189, 88]}
    # elif value > 1.5:
    #     return {"label": "stark positiv",
    #             "color": [18, 157, 5]}
    # else:
    #     return {"label": "keine Angabe",
    #             "color": None}

def calculate_average_impact(data):

    """
    This function calculates the average impact of sub-objectives where target=True,
    grouped by their main objective, if the main objective's target is also True.
    
    Parameters:
    data (dict): The data structure containing objectives and sub-objectives.

    Returns:
    dict: A dictionary with main_objective_id as keys and the average impact as values.
    """
    average_impact = {}
    
    # Iterating through the main objectives
    for objective in data.objectives:
        if objective.target:
            # Filter sub-objectives with target=True
            sub_objectives = [sub_obj for sub_obj in objective.sub_objectives if sub_obj.target]
            
            # Sum the impacts of the sub-objectives
            total_impact = sum(sub_obj.impact for sub_obj in sub_objectives if sub_obj.impact is not None)
            
            # Calculate the average impact if there are sub-objectives with target=True
            if sub_objectives:
                average_impact[objective.main_objective_id] = total_impact / len(sub_objectives)
        else:
            average_impact[objective.main_objective_id] = None

    return average_impact