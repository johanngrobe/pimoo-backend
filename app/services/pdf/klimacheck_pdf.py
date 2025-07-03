from io import BytesIO

from app.models.klimacheckEingabe import KlimacheckEingabe
from app.services.pdf.base_pdf import BasePDF
from app.utils.label_util import (
    label_climate_impact,
    label_climate_impact_duration,
    label_climate_impact_ghg,
)


class KlimacheckPDF(BasePDF):
    def footer(self):
        self.set_y(-20)
        self.set_font("free-sans", "", 8)
        self.cell(0, 10, f"Seite {self.page_no()}/{{nb}}", align="C")

    def export(self, eingabe: KlimacheckEingabe):
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True, margin=20)
        self.add_page()
        # Different styles of the same font family.
        self.set_font("free-sans", "B", 16)
        self.cell(
            0,
            10,
            "Klimacheck für Magistratsvorlagen",
            border=False,
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.set_font("free-sans", "", 10)

        self.cell(52, 5, txt="**Magistratsvorlagennummer:**", markdown=True)
        self.cell(
            0,
            5,
            txt=f"{eingabe.verwaltungsvorgang_nr}",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.cell(52, 5, txt="**Datum der Magistratssitzung:**", markdown=True)
        self.cell(
            0,
            5,
            txt=f"{eingabe.verwaltungsvorgang_datum.strftime('%d.%m.%Y')}",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.cell(30, 5, txt="**Maßnahme:**", markdown=True)
        self.multi_cell(0, 5, txt=f"{eingabe.name}", new_x="LMARGIN", new_y="NEXT")

        self.cell(0, 3, new_x="LMARGIN", new_y="NEXT")

        self.cell(60, 5, txt="**Einschätzung der Klimarelevanz:**", markdown=True)
        klimarelevanz = label_climate_impact(eingabe.klimarelevanz)
        self.cell(0, 5, txt=f"{klimarelevanz}", new_x="LMARGIN", new_y="NEXT")

        if eingabe.klimarelevanz != "no_effect":
            self.cell(60, 5, txt="**Auswirkung auf Treibhausgase:**", markdown=True)
            auswirkung_thg = label_climate_impact_ghg(eingabe.auswirkung_thg)
            self.cell(0, 5, txt=f"{auswirkung_thg}", new_x="LMARGIN", new_y="NEXT")

            self.cell(60, 5, txt="**Anpassung an den Klimawandel:**", markdown=True)
            auswirkung_klimaanpassung = label_climate_impact(
                eingabe.auswirkung_klimaanpassung
            )
            self.cell(
                0, 5, txt=f"{auswirkung_klimaanpassung}", new_x="LMARGIN", new_y="NEXT"
            )

            self.cell(60, 5, txt="**Beschreibung:**", markdown=True)
            self.multi_cell(
                0,
                5,
                txt=f"{eingabe.auswirkung_beschreibung}",
                new_x="LMARGIN",
                new_y="NEXT",
            )

            self.cell(60, 5, txt="**Dauer der Auswirkung:**", markdown=True)
            auswirkung_dauer = label_climate_impact_duration(eingabe.auswirkung_dauer)
            self.cell(0, 5, txt=f"{auswirkung_dauer}", new_x="LMARGIN", new_y="NEXT")

            self.cell(60, 5, txt="**Alternativmaßnahme:**", markdown=True)
            self.multi_cell(
                0,
                5,
                txt=f"{eingabe.alternativen}",
                new_x="LMARGIN",
                new_y="NEXT",
            )

        # Create a bytes buffer to save the self
        pdf_output = BytesIO()
        self.output(pdf_output)

        # Move the buffer pointer to the beginning
        pdf_output.seek(0)

        return pdf_output
