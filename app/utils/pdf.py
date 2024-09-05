def get_color(wirkung, tangiert=True):
    """
    Definiert die Farbe eines Ziels auf dem PDF, je nachdem wie die Wirkung einer Maßnahme auf ein Ziel ist

    Args:
        wirkung (int): Wirkung einer Maßnahme auf ein Ziel
        tangiert (bool, optional): Ob ein Ziel tangiert ist oder nicht. Defaults to True.

    Returns:
        list: Liste mit RGB-Werten
    """
    if not tangiert:
        return [229, 229, 229]

    if wirkung <= -2.5:
        return [255, 16, 16]
    elif wirkung <= -1.5:
        return [255, 95, 95]
    elif wirkung < 0: 
        return [255, 175, 175]
    elif wirkung == 0:
        return [255,255,255]
    elif wirkung <= 0.5: 
        return [176, 222, 171]
    elif wirkung <= 1.5: 
        return [97, 189, 88]
    elif wirkung > 1.5: 
        return [18, 157, 5]
    

def convert_wirkung(num, tangiert=True):
    """
    Konvertiert die Wirkungsrichtung und -Stärke in eine Textbeschreibung

    Args:
        num (int): Wirkungsrichtung und -Stärke
        tangiert (bool, optional): Ob ein Ziel tangiert ist oder nicht. Defaults to True.

    Returns:
        str: Textbeschreibung der Wirkungsrichtung und -Stärke
    """

    if not tangiert:
        return "Ziel nicht tangiert"
    
    conversion = ""

    if num < -2.5:
        conversion = "stark negativ"
    elif num <= -1.5:
        conversion = "negativ"
    elif num < 0:
        conversion = "leicht negativ"
    elif num == 0:
        conversion = "neutral"
    elif num <= 0.5:
        conversion = "leicht positiv"
    elif num <= 1.5:
        conversion = "positiv"
    elif num > 1.5:
        conversion = "stark positiv"
    else:
        conversion = "keine Angabe"

    return conversion

def summarize_wirkung():
    """
    Arithmeritsches Mittel der Unterziele berechnen

    Returns:
        DataFrame: DataFrame mit arithmetischem Mittel der Unterziele
    """
    df_ampel = st.session_state['df_ziele'][st.session_state['df_ziele']['kat'] == 'Leitziel'][['name']]
    df_ampel.index = df_ampel.index.astype(int)
    df_agg = st.session_state['df_ziele'][st.session_state['df_ziele']['kat'] == 'Unterziel'].groupby('leitziel')[['tangiert', 'wirkung']].sum()
    df_agg = df_ampel.join(df_agg)
    df_agg['mean'] = df_agg['wirkung']/df_agg['tangiert']

    return df_agg