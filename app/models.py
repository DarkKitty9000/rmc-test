from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class NomenclaturePlacing(Base):
    __tablename__ = "nomenclature_placing"

    id = Column(Integer, primary_key=True)
    abbreviatura = Column(String)
    abbreviaturafedokrug = Column(String)
    articul = Column(String)
    brend  = Column(String)
    gorod  = Column(String)
    dataposledneydostupnostitochki  = Column(String)
    dictorskayanachitka  = Column(String)
    dictorskayanachitkapoumolchaniu  = Column(Boolean)
    dom  = Column(String)
    dostupnostnomenclatury  = Column(String)
    zvuk = Column(String)
    zvukpoumolchaniu  = Column(Boolean)
    zvukovayapodlozhka  = Column(String)
    zvukovayapodlozhkapoumolchaniu  = Column(Boolean)
    kod  = Column(String)
    logo  = Column(String)
    mestoprodazhy  = Column(String)
    naimenovanie  = Column(String)
    naimenovaniepolnoe  = Column(String)
    naimenovaniefiltrovannoe  = Column(String)
    operator  = Column(String)
    operatoraremcy  = Column(Boolean)
    osnovnoekontaktnoelicokod  = Column(String)
    rayon  = Column(String)
    region  = Column(String)
    rezhimrabotypo  = Column(String)
    rezhimrabotys  = Column(String)
    svoya  = Column(Boolean)
    sobstvennik   = Column(String)
    statisticanomenclatury  = Column(Boolean)
    tip  = Column(String)
    tipcontenta  = Column(String)
    tipnaselennogopunkta  = Column(String)
    tipregiona  = Column(String)
    tipulicy  = Column(String)
    tipynositeley  = Column(String)
    ulica  = Column(String)
    federalniyokrug = Column(String)
    exteriermassiv = Column(String)
    