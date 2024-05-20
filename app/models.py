from sqlalchemy import Boolean, Column, Integer, String, ARRAY, ForeignKey, CHAR, Date, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base

# Описание промежуточных таблиц для таблиц со связью многие-ко-многим.
# -----------------------------------------------------------------------------
contragent_cp = Table(
    'contragent_cp',
    Base.metadata,
    Column('contragent_link', ForeignKey('contragent.link'), primary_key=True),
    Column('cp_link', ForeignKey('contact_person.link'), primary_key=True)
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


# Описание основных таблиц базы данных
# -----------------------------------------------------------------------------

# Таблица с токенами авторизации для пользователей.
class Token(Base):
    __tablename__ = "token"
    
    user_link = Column(String, ForeignKey("users.link"), primary_key=True)
    token = Column(String, primary_key=True, nullable=False)
    
    user = relationship("User", back_populates="token")


# Данные авторизации для входа на сайт.
class AccountInfo(Base):
    __tablename__ = "account_info"
    __table_args__ = (
        UniqueConstraint('link', 'email', name='account_info_unique'),
    )

    link = Column(
        String,
        ForeignKey("users.link"),
        primary_key=True
    )
    email = Column(String, primary_key=True)
    password = Column(String)

    link_rel = relationship(
        "User",
        back_populates='account_info'
    )


# Пользователи приложения. Как сотрудники, так и контактные лица.
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
    
    contragents = relationship("Contragent", back_populates="nomenclatures")
    contents = relationship(
        "ContentWeb",
        back_populates="nomenclatures"
    )


class ContentWeb(Base):
    __tablename__ = "content_web"

    link = Column(String, primary_key=True, unique=True)
    bezmp = Column(Boolean)
    brand_link = Column(String, ForeignKey("brand.link"))
    buduschiy = Column(Boolean)
    gotoviycontent = Column(Boolean)
    dataokonchaniya = Column(String)
    datasozdaniya = Column(String)
    datastarta = Column(String)
    kl = Column(String)
    cp_link = Column(String, ForeignKey("contact_person.link"))
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
    ca_link = Column(String, ForeignKey("contragent.link"))
    nomenclature_link = Column(String, ForeignKey("nomenclature_placing.link"))

    brands = relationship(
        "Brand",
        back_populates="contents"
    )
    contact_persons = relationship(
        "ContactPerson",
        back_populates="contents"
    )
    contragents = relationship(
        "Contragent",
        back_populates="contents"
    )
    nomenclatures = relationship(
        "NomenclaturePlacing",
        back_populates="contents"
    )


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
    brands = relationship(
        "Brand",
        secondary=contragent_brand,
        back_populates="contragents"
    )
    contact_persons = relationship(
        "ContactPerson",
        secondary=contragent_cp,
        back_populates="contragents"
    )
    contents = relationship(
        "ContentWeb",
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
    contents = relationship(
        "ContentWeb",
        back_populates="brands"
    )


# Контактные лица.
class ContactPerson(Base):
    __tablename__ = "contact_person"

    link = Column(String, primary_key=True)
    full_name = Column(String)
    site_role = Column(String)

    contragents = relationship(
        "Contragent",
        secondary=contragent_cp,
        back_populates="contact_persons"
    )
    cp_info = relationship(
        "CPInfo",
        back_populates="contact_persons"
    )
    contents = relationship(
        "ContentWeb",
        back_populates="contact_persons"
    )


# Виды контактной информации.
class CITypes(Base):
    __tablename__ = "ci_types"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    type = Column(String, nullable=False)

    cp_info = relationship("CPInfo", back_populates="ci_types")


# Контактная информация контактных лиц.
class CPInfo(Base):
    __tablename__ = "cp_contact_info"

    cp_link = Column(String, ForeignKey("contact_person.link"), primary_key=True)
    ci_type = Column(Integer, ForeignKey("ci_types.id"), primary_key=True)
    value = Column(String, nullable=False, primary_key=True)

    contact_persons = relationship("ContactPerson", back_populates="cp_info")
    ci_types = relationship("CITypes", back_populates="cp_info")
