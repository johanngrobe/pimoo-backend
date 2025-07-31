from app.core.db import Base

from app.models.assoziation_indikator_tag import indikator_tag_assoziation
from app.models.assoziation_magistratsvorlage_gemeindeGebiet import (
    magistratsvorlage_gemeindeGebiet_assoziation,
)
from app.models.assoziation_mobilitaetscheckEingabe_user import (
    mobilitaetscheckEingabe_user_assoziation,
)
from app.models.assoziation_mobilitaetscheckEingabeZielUnter_indikator import (
    mobilitaetscheckEingabeZielUnter_indikator_assoziation,
)
from app.models.assoziation_textblock_tag import textblock_tag_assoziation
from app.models.gemeinde import Gemeinde
from app.models.gemeinde_gebiet import GemeindeGebiet
from app.models.klimacheck_klimarelevanz import KlimacheckKlimarelevanz
from app.models.klimacheck_auswirkung_dauer import KlimacheckAuswirkungDauer
from app.models.klimacheck_eingabe import KlimacheckEingabe
from app.models.indikator import Indikator
from app.models.magistratsvorlage import Magistratsvorlage
from app.models.mobilitaetscheck_auswirkung_raeumlich import (
    MobilitaetscheckAuswirkungRaeumlich,
)
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
from app.models.user_rolle import UserRolle
