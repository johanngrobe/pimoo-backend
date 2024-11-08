import datetime
from fpdf import FPDF
from os import path


class BasePDF(FPDF):

    def __init__(self, orientation="P", unit="mm", format="A4"):
        # Pass the parameters to FPDF's __init__ method
        super().__init__(orientation, unit, format)
        font_path = path.dirname(path.abspath(__file__))
        self.add_font(
            "free-sans",
            style="",
            fname=path.join(font_path, "./assests/FreeSans/FreeSans.ttf"),
        )
        self.add_font(
            "free-sans",
            style="b",
            fname=path.join(font_path, "./assests/FreeSans/FreeSansBold.ttf"),
        )
        self.add_font(
            "free-sans",
            style="i",
            fname=path.join(font_path, "./assests/FreeSans/FreeSansOblique.ttf"),
        )
        self.add_font(
            "free-sans",
            style="bi",
            fname=path.join(font_path, "./assests/FreeSans/FreeSansBoldOblique.ttf"),
        )

    def header(self):
        # Get the absolute path to the image
        script_dir = path.dirname(path.abspath(__file__))
        image_path = path.join(
            script_dir, "./assests/pimoo_3logos.png"
        )  # Navigate to assets

        # Normalize the path for compatibility
        image_path = path.normpath(image_path)
        try:
            self.image(image_path, 10, 8, 100)
        except Exception as e:
            print(e)
        self.set_font("free-sans", "", 10)
        self.cell(0, 8, f"{datetime.date.today().strftime('%d.%m.%Y')}", align="R")
        self.ln(15)
