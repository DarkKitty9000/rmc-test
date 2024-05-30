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
    
    print(owner_links)

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
    size: int = Query(ge=1, le=1000)
):
    token = xrmccookie
    data = await request.json()
    print(data["search"])
    if token is None or token == "":
        contents = crud.get_content_web(db=db)
        raise HTTPException(status_code=401, detail="Empty token")
    
    else:
        contents = crud.get_content_web_for_user(db = db, token = token, search = data["search"], page = page, size = size) 
                                                

    temp_list = []
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app)