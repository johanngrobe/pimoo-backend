from app.core.db import Base

from app.models.assoziation_indikator_tag import indikator_tag_assoziation
from app.models.assoziation_mobilitaetscheckEingabeZielUnter_indikator import (
    mobilitaetscheckEingabeZielUnter_indikator_assoziation,
)
from app.models.assoziation_textblock_tag import textblock_tag_assoziation
from app.models.gemeinde import Gemeinde
from app.models.klimacheckEingabe import KlimacheckEingabe
from app.models.indikator import Indikator
from app.models.mobilitaetscheck_ziel_ober import MobilitaetscheckZielOber
from app.models.mobilitaetscheck_ziel_unter import MobilitaetscheckZielUnter
from app.models.mobilitaetscheck_eingabe import MobilitaetscheckEingabe
from app.models.mobilitaetscheck_eingabe_ziel_ober import (
    MobilitaetscheckEingabeZielOber,
)
from app.models.mobilitaetscheck_eingabe_ziel_unter import (
    MobilitaetscheckEingabeZielUnter,
)
from app.models.tag import Tag
from app.models.textblock import Textblock
from app.models.user import User
