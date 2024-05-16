from sqlalchemy import Boolean, Column, Integer, String, ARRAY, ForeignKey, CHAR, Date, Table
from sqlalchemy.orm import relationship

from .database import Base


contragent_user = Table(
    'contragent_user',
    Base.metadata,
    Column('contragent_link', ForeignKey('contragent.link'), primary_key=True),
    Column('user_link', ForeignKey('users.link'), primary_key=True)
)


contragent_brand = Table(
    'contragent_brand',
    Base.metadata,
    Column('contragent_link', ForeignKey('contragent.link'), primary_key=True),
    Column('brand_link', ForeignKey('brand.link'), primary_key=True)
)


nomenclature_contragent = Table(
    'nomenclature_contragent',
    Base.metadata,
    Column(
        'nomenclature_link',
        ForeignKey('nomenclature_placing.link'),
        primary_key=True
    ),
    Column(
        'contragent_link',
        ForeignKey('contragent.link'),
        primary_key=True
    )
)


class Token(Base):
    __tablename__ = "token"
    
    user_link = Column(String, ForeignKey("users.link"), primary_key=True)
    token = Column(String, primary_key=True, nullable=False)
    
    user = relationship("User", back_populates="token")


class AccountInfo(Base):
    __tablename__ = "account_info"

    link = Column(
        String,
        ForeignKey("users.link"),
        primary_key=True,
        unique=True
    )
    email = Column(String, primary_key=True, unique=True)
    password = Column(String)

    link_rel = relationship(
        "User",
        back_populates='account_info'
    )


class User(Base):
    __tablename__ = "users"
    
    link = Column(String, unique=True, primary_key=True)
    name_full = Column(String)
    is_employee = Column(Boolean)
    
    token = relationship("Token", back_populates="user")
    account_info = relationship(
        "AccountInfo",
        back_populates="link_rel"
    )
    contragents = relationship(
        "Contragent",
        secondary=contragent_user,
        back_populates="users"
    )


class NomenclaturePlacing(Base):
    __tablename__ = "nomenclature_placing"

    link = Column(String, primary_key=True)
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
    owner_link = Column(String, ForeignKey("contragent.link"))
    
    contragents = relationship("Contragent", back_populates="nomenclatures")


class ContentWeb(Base):
    __tablename__ = "content_web"

    id = Column(Integer, primary_key=True, unique=True, autoincrement="auto")
    bezmp = Column(Boolean)
    brand = Column(String)
    buduschiy = Column(Boolean)
    gotoviycontent = Column(Boolean)
    dataokonchaniya = Column(String)
    datasozdaniya = Column(String)
    datastarta = Column(String)
    kl = Column(String)
    klkod = Column(String)
    kolichestvoscenariev = Column(Integer)
    contentkod = Column(String)
    kontragent = Column(String)
    naservere = Column(Boolean)
    naimenovanie = Column(String)
    nevypolnennyezadachi = Column(Boolean)
    nomenklatura = Column(String)
    opf = Column(String)
    otvetstvenniy = Column(String)
    primer = Column(Boolean)
    proshedshiy = Column(Boolean)
    rasshireniefailacontenta = Column(String)
    strokabrendov = Column(String)
    scenariy = Column(String)
    scenariykod = Column(String)
    tekuschiy = Column(Boolean)
    fonoviy = Column(Boolean)


class Contragent(Base):
    __tablename__ = "contragent"

    link = Column(String, nullable=False, primary_key=True)
    full_name = Column(String)
    opf = Column(String)
    register_date = Column(Date)
    inn = Column(String)
    keyword = Column(String)
    add_name = Column(String)
    description = Column(String)

    nomenclatures = relationship(
        "NomenclaturePlacing",
        secondary=nomenclature_contragent,
        back_populates="contragents"
    )
    users = relationship(
        "User",
        secondary=contragent_user,
        back_populates="contragents"
    )
    brands = relationship(
        "Brand",
        secondary=contragent_brand,
        back_populates="contragents"
    )
    contact_persons = relationship(
        "ContactPerson",
        back_populates="contragents"
    )


class Brand(Base):
    __tablename__ = "brand"

    link = Column(String, nullable=False, primary_key=True)
    full_name = Column(String)

    contragents = relationship(
        "Contragent",
        secondary=contragent_brand,
        back_populates="brands"
    )


class ContactPerson(Base):
    __tablename__ = "contact_person"

    link = Column(String, primary_key=True)
    contragent_link = Column(String, ForeignKey('contragent.link'))
    site_role = Column(String)

    contragents = relationship("Contragent", back_populates="contact_persons")
    cp_info = relationship("CPInfo", back_populates="contact_persons")


class CITypes(Base):
    __tablename__ = "ci_types"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    type = Column(String, nullable=False)

    cp_info = relationship("CPInfo", back_populates="ci_types")


class CPInfo(Base):
    __tablename__ = "cp_contact_info"

    cp_link = Column(String, ForeignKey("contact_person.link"), primary_key=True)
    ci_type = Column(Integer, ForeignKey("ci_types.id"), primary_key=True)
    value = Column(String, nullable=False)

    contact_persons = relationship("ContactPerson", back_populates="cp_info")
    ci_types = relationship("CITypes", back_populates="cp_info")
