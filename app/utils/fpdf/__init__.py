from fpdf import FPDF
import datetime
import os
import io
from pathlib import Path
from .pdf_utils import get_display_impact, calculcate_average_impact
from ..label import label_climate_impact, label_climate_impact_duration, label_climate_impact_ghg, label_mobility_impact, label_mobility_spatial_impact

class FPDF(FPDF):

    def __init__(self, orientation='P', unit='mm', format='A4'):
        # Pass the parameters to FPDF's __init__ method
        super().__init__(orientation, unit, format)
        font_path = os.path.dirname(os.path.abspath(__file__))
        self.add_font("free-sans", style="", fname=os.path.join(font_path, './assests/FreeSans/FreeSans.ttf'))
        self.add_font("free-sans", style="b", fname=os.path.join(font_path, './assests/FreeSans/FreeSansBold.ttf'))
        self.add_font("free-sans", style="i", fname=os.path.join(font_path, './assests/FreeSans/FreeSansOblique.ttf'))
        self.add_font("free-sans", style="bi", fname=os.path.join(font_path, './assests/FreeSans/FreeSansBoldOblique.ttf'))

    def header(self):
        # Get the absolute path to the image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, './assests/pimoo_3logos.png')  # Navigate to assets
        
        # Normalize the path for compatibility
        image_path = os.path.normpath(image_path)
        try:
            self.image(image_path, 10, 8, 100)
        except Exception as e:
            print(e)
        self.set_font('free-sans', '',10)
        self.cell(0, 8, f"{datetime.date.today().strftime('%d.%m.%Y')}", align='R')
        self.ln(15)

    def footer(self):
        self.set_y(-20)
        self.set_font('free-sans', '', 8)
        self.cell(0, 10, 'Hinweis: Die zu den Indiaktoren zugehörigen Dokumente finden Sie alle im Wissensspeicher', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 10, f"Seite {self.page_no()}/{{nb}}", align="C")

    def export_climate_submission(self, submission):
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True, margin=20)
        self.add_page()
        # Different styles of the same font family.
        self.set_font('free-sans', 'B',16)
        self.cell(0, 10, 'Klimacheck für Magistratsvorlagen', border=False, align='C', new_x="LMARGIN", new_y="NEXT")
        self.set_font('free-sans', '', 10)

        self.cell(52,5, txt="**Magistratsvorlagennummer:**", markdown=True)
        self.cell(0,5, txt=f"{submission.administration_no}", new_x="LMARGIN", new_y="NEXT")
        self.cell(52,5, txt="**Datum der Magistratssitzung:**", markdown=True)
        self.cell(0,5, txt=f"{submission.administration_date.strftime('%d.%m.%Y')}" , new_x="LMARGIN",new_y="NEXT")
        self.cell(30,5, txt="**Maßnahme:**", markdown=True)
        self.multi_cell(0,5, txt=F"{submission.label}",new_x="LMARGIN", new_y="NEXT")

        self.cell(0,3, new_x="LMARGIN", new_y="NEXT")
        
        self.cell(60,5, txt="**Einschätzung der Klimarelevanz:**", markdown=True)
        impact = label_climate_impact(submission.impact)
        self.cell(0,5, txt=f"{impact}", new_x="LMARGIN",new_y="NEXT")

        if submission.impact != "no_effect":
            self.cell(60,5, txt="**Auswirkung auf Treibhausgase:**", markdown=True)
            impact_ghg = label_climate_impact_ghg(submission.impact_ghg)
            self.cell(0,5, txt=f"{impact_ghg}", new_x="LMARGIN",new_y="NEXT")

            self.cell(60,5, txt="**Anpassung an den Klimawandel:**", markdown=True)
            impact_adaption = label_climate_impact(submission.impact_adaption)
            self.cell(0,5, txt=f"{impact_adaption}", new_x="LMARGIN",new_y="NEXT")

            self.cell(60,5, txt="**Beschreibung:**", markdown=True)
            self.multi_cell(0,5, txt=f"{submission.impact_desc}",new_x="LMARGIN", new_y="NEXT")

            self.cell(60,5, txt="**Dauer der Auswirkung:**", markdown=True)
            impact_duration = label_climate_impact_duration(submission.impact_duration)
            self.cell(0,5, txt=f"{impact_duration}", new_x="LMARGIN",new_y="NEXT")

            self.cell(60,5, txt="**Alternativmaßnahme:**", markdown=True)
            self.multi_cell(0,5, txt=f"{submission.alternative_desc}",new_x="LMARGIN", new_y="NEXT")

        # Create a bytes buffer to save the self
        pdf_output = io.BytesIO()
        self.output(pdf_output)

        # Move the buffer pointer to the beginning
        pdf_output.seek(0)

        return pdf_output
    
    def export_mobility_submission(self, submission):
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True, margin=20)
        self.add_page()
        self.set_font('free-sans', 'B',16)
        self.cell(0, 10, 'Mobilitätscheck für Magistratsvorlagen', border=False, align='C', new_x="LMARGIN", new_y="NEXT")
        self.set_font('free-sans', '', 10)

        self.cell(52,5, txt="**Magistratsvorlagennummer:**", markdown=True)
        self.cell(0,5, txt=f"{submission.administration_no}", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.cell(52,5, txt="**Datum der Magistratssitzung:**", markdown=True)
        self.cell(0,5, txt=f"{submission.administration_date.strftime('%d.%m.%Y')}" , new_x="LMARGIN",new_y="NEXT")
        self.ln(2)
        self.cell(35,5, txt="**Maßnahme:**", markdown=True)
        self.multi_cell(0,5, txt=F"{submission.label}",new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.cell(35,5, txt="**Beschreibung:**", markdown=True)
        self.multi_cell(0,5, txt=f"{submission.desc}",new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.cell(35,5, txt="**Sachbearbeitung:**", markdown=True)
        editors = ""
        if submission.created_by:
             editors = f"{submission.author.first_name} {submission.author.last_name}"
        if submission.last_edited_by:
            if submission.created_by != submission.last_edited_by:
                editors += f", {submission.last_editor.first_name} {submission.last_editor.last_name}"
            
        self.cell(0,5, txt=editors, new_x="LMARGIN",new_y="NEXT")

        self.cell(0,3, new_x="LMARGIN", new_y="NEXT")

        average_impact_main_objectives = calculcate_average_impact(submission)

        box_x = self.get_x()
        box_y = self.get_y()
        
        self.cell(0, 10, '**Zielampel laut verkehrlichem Leitbild**', markdown=True, align='L', new_x="LMARGIN", new_y="NEXT")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, './assests/legende.png')  # Navigate to assets
        # Normalize the path for compatibility
        image_path = os.path.normpath(image_path)
        self.image(image_path, box_x+115, box_y + 3, 70)
        self.set_font('free-sans', '', 10)
        
        for main_objective in submission.objectives:
            display_impact = get_display_impact(average_impact_main_objectives[main_objective.main_objective_id], main_objective.target)
            self.set_fill_color(r=display_impact["color"]["r"], g=display_impact["color"]["g"], b =display_impact["color"]["b"])
            self.cell(0,8, txt=f"{main_objective.main_objective_id}. {main_objective.main_objective.label}", markdown=True, fill=True,  new_y="NExT", new_x="LMARGIN")
        box_h = self.get_y() - box_y
        self.rect(box_x, box_y, self.epw, box_h)

        # All main objective and only targeted sub objectives are displayed

        self.set_font('free-sans', '', 11)
        self.cell(0, 5, new_x="LMARGIN", new_y="NEXT")

        padding = [0,10,0,0]

        for ix, main_objective in enumerate(submission.objectives):
            
            self.set_line_width(0.25)

            self.cell(10,10, txt=f"**{main_objective.main_objective.no}**", markdown=True)

            self.multi_cell(145,10, txt=f"**{main_objective.main_objective.label}**", markdown=True,  max_line_height=5, padding=padding, new_y="TOP")

            display_impact = get_display_impact(average_impact_main_objectives[main_objective.main_objective_id], main_objective.target)

            self.set_fill_color(r=display_impact["color"]["r"], g=display_impact["color"]["g"], b =display_impact["color"]["b"])

            self.multi_cell(35,10, txt=f"**Gesamtwirkung:** \n{display_impact["label"]}", markdown=True, fill=True, max_line_height=5, new_x="LMARGIN", new_y="NEXT")

            self.set_line_width(0.1)

            for index, sub_objective in enumerate(main_objective.sub_objectives):

                if sub_objective.target:
                    if index == 0:
                        self.set_line_width(0.25)
                    else:
                        self.set_line_width(0.1)
                    
                    self.cell(0,0, border="T", new_x="LMARGIN", new_y="NEXT")

                    self.cell(10, 10, txt=f"{main_objective.main_objective.no}.{
                    sub_objective.sub_objective.no}", markdown=True, border="T")

                    self.multi_cell(145,10, txt=f"{sub_objective.sub_objective.label}", markdown=True, max_line_height=5, border="T", padding=padding, new_y="TOP")
                    display_impact = get_display_impact(sub_objective.impact, sub_objective.target)
                    self.set_fill_color(r=display_impact["color"]["r"], g=display_impact["color"]["g"], b =display_impact["color"]["b"])

                # if not sub_objective.target:
                #     self.multi_cell(35,10, txt=f"**Wirkung:**\n{display_impact["label"]}", markdown=True,border="T",max_line_height=5, fill=True, new_x="LMARGIN", new_y="NEXT")

                
                    self.multi_cell(35,10, txt=f"**Wirkung:**\n{display_impact["label"]}", markdown=True,border="T",max_line_height=5, fill=True, new_x="LEFT", new_y="NEXT")
                    self.multi_cell(35,10, txt=f"**Räumlich:**\n{label_mobility_spatial_impact(sub_objective.spatial_impact)}", markdown=True,max_line_height=5, new_x="LMARGIN", new_y="TOP")
                    self.cell(10, 5)
                    # table_x = self.get_x()
                    self.cell(25,5, txt="**Anmerkung:**", markdown=True)
                    if sub_objective.annotation:
                        self.multi_cell(120,5, txt=sub_objective.annotation, padding=padding, new_x="LMARGIN", new_y="NEXT")
                        self.cell(145, 1, new_x="LMARGIN", new_y="NEXT")
                        
                    else:
                        self.cell(0,5, txt="-", new_x="LMARGIN", new_y="NEXT")

                    self.cell(10,5)
                    # self.cell(25,5, txt="**Indikatoren:**", markdown=True)
                    # self.multi_cell(120,5, txt=', '.join(indicator.label for indicator in sub_objective.indicators), markdown=True, padding=padding, new_x="LMARGIN", new_y="NEXT")
                    # Set the label for "Indikatoren:"
                    self.cell(25, 5, txt="**Indikatoren:**", markdown=True)
                    if sub_objective.indicators:
                        
                        # Fixed indentation for bullet points
                        bullet_indent = 45  # Adjust this value to align with "Indikatoren:"

                        # Start adding indicators as a bulleted list on the same line
                        for i, indicator in enumerate(sub_objective.indicators):
                            # Set the x position for bullet points alignment
                            self.set_x(bullet_indent)
                            
                            # Set bullet point and label text
                            bullet_point = "• "
                            label_text = bullet_point + indicator.label
                            
                            # Add hyperlink if a source URL exists, otherwise just add text
                            if indicator.source_url:
                                self.set_text_color(0, 0, 255)  # Optional: set link color to blue
                                self.cell(0, 5, label_text, link=indicator.source_url, ln=1)
                                self.set_text_color(0, 0, 0)  # Reset color after the link text
                            else:
                                self.cell(0, 5, label_text, ln=1)
                    else:
                        self.cell(0, 5, txt="-", markdown=True, new_x="LMARGIN", new_y="NEXT")

            if not ix == len(submission.objectives) - 1:
                self.set_line_width(0.5)
                self.cell(0, 1, border="B", new_x="LMARGIN", new_y="NEXT")
                self.cell(0, 1, new_x="LMARGIN", new_y="NEXT")
        # Create a bytes buffer to save the self
        pdf_output = io.BytesIO()
        self.output(pdf_output)

        # Move the buffer pointer to the beginning
        pdf_output.seek(0)

        return pdf_output