from app.src.export.custom_FPDF import FPDF
from ... import schemas
import pandas as pd
import numpy as np

def mobility_submission_to_pdf(submission: schemas.MobilitySubmissionOut):
    """
    Automatisches generieren einer PDF

    Returns:
        bytes: PDF-File
    """
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_font('helvetica', 'B',16)
    pdf.cell(0, 10, 'Mobilitätscheck für Magistratsvorlagen', border=False, align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', '', 10)

    pdf.cell(52,5, txt="**Magistratsvorlagennummer:**", markdown=True)
    pdf.cell(0,5, txt=f"{submission.submission_no}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(52,5, txt="**Datum der Magistratssitzung:**", markdown=True)
    pdf.cell(0,5, txt=f"{submission.submission_date.strftime('%d.%m.%Y')}" , new_x="LMARGIN",new_y="NEXT")
    pdf.cell(30,5, txt="**Maßnahme:**", markdown=True)
    pdf.multi_cell(0,5, txt=F"{submission.title}",new_x="LMARGIN", new_y="NEXT")
    pdf.cell(30,5, txt="**Beschreibung:**", markdown=True)
    pdf.multi_cell(0,5, txt=f"{submission.desc}",new_x="LMARGIN", new_y="NEXT")
    pdf.cell(30,5, txt="**Bearbeitet durch:**", markdown=True)
    pdf.cell(0,5, txt=f"{submission.author}", new_x="LMARGIN",new_y="NEXT")


    pdf.cell(0,3, new_x="LMARGIN", new_y="NEXT")

    # TODO summazize_impact überarbeiten, da noch mit Pandas gearbeitet wird
    df_ampel = summarize_wirkung()

    box_x = pdf.get_x()
    box_y = pdf.get_y()
    
    pdf.cell(0, 10, '**Zielampel laut verkehrlichem Leitbild**', markdown=True, align='L', new_x="LMARGIN", new_y="NEXT")
    pdf.image('pictures/legende.png', box_x+115, box_y + 3, 70)
    pdf.set_font('helvetica', '', 10)
    
    for ind in df_ampel.index:
        leitziel_name = df_ampel['name'][ind]
        leitziel_tangiert = df_ampel['tangiert'][ind]
        leitziel_wirkung = df_ampel['wirkung'][ind]
        color = get_color(leitziel_wirkung, leitziel_tangiert)
        pdf.set_fill_color(r= color[0], g=color[1], b =color[2])
        pdf.cell(0,8, txt=f"{ind}. {leitziel_name}", markdown=True, fill=True,  new_y="NExT", new_x="LMARGIN")
    box_h = pdf.get_y() - box_y
    pdf.rect(box_x, box_y, pdf.epw, box_h)

    submission.results

    df = st.session_state['df_ziele']

    # Alle Ziele und Unterziele werden angezeigt
    print_df = df
    print_unterziele = print_df[print_df['kat'] == 'Unterziel']
    print_leitziele = df_ampel

    # Nur tangierte Ziele und Unterziele werden angezeigt
    # print_df = df[df['tangiert'] == True]
    # print_unterziele = print_df[print_df['kat'] == 'Unterziel']
    # print_leitziele = df_ampel[df_ampel['tangiert'] > 0]

    pdf.set_font('helvetica', '', 11)
    pdf.cell(0, 5, new_x="LMARGIN", new_y="NEXT")

    for ind_leitziel in print_leitziele.index:

        leitziel_name = print_leitziele['name'][ind_leitziel]
        leitziel_tangiert = print_leitziele['tangiert'][ind_leitziel]
        leitziel_wirkung = print_leitziele['mean'][ind_leitziel]

        pdf.cell(10,10, txt=f"**{int(ind_leitziel)}**", markdown=True, border="TL")
        pdf.multi_cell(145,10, txt=f"**{leitziel_name}**", markdown=True, border="TR", max_line_height=5, new_y="TOP")
        color = get_color(leitziel_wirkung, leitziel_tangiert)
        pdf.set_fill_color(r= color[0], g=color[1], b =color[2])
        pdf.multi_cell(35,10, txt=f"**Gesamtwirkung:** \n{convert_wirkung(leitziel_wirkung)}", markdown=True, fill=True, border="TBR", max_line_height=5, new_x="LMARGIN", new_y="NEXT")

        for ind in print_unterziele.index:
            if ind_leitziel == print_unterziele['leitziel'][ind]:

                unterziel_name = print_unterziele['name'][ind]
                unterziel_tangiert = print_unterziele['tangiert'][ind]
                unterziel_wirkung = print_unterziele['wirkung'][ind]
                unterziel_wirkung_text = convert_wirkung(unterziel_wirkung, unterziel_tangiert)
                unterziel_raeumlich = print_unterziele['wirkung_raeumlich'][ind]
                unterziel_desc = print_unterziele['erlaeuterung'][ind]
                unterziel_indikatoren = print_unterziele['indikatoren'][ind]

                if unterziel_tangiert:
                    pdf.cell(10, 10, txt=f"{ind}", markdown=True, border="T")
                    pdf.multi_cell(145,10, txt=f"{unterziel_name}", markdown=True, max_line_height=5, border="T", new_y="TOP")
                    color = get_color(unterziel_wirkung, unterziel_tangiert)
                    pdf.set_fill_color(r= color[0], g=color[1], b =color[2])
                    pdf.multi_cell(35,10, txt=f"**Wirkung:**\n{unterziel_wirkung_text}", markdown=True,border="LT",max_line_height=5, fill=True, new_x="LEFT", new_y="NEXT")
                    pdf.multi_cell(35,15, txt=f"\n**Räumlich:**\n{unterziel_raeumlich}", markdown=True, border="L",max_line_height=5, new_x="LMARGIN", new_y="TOP")
                    pdf.cell(10, 5)
                    pdf.multi_cell(145,5,txt=f"**Erläuterung:** {unterziel_desc} \n\n**Indikatoren:** {', '.join(unterziel_indikatoren)}", markdown=True,border="R", new_x="LMARGIN", new_y="NEXT")
                else:
                    pdf.cell(10, 10, txt=f"{ind}", markdown=True, border="T")
                    pdf.multi_cell(145,10, txt=f"{unterziel_name}", markdown=True, max_line_height=5, border="T", new_y="TOP")
                    color = get_color(unterziel_wirkung, unterziel_tangiert)
                    pdf.set_fill_color(r= color[0], g=color[1], b =color[2])
                    pdf.multi_cell(35,10, txt=f"**Wirkung:**\n{unterziel_wirkung_text}", markdown=True,border="LT",max_line_height=5, fill=True, new_x="LMARGIN", new_y="NEXT")

        pdf.cell(0, 8, new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())



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