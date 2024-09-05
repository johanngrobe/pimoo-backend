from fpdf import FPDF
import datetime
import os
import io
from ...utils.pdf import *

class FPDF(FPDF):

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
        self.set_font('helvetica', '',10)
        self.cell(0, 8, f"{datetime.date.today().strftime('%d.%m.%Y')}", align='R')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', '', 8)
        self.cell(0, 10, f"Seite {self.page_no()}/{{nb}}", align="C")

    def export_climate_submission(self, submission):
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True, margin=20)
        self.add_page()
        self.set_font('helvetica', 'B',16)
        self.cell(0, 10, 'Klimacheck für Magistratsvorlagen', border=False, align='C', new_x="LMARGIN", new_y="NEXT")
        self.set_font('helvetica', '', 10)

        self.cell(52,5, txt="**Magistratsvorlagennummer:**", markdown=True)
        self.cell(0,5, txt=f"{submission.administration_no}", new_x="LMARGIN", new_y="NEXT")
        self.cell(52,5, txt="**Datum der Magistratssitzung:**", markdown=True)
        self.cell(0,5, txt=f"{submission.administration_date.strftime('%d.%m.%Y')}" , new_x="LMARGIN",new_y="NEXT")
        self.cell(30,5, txt="**Maßnahme:**", markdown=True)
        self.multi_cell(0,5, txt=F"{submission.label}",new_x="LMARGIN", new_y="NEXT")
        self.cell(30,5, txt="**Beschreibung:**", markdown=True)
        self.cell(0,5, txt=f"{submission.author}", new_x="LMARGIN",new_y="NEXT")

        self.cell(0,3, new_x="LMARGIN", new_y="NEXT")
        
        self.cell(30,5, txt="**Einschätzung der Klimarelevanz**", markdown=True)
        self.cell(0,5, txt=f"{submission.impact}", new_x="LMARGIN",new_y="NEXT")

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
        self.set_font('helvetica', 'B',16)
        self.cell(0, 10, 'Mobilitätscheck für Magistratsvorlagen', border=False, align='C', new_x="LMARGIN", new_y="NEXT")
        self.set_font('helvetica', '', 10)

        self.cell(52,5, txt="**Magistratsvorlagennummer:**", markdown=True)
        self.cell(0,5, txt=f"{submission.administration_no}", new_x="LMARGIN", new_y="NEXT")
        self.cell(52,5, txt="**Datum der Magistratssitzung:**", markdown=True)
        self.cell(0,5, txt=f"{submission.administration_date.strftime('%d.%m.%Y')}" , new_x="LMARGIN",new_y="NEXT")
        self.cell(30,5, txt="**Maßnahme:**", markdown=True)
        self.multi_cell(0,5, txt=F"{submission.label}",new_x="LMARGIN", new_y="NEXT")
        self.cell(30,5, txt="**Beschreibung:**", markdown=True)
        self.multi_cell(0,5, txt=f"{submission.desc}",new_x="LMARGIN", new_y="NEXT")
        self.cell(30,5, txt="**Bearbeitet durch:**", markdown=True)
        self.cell(0,5, txt=f"{submission.author}", new_x="LMARGIN",new_y="NEXT")


        self.cell(0,3, new_x="LMARGIN", new_y="NEXT")

        # Create a bytes buffer to save the self
        pdf_output = io.BytesIO()
        self.output(pdf_output)

        # Move the buffer pointer to the beginning
        pdf_output.seek(0)

        return pdf_output

        # TODO summazize_impact überarbeiten, da noch mit Pandas gearbeitet wird
        # df_ampel = summarize_wirkung()

        # box_x = self.get_x()
        # box_y = self.get_y()
        
        # self.cell(0, 10, '**Zielampel laut verkehrlichem Leitbild**', markdown=True, align='L', new_x="LMARGIN", new_y="NEXT")
        # self.image('pictures/legende.png', box_x+115, box_y + 3, 70)
        # self.set_font('helvetica', '', 10)
        
        # for ind in df_ampel.index:
        #     leitziel_name = df_ampel['name'][ind]
        #     leitziel_tangiert = df_ampel['tangiert'][ind]
        #     leitziel_wirkung = df_ampel['wirkung'][ind]
        #     color = get_color(leitziel_wirkung, leitziel_tangiert)
        #     self.set_fill_color(r= color[0], g=color[1], b =color[2])
        #     self.cell(0,8, txt=f"{ind}. {leitziel_name}", markdown=True, fill=True,  new_y="NExT", new_x="LMARGIN")
        # box_h = self.get_y() - box_y
        # self.rect(box_x, box_y, self.epw, box_h)

        # submission.results

        # df = st.session_state['df_ziele']

        # # Alle Ziele und Unterziele werden angezeigt
        # print_df = df
        # print_unterziele = print_df[print_df['kat'] == 'Unterziel']
        # print_leitziele = df_ampel

        # # Nur tangierte Ziele und Unterziele werden angezeigt

        # self.set_font('helvetica', '', 11)
        # self.cell(0, 5, new_x="LMARGIN", new_y="NEXT")

        # for ind_leitziel in print_leitziele.index:

        #     leitziel_name = print_leitziele['name'][ind_leitziel]
        #     leitziel_tangiert = print_leitziele['tangiert'][ind_leitziel]
        #     leitziel_wirkung = print_leitziele['mean'][ind_leitziel]

        #     self.cell(10,10, txt=f"**{int(ind_leitziel)}**", markdown=True, border="TL")
        #     self.multi_cell(145,10, txt=f"**{leitziel_name}**", markdown=True, border="TR", max_line_height=5, new_y="TOP")
        #     color = get_color(leitziel_wirkung, leitziel_tangiert)
        #     self.set_fill_color(r= color[0], g=color[1], b =color[2])
        #     self.multi_cell(35,10, txt=f"**Gesamtwirkung:** \n{convert_wirkung(leitziel_wirkung)}", markdown=True, fill=True, border="TBR", max_line_height=5, new_x="LMARGIN", new_y="NEXT")

        #     for ind in print_unterziele.index:
        #         if ind_leitziel == print_unterziele['leitziel'][ind]:

        #             unterziel_name = print_unterziele['name'][ind]
        #             unterziel_tangiert = print_unterziele['tangiert'][ind]
        #             unterziel_wirkung = print_unterziele['wirkung'][ind]
        #             unterziel_wirkung_text = convert_wirkung(unterziel_wirkung, unterziel_tangiert)
        #             unterziel_raeumlich = print_unterziele['wirkung_raeumlich'][ind]
        #             unterziel_desc = print_unterziele['erlaeuterung'][ind]
        #             unterziel_indikatoren = print_unterziele['indikatoren'][ind]

        #             if unterziel_tangiert:
        #                 self.cell(10, 10, txt=f"{ind}", markdown=True, border="T")
        #                 self.multi_cell(145,10, txt=f"{unterziel_name}", markdown=True, max_line_height=5, border="T", new_y="TOP")
        #                 color = get_color(unterziel_wirkung, unterziel_tangiert)
        #                 self.set_fill_color(r= color[0], g=color[1], b =color[2])
        #                 self.multi_cell(35,10, txt=f"**Wirkung:**\n{unterziel_wirkung_text}", markdown=True,border="LT",max_line_height=5, fill=True, new_x="LEFT", new_y="NEXT")
        #                 self.multi_cell(35,15, txt=f"\n**Räumlich:**\n{unterziel_raeumlich}", markdown=True, border="L",max_line_height=5, new_x="LMARGIN", new_y="TOP")
        #                 self.cell(10, 5)
        #                 self.multi_cell(145,5,txt=f"**Erläuterung:** {unterziel_desc} \n\n**Indikatoren:** {', '.join(unterziel_indikatoren)}", markdown=True,border="R", new_x="LMARGIN", new_y="NEXT")
        #             else:
        #                 self.cell(10, 10, txt=f"{ind}", markdown=True, border="T")
        #                 self.multi_cell(145,10, txt=f"{unterziel_name}", markdown=True, max_line_height=5, border="T", new_y="TOP")
        #                 color = get_color(unterziel_wirkung, unterziel_tangiert)
        #                 self.set_fill_color(r= color[0], g=color[1], b =color[2])
        #                 self.multi_cell(35,10, txt=f"**Wirkung:**\n{unterziel_wirkung_text}", markdown=True,border="LT",max_line_height=5, fill=True, new_x="LMARGIN", new_y="NEXT")

            # self.cell(0, 8, new_x="LMARGIN", new_y="NEXT")

        # # Create a bytes buffer to save the self
        # pdf_output = io.BytesIO()
        # self.output(pdf_output)

        # # Move the buffer pointer to the beginning
        # pdf_output.seek(0)

        # return pdf_output