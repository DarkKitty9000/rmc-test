from sqlalchemy import Boolean, Column, Integer, String, ARRAY, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Token(Base):
    __tablename__ = "token"
    
    user_link = Column(String, ForeignKey("users.link"))
    token = Column(String, primary_key=True)
    
    user = relationship("User", back_populates="token")


class User(Base):
    __tablename__ = "users"
    
    link = Column(String, unique=True, primary_key=True)
    email = Column(String)
    name_full = Column(String)
    
    token = relationship("Token", back_populates="user")
    nomenclature_placing = relationship(
        "NomenclaturePlacing",
        back_populates="owner"
    )


class NomenclaturePlacing(Base):
    __tablename__ = "nomenclature_placing"

    id = Column(Integer, primary_key=True, autoincrement=True)
    abbreviatura = Column(String)
    abbreviaturafedokrug = Column(String)
    articul = Column(String)
    brend  = Column(String)
    gorod  = Column(String)
    dataposledneydostupnostitochki  = Column(String)
    dictorskayanachitka  = Column(String)
    dictorskayanachitkapoumolchaniu  = Column(Boolean)
    dom  = Column(String)
    dostupnostnomenclatury  = Column(Boolean)
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
    tipynositeley  = Column(ARRAY(String))
    ulica  = Column(String)
    federalniyokrug = Column(String)
    exteriermassiv = Column(ARRAY(String))
    owner_link = Column(String, ForeignKey("users.link"))
    
    owner = relationship("User", back_populates="nomenclature_placing")
