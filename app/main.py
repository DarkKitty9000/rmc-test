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
        users_nomenclature = crud.get_nomenclature_placing_from_db_for_user(
            db=db,
            token=token,
            # page=page,
            # size=size
        )

        owner_links = [object_nomenclature for object_nomenclature in users_nomenclature]

        nomenclatures = crud.get_nomenclature_placing_from_db(
            db=db,
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

            if nomenclature in owner_links:
                Owner = True
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
                "Своя": Owner,
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
    request: Request,
    db: Session = Depends(get_db),
    xrmccookie: str = Header(default = None),
    page: int = Query(ge=0, default=0),
    size: int = Query(ge=1, le=8000)
):
    token = xrmccookie
    data = await request.json()
    print(data["СтрокаПоиска"])
    if token is None or token == "":
        contents = crud.get_content_web(db=db)
        # raise HTTPException(status_code=401, detail="Empty token")
    
    else:
        contents = crud.get_content_web_for_user(db = db, token = token, search = data["СтрокаПоиска"], page = page, size = size) 
                                                

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
                "name": element.naimenovanie,
                "code": element.contentkod,
                "creationDate": element.datasozdaniya,
                "current": element.tekuschiy, # Определять на новом сервере
                "past": element.proshedshiy, # Определять на новом сервере
                "future": element.buduschiy, # Определять на новом сервере
                "withoutMP": element.bezmp,
                "scriptCount": element.kolichestvoscenariev,
                "scriptCode": element.scenariykod,
                "script": element.scenariy,
                "responsible": element.otvetstvenniy,
                "fileExtension": element.rasshireniefailacontenta,
                "onServer": element.naservere,
                "endDate": element.dataokonchaniya,
                "cl": element.kl,
                "clCode": KLCode,
                "type": element.fonoviy,
                "readyContent": element.gotoviycontent,
                "haveNotDoneTasks": element.nevypolnennyezadachi,
                "brandsRow": element.logo,
                "counterparty": contragent, # строкой
                "brand": brand,    #  строкой
                "opf": element.opf,
                "nomenclatureS": element.nomenklatura,
                "example": element.primer,
                "startDate": element.datastarta, 
            }
            temp_list.append(values)
        
    res = {
        
        "ДобавитьновыйКонтент": True,        
        "ОбщееКоличество": 100,
        'СтрокаТЧ': temp_list
    }
    return res


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0")