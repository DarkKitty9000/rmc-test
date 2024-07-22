from fastapi import FastAPI, Depends, Query, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from typing import Any, Dict, List, Union


import crud, models, schemas
from database import SessionLocal, engine
import sys
from dotenv import load_dotenv
import os

load_dotenv() # Загружаем переменные среды из .env файла.


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

SECRET_KEY = os.getenv("SECRET_KEY")

app.add_middleware(
    SessionMiddleware,
    secret_key = SECRET_KEY,
    max_age = None
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Обработка OPTIONS запросов
@app.options("/{path:path}")
async def options_handler(path: str):
    return {"Allow": "GET, POST, OPTIONS"}
        

# Метод получения всех возможных мест размещения номенклатуры
@app.post("/LoadNomenclaturePlacing")
async def get_nomenclature_placing(
    db: Session = Depends(get_db),
    xrmccookie: str = Header(default = None)
): 
    token = xrmccookie
    if token != "" and token is not None:
        users_nomenclature = crud.get_nomenclature_placing_from_db_for_user(
            db=db,
            token=token
        )

        owner_links = [object_nomenclature for object_nomenclature in users_nomenclature]

        nomenclatures = crud.get_nomenclature_placing_from_db(
            db=db
        )
    else:
        nomenclatures = crud.get_nomenclature_placing_from_db(
            db=db
        )

        owner_links = []
    
    temp_list = []

    if nomenclatures is not None:        
        for nomenclature in nomenclatures:

            if len(owner_links) != 0:

                if nomenclature in owner_links:
                    Owner = True
                else:
                    Owner = False

            else:
                Owner = False    

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
                "Своя": Owner, #Переделать
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

@app.post('/LoadContentWebTest')
async def load_content_web_test(
    request: Request,
    db: Session = Depends(get_db),
    xrmccookie: str = Header(default = None),
    page: int = Query(ge=0, default=0),
    size: int = Query(ge=1, le=8000)
):
    token = xrmccookie
    data = await request.json()
    print(data)
 
    if token is None or token == "":
        contents, count = crud.get_content_web_test_non_auth(db=db)
        # raise HTTPException(status_code=401, detail="Empty token")
    
    else:
        contents, count = crud.get_content_web_test(db = db, token = token, filterData = data, page = page, size = size) 
    temp_list = [] 
    if contents is not None:        
        for element in contents:

            values = { 
                "Наименование": element.naimenovanie,
                "КонтентКод": element.contentkod,
                "ДатаСоздания": element.datasozdaniya,
                "Текущий": element.tekuschiy, # Определять на новом сервере
                "Прошедший": element.proshedshiy, # Определять на новом сервере
                "Будущий": element.buduschiy, # Определять на новом сервере
                "БезМП": element.bezmp,
                "КоличествоСценариев": element.kolichestvoscenariev,
                "СценарийКод": element.scenariykod,
                "Сценарий": element.scenariy,
                "Ответственный": element.otvetstvenniy,
                "РасширениеФайлаКонтента": element.rasshireniefailacontenta,
                "НаСервере": element.naservere,
                "ДатаОкончания": element.dataokonchaniya,
                "КЛ": element.kl,
                "КЛКод": element.cp_link if not element.cp_link is None else "",
                "Фоновый": element.fonoviy,
                "ГотовыйКонтент": element.gotoviycontent,
                "НевыполненныеЗадачи": element.nevypolnennyezadachi,
                "СтрокаБрендов": element.logo,
                "Контрагент": element.kontragent,
                "Бренд": element.brand if not element.brand is None else "",
                "ОПФ": element.opf,
                "Номенклатура": element.nomenklatura,
                "Пример": element.primer,
                "ДатаСтарта": element.datastarta, 
            }
            temp_list.append(values)
        
    res = {
               
        "ОбщееКоличество": count,
        'СтрокаТЧ': temp_list
    }
    return res     

@app.post('/LoadContentWeb')
async def load_content_web(
    request: Request,
    db: Session = Depends(get_db),
    xrmccookie: str = Header(default = None),
    page: int = Query(ge=0, default=0),
    size: int = Query(ge=1, le=8000)
):
    token = xrmccookie
    data = await request.json()
    print(data)
 
    if token is None or token == "":
        contents, count = crud.get_content_web(db=db)
        # raise HTTPException(status_code=401, detail="Empty token")
    
    else:
        contents, count = crud.get_content_web_for_user(db = db, token = token, filterData = data, page = page, size = size) 
                                                

    temp_list = []
    if contents is not None:        
        for element in contents:

            contragent = ""
            brand = ""
            KLCode = ""

            if len(element.contragents) != 0:
                contragent = element.contragents[0].full_name

            if len(element.brands) != 0:
                brand = element.brands[0].full_name

            if element.cp_link != None:
                KLCode = element.cp_link

            values = { 
                "Наименование": element.naimenovanie,
                "КонтентКод": element.contentkod,
                "ДатаСоздания": element.datasozdaniya,
                "Текущий": element.tekuschiy, # Определять на новом сервере
                "Прошедший": element.proshedshiy, # Определять на новом сервере
                "Будущий": element.buduschiy, # Определять на новом сервере
                "БезМП": element.bezmp,
                "КоличествоСценариев": element.kolichestvoscenariev,
                "СценарийКод": element.scenariykod,
                "Сценарий": element.scenariy,
                "Ответственный": element.otvetstvenniy,
                "РасширениеФайлаКонтента": element.rasshireniefailacontenta,
                "НаСервере": element.naservere,
                "ДатаОкончания": element.dataokonchaniya,
                "КЛ": element.kl,
                "КЛКод": KLCode,
                "Фоновый": element.fonoviy,
                "ГотовыйКонтент": element.gotoviycontent,
                "НевыполненныеЗадачи": element.nevypolnennyezadachi,
                "СтрокаБрендов": element.logo,
                "Контрагент": contragent, # строкой
                "Бренд": brand,    #  строкой
                "ОПФ": element.opf,
                "Номенклатура": element.nomenklatura,
                "Пример": element.primer,
                "ДатаСтарта": element.datastarta, 
            }
            temp_list.append(values)
        
    res = {
               
        "ОбщееКоличество": count,
        'СтрокаТЧ': temp_list
    }
    return res


@app.post("/LoadNomenclature")
async def get_nomenclature_cv(
    db: Session = Depends(get_db),
    xrmccookie: str = Header(default = None)
): 
    token = xrmccookie
    if token != "" and token is not None:
        nomenclatures = crud.get_nomenclature_cv_from_db_for_user(
            db=db,
            token=token
        )
        primer = crud.get_nomenclature_cv_primer(
            db=db
        )

        common_elements = [element for element in nomenclatures if element in primer]

        if len(common_elements) == 0:
            nomenclatures.extend(primer)

    else:
        nomenclatures = []
        primer = crud.get_nomenclature_cv_primer(
            db=db
        )
        nomenclatures.extend(primer)
    
    temp_list = []

    owner_links = []

    if nomenclatures is not None:        
        for nomenclature in nomenclatures:

            if len(owner_links) != 0:

                if nomenclature in owner_links:
                    Owner = True
                else:
                    Owner = False

            else:
                Owner = False   

            values = { 
                "Код": nomenclature.kod, 
                "Бренд": nomenclature.brands_str, 
                "Наименование": nomenclature.name, 
                "Артикул": nomenclature.article, 
                "Город": nomenclature.gorod, 
                "Дом": nomenclature.dom, 
                "Регион": nomenclature.region, 
                "Улица": nomenclature.ylica, 
                "СтатистикаНоменклатуры": nomenclature.statistica, 
                "ФедеральныйОкруг": nomenclature.federalnyi_okrug, 
                "НаименованиеПолное": nomenclature.name_full, 
                "ДоступностьНоменклатуры": nomenclature.dostupnost_nomenclature, 
                "МестоПродажи": nomenclature.mesto_prodaji, 
                "Аббревиатура": nomenclature.abbreviatura, 
                "ТИП": nomenclature.tip, 
                "Оператор": nomenclature.operator, 
                "ТипКонтента": nomenclature.tip_contenta, 
                "Звук": nomenclature.zvuk, 
                "ЗвуковаяПодложка": nomenclature.zvukovaya_podlozka, 
                "ДикторскаяНачитка": nomenclature.dictorskaya_nachitka, 
                "Район": nomenclature.raion,   
                "ДатаПоследнейДоступностиТочки": nomenclature.data_poslednei_dostupnosti, 
                "Лого": nomenclature.logo, 
                "АббревиатураФедОкруг": nomenclature.abbreviatura_fed_okrug, 
                "Своя": Owner, #Переделать
                "ОсновноеКонтактноеЛицоКод": nomenclature.cp_kod, 
                "ЭкстерьерМассив": nomenclature.exterier_massiv, 
                "ТипыНосителей": nomenclature.tipy_nositelei, 
                "НаименованиеФильтрованное": nomenclature.name_filter,
                "Пример": nomenclature.primer 
            }
            temp_list.append(values)
        
    res = {
        'СтрокаТЧ': temp_list
    }
    return res

@app.post('/GetContentFilters')
async def load_content_web(
    request: Request,
    db: Session = Depends(get_db),
    xrmccookie: str = Header(default = None)
):
    token = xrmccookie
    data = await request.json()
 
    dataset = crud.get_content_filters(db = db, token = token, data = data)
        
                                                
    res = {
       "filters": dataset 
    }
    return res


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="192.168.0.5", port=8000) #Основа: 192.168.0.5, тест - 127.0.0.1. Видишь второй вариант в проде - стучи программисту.

