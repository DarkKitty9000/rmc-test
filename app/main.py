from fastapi import FastAPI, Depends, Query, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
import sys

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# Метод получения всех возможных мест размещения номенклатуры
@app.post("/LoadNomenclaturePlacing")
async def get_nomenclature_placing(
    db: Session = Depends(get_db),
    xrmccookie: str = Header(default = None),
    # page: int = Query(ge=0, default=0),
    # size: int = Query(ge=1, le=100)
): 
    token = xrmccookie
    if token != "" and token is not None:
        nomenclatures = crud.get_nomenclature_placing_from_db_for_user(
            db=db,
            token=token,
            # page=page,
            # size=size
        )
    else:
        nomenclatures = crud.get_nomenclature_placing_from_db(
            db=db,
            # page=page,
            # size=size
        )
    
    temp_list = []
    
    if nomenclatures is not None:        
        for nomenclature in nomenclatures:
            values = { 
                "Код": nomenclature.kod, 
                "Бренд": nomenclature.brend, 
                "Наименование": nomenclature.naimenovanie, 
                "Артикул": nomenclature.articul, 
                "Город": nomenclature.gorod, 
                "Дом": nomenclature.dom, 
                "Регион": nomenclature.region, 
                "Улица": nomenclature.ulica, 
                "СтатистикаНоменклатуры": nomenclature.statisticanomenclatury, 
                "ФедеральныйОкруг": nomenclature.federalniyokrug, 
                "НаименованиеПолное": nomenclature.naimenovaniepolnoe, 
                "ДоступностьНоменклатуры": nomenclature.dostupnostnomenclatury, 
                "МестоПродажи": nomenclature.mestoprodazhy, 
                "Аббревиатура": nomenclature.abbreviatura, 
                "ТИП": nomenclature.tip, 
                "Оператор": nomenclature.operator, 
                "ТипКонтента": nomenclature.tipcontenta, 
                "Звук": nomenclature.zvuk, 
                "ЗвуковаяПодложка": nomenclature.zvukovayapodlozhka, 
                "ДикторскаяНачитка": nomenclature.dictorskayanachitka, 
                "Район": nomenclature.rayon, 
                "ЗвукПоУмолчанию": nomenclature.zvukpoumolchaniu, 
                "ДикторскаяНачиткаПоУмолчанию": nomenclature.dictorskayanachitkapoumolchaniu, 
                "ЗвуковаяПодложкаПоУмолчанию": nomenclature.zvukovayapodlozhkapoumolchaniu, 
                "ДатаПоследнейДоступностиТочки": nomenclature.dataposledneydostupnostitochki, 
                "РежимРаботыС": nomenclature.rezhimrabotys, 
                "РежимРаботыПо": nomenclature.rezhimrabotypo, 
                "Лого": nomenclature.logo, 
                "АббревиатураФедОкруг": nomenclature.abbreviaturafedokrug, 
                "ОператорАремси": nomenclature.operatoraremcy, 
                "Владелец": (nomenclature.contragents[0].link \
                             if nomenclature.contragents.count == 1 else \
                                x.link for x in nomenclature.contragents \
                ), 
                "ОсновноеКонтактноеЛицоКод": nomenclature.osnovnoekontaktnoelicokod, 
                "ЭкстерьерМассив": nomenclature.exteriermassiv, 
                "ТипыНосителей": nomenclature.tipynositeley, 
                "НаименованиеФильтрованное": nomenclature.naimenovaniefiltrovannoe 
            }
            temp_list.append(values)
        
    res = {
        'СтрокаТЧ': temp_list
    }
    return res


# Метод получения мест размещения для конкретного пользователя по токену
@app.post("/LoadNomenclaturePlacingForUser")
async def get_nomenclature_placing_for_user(
    db: Session = Depends(get_db),
    xrmccookie: str = Header(default = None),
    # page: int = Query(ge=0, default=0),
    # size: int = Query(ge=1, le=100)
):
    token = xrmccookie
    if token is None or token == "":
        raise HTTPException(status_code=401, detail="Empty token")
    nomenclatures = crud.get_nomenclature_placing_from_db_for_user(
        db=db,
        token=token,
        # page=page,
        # size=size
    )
    
    temp_list = []
    
    if nomenclatures is not None:        
        for nomenclature in nomenclatures:
            values = { 
                "Код": nomenclature.kod, 
                "Бренд": nomenclature.brend, 
                "Наименование": nomenclature.naimenovanie, 
                "Артикул": nomenclature.articul, 
                "Город": nomenclature.gorod, 
                "Дом": nomenclature.dom, 
                "Регион": nomenclature.region, 
                "Улица": nomenclature.ulica, 
                "СтатистикаНоменклатуры": nomenclature.statisticanomenclatury, 
                "ФедеральныйОкруг": nomenclature.federalniyokrug, 
                "НаименованиеПолное": nomenclature.naimenovaniepolnoe, 
                "ДоступностьНоменклатуры": nomenclature.dostupnostnomenclatury, 
                "МестоПродажи": nomenclature.mestoprodazhy, 
                "Аббревиатура": nomenclature.abbreviatura, 
                "ТИП": nomenclature.tip, 
                "Оператор": nomenclature.operator, 
                "ТипКонтента": nomenclature.tipcontenta, 
                "Звук": nomenclature.zvuk, 
                "ЗвуковаяПодложка": nomenclature.zvukovayapodlozhka, 
                "ДикторскаяНачитка": nomenclature.dictorskayanachitka, 
                "Район": nomenclature.rayon, 
                "ЗвукПоУмолчанию": nomenclature.zvukpoumolchaniu, 
                "ДикторскаяНачиткаПоУмолчанию": nomenclature.dictorskayanachitkapoumolchaniu, 
                "ЗвуковаяПодложкаПоУмолчанию": nomenclature.zvukovayapodlozhkapoumolchaniu, 
                "ДатаПоследнейДоступностиТочки": nomenclature.dataposledneydostupnostitochki, 
                "РежимРаботыС": nomenclature.rezhimrabotys, 
                "РежимРаботыПо": nomenclature.rezhimrabotypo, 
                "Лого": nomenclature.logo, 
                "АббревиатураФедОкруг": nomenclature.abbreviaturafedokrug, 
                "ОператорАремси": nomenclature.operatoraremcy, 
                "Своя": nomenclature.svoya, 
                "ОсновноеКонтактноеЛицоКод": nomenclature.osnovnoekontaktnoelicokod, 
                "ЭкстерьерМассив": nomenclature.exteriermassiv, 
                "ТипыНосителей": nomenclature.tipynositeley, 
                "НаименованиеФильтрованное": nomenclature.naimenovaniefiltrovannoe 
            }
            temp_list.append(values)
        
    res = {
        'СтрокаТЧ': temp_list
    }
    return res


