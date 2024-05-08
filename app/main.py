from fastapi import FastAPI, Depends
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
        

@app.post("/LoadNomenclaturePlacing")
async def get_nomenclature_placing(db: Session = Depends(get_db)):
    nomenclatures = crud.get_nomenclature_placing_from_db(db=db)
    
    temp = []
    
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
        temp.append(values)
    
    res = {
        'СтрокаТЧ': temp
    }
    return res


@app.get("/test")
def get_something():
    print('got_something')
