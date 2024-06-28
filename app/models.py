from sqlalchemy import Boolean, Column, Integer, String, ARRAY, ForeignKey, \
     CHAR, DateTime, Table, UniqueConstraint, Date
from sqlalchemy.orm import relationship

from database import Base

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


# nomenclature_contragent = Table(
#     'nomenclature_contragent',
#     Base.metadata,
#     Column(
#         'nomenclature_link',
#         ForeignKey('nomenclature_placing.link'),
#         primary_key=True
#     ),
#     Column(
#         'contragent_link',
#         ForeignKey('contragent.link'),
#         primary_key=True
#     )
# )


content_brand = Table(
    'content_brand',
    Base.metadata,
    Column(
        'content_link',
        ForeignKey('content_web.link'),
        primary_key=True
    ),
    Column(
        'brand_link',
        ForeignKey('brand.link'),
        primary_key=True
    )
)


content_contragent = Table(
    'content_contragent',
    Base.metadata,
    Column(
        'content_link',
        ForeignKey('content_web.link'),
        primary_key=True
    ),
    Column(
        'contragent_link',
        ForeignKey('contragent.link'),
        primary_key=True
    )
)


content_nomenclature = Table(
    'content_nomenclature',
    Base.metadata,
    Column(
        'content_link',
        ForeignKey('content_web.link'),
        primary_key=True
    ),
    Column(
        'nomenclature_link',
        ForeignKey('nomenclature_placing.link'),
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
    
    contragents = relationship(
        "Contragent",
        secondary = 'nomenclature_contragent',
        back_populates ="nomenclatures"
    )
    contents = relationship(
        "ContentWeb",
        secondary = 'content_nomenclature',
        back_populates="nomenclatures"
    )

class NomenclatureCV(Base):
    __tablename__ = "nomenclature_cv"

    link = Column(String, primary_key=True)
    abbreviatura = Column(String)
    abbreviatura_fed_okrug = Column(String)
    article = Column(String)
    brands_str  = Column(String)
    gorod  = Column(String)
    data_poslednei_dostupnosti  = Column(String)
    dictorskaya_nachitka  = Column(String)
    dom  = Column(String)
    dostupnost_nomenclature  = Column(Boolean)
    zvuk = Column(String)
    zvukovaya_podlozka  = Column(String)
    logo  = Column(String)
    mesto_prodaji  = Column(String)
    name  = Column(String)
    name_full  = Column(String)
    name_filter  = Column(String)
    operator  = Column(String)
    raion  = Column(String)
    region  = Column(String)
    svoya  = Column(Boolean)
    statistica = Column(Boolean)
    tip  = Column(String)
    tip_contenta  = Column(String)
    tipy_nositelei  = Column(ARRAY(String))
    ylica  = Column(String)
    federalnyi_okrug = Column(String)
    exterier_massiv = Column(ARRAY(String))
    cp_link = Column(String, ForeignKey("contact_person.link"))
    primer = Column(Boolean)
    
    contact_persons = relationship(
        "ContactPerson",
        back_populates="nomenclature_cv"
    )



class ContentWeb(Base):
    __tablename__ = "content_web"

    link = Column(String, primary_key=True, unique=True)
    bezmp = Column(Boolean)
    buduschiy = Column(Boolean)
    gotoviycontent = Column(Boolean)
    dataokonchaniya = Column(DateTime(False))
    datasozdaniya = Column(DateTime(False))
    datastarta = Column(DateTime(False))
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
    logo = Column(String)
    scenariy = Column(String)
    scenariykod = Column(String)
    tekuschiy = Column(Boolean)
    fonoviy = Column(Boolean)

    brands = relationship(
        "Brand",
        secondary = content_brand,
        back_populates = "contents"
    )
    contact_persons = relationship(
        "ContactPerson",
        back_populates="contents"
    )
    contragents = relationship(
        "Contragent",
        secondary = content_contragent,
        back_populates = "contents"
    )
    nomenclatures = relationship(
        "NomenclaturePlacing",
        secondary = 'content_nomenclature',
        back_populates = "contents"
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
        secondary = 'nomenclature_contragent',
        back_populates = "contragents"
    )
    brands = relationship(
        "Brand",
        secondary = contragent_brand,
        back_populates = "contragents"
    )
    contact_persons = relationship(
        "ContactPerson",
        secondary= contragent_cp,
        back_populates="contragents"
    )
    contents = relationship(
        "ContentWeb",
        secondary = content_contragent,
        back_populates = "contragents"
    )


class Brand(Base):
    __tablename__ = "brand"

    link = Column(String, nullable=False, primary_key=True)
    full_name = Column(String)

    contragents = relationship(
        "Contragent",
        secondary = contragent_brand,
        back_populates = "brands"
    )
    contents = relationship(
        "ContentWeb",
        secondary = content_brand,
        back_populates = "brands"
    )


# Контактные лица.
class ContactPerson(Base):
    __tablename__ = "contact_person"

    link = Column(String, primary_key=True)
    full_name = Column(String)
    site_role = Column(String)

    contragents = relationship(
        "Contragent",
        secondary = contragent_cp,
        back_populates = "contact_persons"
    )
    cp_info = relationship(
        "CPInfo",
        back_populates="contact_persons"
    )
    contents = relationship(
        "ContentWeb",
        back_populates="contact_persons"
    )
    nomenclature_cv = relationship(
        "NomenclatureCV",
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

# Промежуточная таблица номенклатура - контрагент
class nomenclature_contragent (Base):
    __tablename__ = "nomenclature_contragent"

    nomenclature_link = Column(String, ForeignKey('nomenclature_placing.link'), primary_key=True)
    contragent_link = Column(String, ForeignKey('contragent.link'), primary_key=True)

# Промежуточная таблица контрагент - бренд
# class contragent_brand (Base):
#     __tablename__ ='contragent_brand'
    
#     contragent_link = Column(String, ForeignKey('contragent.link'), primary_key=True)
#     brand_link = Column(String, ForeignKey('brand.link'), primary_key=True)

# # Промежуточная таблица контент - бренд
# class content_brand (Base):
#     __tablename__ = 'content_brand'

#     content_link = Column(String, ForeignKey('content_web.link'), primary_key=True)
#     brand_link = Column(String, ForeignKey('brand.link'), primary_key=True)

# # Промежуточная таблица контент - контрагент
# class content_contragent (Base):
#     __tablename__ = 'content_contragent'
    
#     content_link = Column(String, ForeignKey('content_web.link'), primary_key=True)
#     contragent_link = Column(String, ForeignKey('contragent.link'), primary_key=True)

# class contragent_cp(Base):
#     __tablename__ = 'contragent_cp'

#     contragent_link = Column(String, ForeignKey('contragent.link'), primary_key=True)
#     cp_link = Column(String, ForeignKey('contact_person.link'), primary_key=True)

