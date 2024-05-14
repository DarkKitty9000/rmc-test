from pydantic import BaseModel, Field


class NomenclaturePlacing(BaseModel):
    abbreviatura: str = Field(serialization_alias='Аббревиатура')
    abbreviaturafedokrug: str = Field(
        serialization_alias='АббревиатураФедОкруг'
    )
    articul: str = Field(serialization_alias='Артикул')
    brend: str = Field(serialization_alias='Бренд')
    gorod: str = Field(serialization_alias='Город')
    dataposledneydostupnostitochki: str = Field(
        serialization_alias='ДатаПоследнейДоступностиТочки'
    )
    dictorskayanachitka: str = Field(serialization_alias='ДикторскаяНачитка')
    dictorskayanachitkapoumolchaniu: bool = Field(
        serialization_alias='ДикторскаяНачиткаПоУмолчанию'
    )
    dom: str = Field(serialization_alias='Дом')
    dostupnostnomenclatury: str = Field(
        serialization_alias='ДоступностьНоменклатуры'
    )
    zvuk: str = Field(serialization_alias='Звук')
    zvukpoumolchaniu: bool = Field(serialization_alias='ЗвукПоУмолчанию')
    zvukovayapodlozhka: str = Field(serialization_alias='ЗвуковаяПодложка')
    zvukovayapodlozhkapoumolchaniu: bool = Field(
        serialization_alias='ЗвуковаяПодложкаПоУмолчанию'
    )
    kod: str = Field(serialization_alias='Код')
    logo: str = Field(serialization_alias='Лого')
    mestoprodazhy: str = Field(serialization_alias='МестоПродажи')
    naimenovanie: str = Field(serialization_alias='Наименование')
    naimenovaniepolnoe: str = Field(serialization_alias='НаименованиеПолное')
    naimenovaniefiltrovannoe: str = Field(
        serialization_alias='НаименованиеФильтрованное'
    )
    operator: str = Field(serialization_alias='Оператор')
    operatoraremcy: bool = Field(serialization_alias='ОператорАремси')
    osnovnoekontaktnoelicokod: str = Field(
        serialization_alias='ОсновноеКонтактноеЛицоКод'
    )
    rayon: str = Field(serialization_alias='Район')
    region: str = Field(serialization_alias='Регион')
    rezhimrabotypo: str = Field(serialization_alias='РежимРаботыПо')
    rezhimrabotys: str = Field(serialization_alias='РежимРаботыС')
    svoya: bool = Field(serialization_alias='Своя')
    sobstvennik: str
    statisticanomenclatury: bool = Field(
        serialization_alias='СтатистикаНоменклатуры'
    )
    tip: str = Field(serialization_alias='ТИП')
    tipcontenta: str = Field(serialization_alias='ТипКонтента')
    tipnaselennogopunkta: str
    tipregiona: str
    tipulicy: str
    tipynositeley: list[str] = Field(serialization_alias='ТипыНосителей')
    ulica: str = Field(serialization_alias='Улица')
    federalniyokrug: str = Field(serialization_alias='ФедеральныйОкруг')
    exteriermassiv: list[str] = Field(serialization_alias='ЭкстерьерМассив')

    class Config:
        from_attributes = True