@app.post('/LoadContentWeb')
async def load_content_web(
    db: Session = Depends(get_db),
    xrmccookie: str = Header(default = None),
    # page: int = Query(ge=0, default=0),
    # size: int = Query(ge=1, le=100)
):
    token = xrmccookie
    if token is None or token == "":
        contents = crud.get_content_web(db=db)
        #raise HTTPException(status_code=401, detail="Empty token")
    
    else:
        contents = crud.get_content_web_for_user(db = db, token = token) 
                                                #  page = page, size = size)

    temp_list = []
    print(contents)
    if contents is not None:        
        for element in contents:
            values = { 
                "Наименование": element.naimenovanie,
                "КонтентКод": element.contentkod,
                "ДатаСоздания": element.datasozdaniya,
                "Текущий": element.tekuschiy,
                "Прошедший": element.proshedshiy,
                "Будущий": element.buduschiy,
                "БезМП": element.bezmp,
                "КоличествоСценариев": element.kolichestvoscenariev,
                "СценарийКод": element.scenariykod,
                "Сценарий": element.scenariy,
                "Ответственный": element.otvetstvenniy,
                "РасширениеФайлаКонтента": element.rasshireniefailacontenta,
                "НаСервере": element.naservere,
                "ДатаОкончания": element.dataokonchaniya,
                "КЛ": element.kl,
                "КЛКод": element.cp_link,
                "Фоновый": element.fonoviy,
                "ГотовыйКонтент": element.gotoviycontent,
                "НевыполненныеЗадачи": element.nevypolnennyezadachi,
                "СтрокаБрендов": element.logo,
                "Контрагент": element.contragents,
                "Бренд": element.brands,
                "ОПФ": element.opf,
                "Номенклатура": element.nomenklatura,
                "Пример": element.primer,
                "ДатаСтарта": element.datastarta, 
            }
            temp_list.append(values)
        
    res = {
        'СтрокаТЧ': temp_list
    }
    return res


# @app.route('/LoadContentWebForUser')
# async def load_content_web_for_user(
#     db: Session,
#     token: str = None
# ):
#     if token is None or token == "":
#         raise HTTPException(status_code=401, detail="Empty token")
    
#     contents = crud.get_content_web(db=db)

#     temp_list = []

#     if contents is not None:        
#         for element in contents:
#             values = { 
#                 "Наименование": element.naimenovanie,
#                 "КонтентКод": element.contentkod,
#                 "ДатаСоздания": element.datasozdaniya,
#                 "Текущий": element.tekuschiy,
#                 "Прошедший": element.proshedshiy,
#                 "Будущий": element.buduschiy,
#                 "БезМП": element.bezmp,
#                 "КоличествоСценариев": element.kolichestvoscenariev,
#                 "СценарийКод": element.scenariykod,
#                 "Сценарий": element.scenariy,
#                 "Ответственный": element.otvetstvenniy,
#                 "РасширениеФайлаКонтента": element.rasshireniefailacontenta,
#                 "НаСервере": element.naservere,
#                 "ДатаОкончания": element.dataokonchaniya,
#                 "КЛ": element.kl,
#                 "КЛКод": element.klkod,
#                 "Фоновый": element.fonoviy,
#                 "ГотовыйКонтент": element.gotoviycontent,
#                 "НевыполненныеЗадачи": element.nevypolnennyezadachi,
#                 "СтрокаБрендов": element.strokabrendov,
#                 "Контрагент": element.kontragent,
#                 "Бренд": element.brand,
#                 "ОПФ": element.opf,
#                 "Номенклатура": element.nomenklatura,
#                 "Пример": element.primer,
#                 "ДатаСтарта": element.datastarta, 
#             }
#             temp_list.append(values)
        
#     res = {
#         'СтрокаТЧ': temp_list
#     }
#     return res
