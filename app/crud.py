from sqlalchemy import select, orm, or_, func, text, any_, and_, delete, insert
from sqlalchemy.orm import Session, joinedload, contains_eager, aliased
from fastapi import HTTPException
from fastapi_filter import FilterDepends

import models, schemas


# Метод для получения мест размещения номенклатуры
def get_nomenclature_placing_from_db(
        db: Session,

    ):
    """
    Метод для получения мест размещения номенклатуры
    db - Сессия базы данных,
    """
    response = db.query(models.NomenclaturePlacing).all()
    return response


def get_nomenclature_placing_from_db_for_user(
        db: Session,
        token: str,

    ):
    """
    Метод для получения мест размещения номенклатуры по пользователю
    db - Сессия базы данных,
    token - Токен авторизации пользователя
    """

    user = get_user_by_token(db = db, token = token) # Получаем пользователя

    if user.is_employee:
        response = db.query(models.NomenclaturePlacing).all()
        return response 

    else:
    # Получаем всех контрагентов по пользователю.
        contragents = get_contragent_by_user(db = db, user = user)
        try:
            response = db.query(models.NomenclaturePlacing).join(models.nomenclature_contragent).filter(
                    models.nomenclature_contragent.contragent_link.in_(contragents)    
                ).all()
            return response
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
    

""" def get_content_web(db: Session) -> models.ContentWeb:
    
    Метод получения примеров контента
    db - Сессия базы данных,
    token - Токен авторизации пользователя
    Вызывается если пользователь не авторизован
    
    response = db.query(models.ContentWeb).filter(models.ContentWeb.primer == True)
    count = db.query(func.count(models.ContentWeb.link)).scalar()
    return response, count


def get_content_web_for_user(db: Session, token: str, filterData: str, page: int, size: int) -> models.ContentWeb: 
                           
    Метод получения контента по пользователю.
    db - Сессия базы данных,
    token - Токен авторизации пользователя
    filterData - Данные фильтрации в запросе
    page - отдаваемая страница массива данных
    size - размерность страницы массива данных
 
    user = get_user_by_token(db = db, token = token) # Получаем пользователя

    subresponse = (select(models.ContentWeb).join(models.ContentWeb.brands, isouter = True)\
         .join(models.ContentWeb.contragents, isouter = True).join(models.ContentWeb.contact_persons, isouter=True))

    if user.is_employee:

        if filterData["search"] == "":

            or_filters = []

            if filterData["tekuschiy"] == True:
                or_filters.append(models.ContentWeb.tekuschiy == True)

            if filterData["buduschiy"] == True:
                or_filters.append(models.ContentWeb.buduschiy == True)

            if filterData["proshedshiy"] == True:
                or_filters.append(models.ContentWeb.proshedshiy == True)

            if filterData["bezmp"] == True:
                or_filters.append(models.ContentWeb.bezmp == True)

            if or_filters:
                subresponse = subresponse.filter(or_(*or_filters))

        else:
 
            # Разбиваем поиск на отдельные проверки для каждого поля
            brand_filter = models.Brand.full_name.ilike(f'%{filterData["search"]}%')
            contentkod_filter = models.ContentWeb.contentkod.ilike(f'%{filterData["search"]}%')
            contragent_filter = models.Contragent.full_name.ilike(f'%{filterData["search"]}%')
            contactperson_filter = models.ContactPerson.full_name.ilike(f'%{filterData["search"]}%')
            naimenovanie_filter = models.ContentWeb.naimenovanie.ilike(f'%{filterData["search"]}%')

            # Объединяем все фильтры с оператором ИЛИ (|)
            combined_filter = brand_filter | contentkod_filter | contragent_filter | contactperson_filter | naimenovanie_filter

            subresponse = (subresponse.filter(combined_filter))

        response = (select(models.ContentWeb).select_from(subresponse.alias())
                     .join(models.ContentWeb.brands)
                     .join(models.ContentWeb.contragents)
                     .join(models.ContentWeb.contact_persons)
                     .options(contains_eager(models.ContentWeb.brands), 
                              contains_eager(models.ContentWeb.contragents), 
                              contains_eager(models.ContentWeb.contact_persons))).order_by(models.ContentWeb.datasozdaniya.desc())
        
        count = db.execute(select(func.count()).select_from(subresponse.alias())).scalar()

        print(response)
        unic_list = db.execute(response.limit(size).offset(page * size)).scalars().unique().all()
        
        return unic_list, count 
    
    else:
    # Получаем всех контрагентов по пользователю.
        contragents = get_contragent_by_user(db = db, user = user)
        try:
            subresponse = subresponse.filter(
                    models.Contragent.link.in_(contragents)    
                )
                
            if filterData["search"] != '':

                # Разбиваем поиск на отдельные проверки для каждого поля
                brand_filter = models.Brand.full_name.ilike(f'%{filterData["search"]}%')
                contentkod_filter = models.ContentWeb.contentkod.ilike(f'%{filterData["search"]}%')
                contragent_filter = models.Contragent.full_name.ilike(f'%{filterData["search"]}%')
                contactperson_filter = models.ContactPerson.full_name.ilike(f'%{filterData["search"]}%')
                naimenovanie_filter = models.ContentWeb.naimenovanie.ilike(f'%{filterData["search"]}%')

                # Объединяем все фильтры с оператором ИЛИ (|)
                combined_filter = brand_filter | contentkod_filter | contragent_filter | contactperson_filter | naimenovanie_filter

                subresponse = (subresponse.filter(combined_filter))

            else:

                or_filters = []

                if filterData["tekuschiy"] == True:
                    or_filters.append(models.ContentWeb.tekuschiy == True)

                if filterData["buduschiy"] == True:
                    or_filters.append(models.ContentWeb.buduschiy == True)

                if filterData["proshedshiy"] == True:
                    or_filters.append(models.ContentWeb.proshedshiy == True)

                if filterData["bezmp"] == True:
                    or_filters.append(models.ContentWeb.bezmp == True)

                if or_filters:
                    subresponse = subresponse.filter(or_(*or_filters))

            subresponse = subresponse.order_by(models.ContentWeb.primer.desc(), models.ContentWeb.datasozdaniya.desc())

            response = (select(models.ContentWeb).select_from((subresponse.alias()))\
                    .join(models.ContentWeb.brands, isouter = True).join(models.ContentWeb.contragents, isouter = True).join(models.ContentWeb.contact_persons, isouter = True)
                    .options(contains_eager(models.ContentWeb.brands), contains_eager(models.ContentWeb.contragents), contains_eager(models.ContentWeb.contact_persons)))
        
            count = db.execute(select(func.count()).select_from(subresponse.alias())).scalar()

            response = db.execute(response.limit(size).offset(page * size)).scalars().unique().all()

            return response, count
        except Exception as e:
            print(f"Error occurred: in get_content {e}")
            return None """
    


def get_user_by_token(db: Session, token: str):
    """
    Метод получения пользователя по токену авторизации.
    db - Сессия базы данных,
    token - токен авторизации.
    """
    try:
        token = db.query(models.Token).filter(
            models.Token.token == token
        ).first()
        user = db.query(models.User).filter(
            models.User.link == token.user_link
        ).first()
        return user
    except:
        raise HTTPException(status_code = 404, detail = "Пользователь не найден.")


def get_contragent_by_user(db: Session, user: models.User):
    """
    Метод получения контрагента по пользователю
    db - Сессия базы данных,
    user - Объект пользователя.
    """
    contragents = db.query(models.Contragent).filter(
        models.Contragent.contact_persons.any(link = user.link)
    ).all()
    return [contragent.full_name for contragent in contragents]

def get_cp_by_user(db: Session, user: models.User):
    """
    Метод получения контрагента по пользователю
    db - Сессия базы данных,
    user - Объект пользователя.
    """
    cp_link = db.query(models.ContactPerson).filter(
        models.ContactPerson.link == user.link
    ).first()
    return cp_link


def get_nomenclature_cv_from_db(
        db: Session,

    ):
    """
    Метод для получения номенклатуры КВ
    db - Сессия базы данных,
    """
    response = db.query(models.NomenclatureCV).all()
    return response


def get_nomenclature_cv_from_db_for_user(
        db: Session,
        token: str,
    ):
    """
    Метод для получения номенклатуры КВ по пользователю
    db - Сессия базы данных,
    token - Токен авторизации пользователя
    """

    user = get_user_by_token(db = db, token = token) # Получаем пользователя

    if user.is_employee:
        response = db.query(models.NomenclatureCV).all()
        return response 

    else:
    # Получаем всю номенклатуру по пользователю.
        cp_link = get_cp_by_user(db = db, user = user)
        try:
            response = db.query(models.NomenclatureCV).filter(
                    models.NomenclatureCV.contact_persons.any(link = cp_link.link)    
                ).all()
            return response
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
        

def get_nomenclature_cv_primer(db: Session) -> models.ContentWeb:
    """
    Метод получения примеров номенклатуры КВ
    db - Сессия базы данных,
    Вызывается если пользователь не авторизован
    """
    response = db.query(models.NomenclatureCV).filter(models.NomenclatureCV.primer == True).all()
    return response

def get_content_web_non_auth(db: Session) -> models.ContentWeb:
    """
    Метод получения примеров контента
    db - Сессия базы данных,
    token - Токен авторизации пользователя
    Вызывается если пользователь не авторизован
    """
    response = db.query(models.ContentWeb).filter(models.ContentWeb.primer == True)
    count = db.query(func.count(models.ContentWeb.link)).filter(models.ContentWeb.primer == True).scalar()
    return response, count


def get_content_web(db: Session, token: str, page: int, size: int, return_dict: dict, data: dict) -> models.ContentWeb: 
                           
    """
    Метод получения контента по пользователю.
    db - Сессия базы данных,
    token - Токен авторизации пользователя
    filterData - Данные фильтрации в запросе
    page - отдаваемая страница массива данных
    size - размерность страницы массива данных
    """
    user = get_user_by_token(db = db, token = token) # Получаем пользователя

    response = db.query(models.ContentWeb)
    
    filterData = get_filters_by_saved_data(db, token)
    if user.is_employee:

        combined_filter = [True]
        if data["search"] != "":

            # Разбиваем поиск на отдельные проверки для каждого поля
            brand_filter = func.array_to_string(models.ContentWeb.brand_list, ';').ilike(f'%{data["search"]}%')
            contragent_filter =  func.array_to_string(models.ContentWeb.contragent_list, ';').ilike(f'%{data["search"]}%')

            contentkod_filter = models.ContentWeb.contentkod.ilike(f'%{data["search"]}%')
            contactperson_filter = models.ContentWeb.kl.ilike(f'%{data["search"]}%')
            naimenovanie_filter = models.ContentWeb.naimenovanie.ilike(f'%{data["search"]}%')

            # Объединяем все фильтры с оператором ИЛИ (|)
            combined_filter = brand_filter | contentkod_filter | contragent_filter | contactperson_filter | naimenovanie_filter

        or_filters = []
        filters_list_brand = []
        filters_list_contragent = []
        filters_list_otvetstvenniy = []
        filters_list_kl = []

        if filterData["showCurrent"] == True:
            or_filters.append(models.ContentWeb.tekuschiy == True)

        if filterData["showFuture"] == True:
            or_filters.append(models.ContentWeb.buduschiy == True)

        if filterData["showPast"] == True:
            or_filters.append(models.ContentWeb.proshedshiy == True)

        if filterData["showWithoutMP"] == True:
            or_filters.append(models.ContentWeb.bezmp == True)

        if filterData["showAdFilter"] == True:
            or_filters.append(models.ContentWeb.fonoviy == False)

        if filterData["showUndoneTaskFilter"] == True:
            or_filters.append(models.ContentWeb.nevypolnennyezadachi == True)

        if filterData["showOnServerFilter"] == True:
            or_filters.append(models.ContentWeb.naservere == True)

        if filterData["showAudioFilter"] == True:
            or_filters.append('Аудио' == any_(models.ContentWeb.filetypes))

        if filterData["showVideoFilter"] == True:
            or_filters.append('Видео' == any_(models.ContentWeb.filetypes))

        if filterData["showImageFilter"] == True:
            or_filters.append('Картинка' == any_(models.ContentWeb.filetypes))

        if filterData["showTextFilter"] == True:
            or_filters.append('Текст' == any_(models.ContentWeb.filetypes))

        if filterData["showHaveScriptFilter"] == True:
            or_filters.append(models.ContentWeb.scenariy != '')

        if filterData["showUnknownFileTypeFilter"] == True:
            or_filters.append('Неопределено' == any_(models.ContentWeb.filetypes))

        if filterData["showNoFileFilter"] == True:
            or_filters.append(models.ContentWeb.rasshireniefailacontenta == '')

        if filterData["isExample"] == True:
            or_filters.append(models.ContentWeb.primer == True)

        for item in filterData["brand_list"]:
            filters_list_brand.append(item == any_(models.ContentWeb.brand_list))

        for item in filterData["contragent_list"]:
            filters_list_contragent.append(item == any_(models.ContentWeb.contragent_list))

        for item in filterData["kl"]:
            filters_list_kl.append(item == models.ContentWeb.kl)

        for item in filterData["otvetstvenniy"]:
            filters_list_otvetstvenniy.append(item == models.ContentWeb.otvetstvenniy)

        if len(or_filters) == 0:
            or_filters.append(True)

        if len(filters_list_brand) == 0:
            filters_list_brand.append(True)

        if len(filters_list_contragent) == 0:
            filters_list_contragent.append(True)

        if len(filters_list_kl) == 0:
            filters_list_kl.append(True)

        if len(filters_list_otvetstvenniy) == 0:
            filters_list_otvetstvenniy.append(True)

        response = response.filter(or_(*combined_filter) & and_(*or_filters) & or_(*filters_list_brand) & or_(*filters_list_contragent) & or_(*filters_list_kl) & or_(*filters_list_otvetstvenniy) | (models.ContentWeb.primer == True))

        filters_list = or_(*combined_filter) & or_(*filters_list_kl) & or_(*filters_list_brand) & or_(*filters_list_contragent) & or_(*filters_list_otvetstvenniy) & and_(*or_filters)
        
        if filterData["current_filter"] == "brand_list":
            
            filters_list_excluded_current = or_(*combined_filter) & or_(*filters_list_kl) & or_(*filters_list_contragent) & or_(*filters_list_otvetstvenniy) & and_(*or_filters)

        elif filterData["current_filter"] == "contragent_list":
            
            filters_list_excluded_current = or_(*combined_filter) & or_(*filters_list_kl) & or_(*filters_list_brand) & or_(*filters_list_otvetstvenniy) & and_(*or_filters)

        elif filterData["current_filter"] == "otvetstvenniy":
            
            filters_list_excluded_current = or_(*combined_filter) & or_(*filters_list_kl) & or_(*filters_list_brand) & or_(*filters_list_contragent) & and_(*or_filters)

        elif filterData["current_filter"] == "kl":
            
            filters_list_excluded_current = or_(*combined_filter) & or_(*filters_list_brand) & or_(*filters_list_contragent) & or_(*filters_list_otvetstvenniy) & and_(*or_filters)

        if filterData["current_filter"] == "otvetstvenniy":
            response_of_responsibles = select(models.ContentWeb.otvetstvenniy).filter(filters_list_excluded_current).group_by(models.ContentWeb.otvetstvenniy)
        else:
            response_of_responsibles = select(models.ContentWeb.otvetstvenniy).filter(filters_list).group_by(models.ContentWeb.otvetstvenniy)

        result = db.execute(response_of_responsibles)
        for item in result:
            return_dict["otvetstvenniy"].append(item.otvetstvenniy) if not item.otvetstvenniy in filterData['otvetstvenniy'] else True

        if filterData["current_filter"] == "brand_list":
            response_of_brand = select(models.ContentWeb.brand_list).filter(filters_list_excluded_current).group_by(models.ContentWeb.brand_list)
        else:
            response_of_brand = select(models.ContentWeb.brand_list).filter(filters_list).group_by(models.ContentWeb.brand_list)

        result = db.execute(response_of_brand)
        for item in result:
            if item.brand_list is not None:
                for brand in item.brand_list:
                    return_dict["brand_list"].append(brand) if not return_dict["brand_list"].__contains__(brand) and not brand in filterData['brand_list'] else True

        if filterData["current_filter"] == "contragent_list":
            response_of_contragent = select(models.ContentWeb.contragent_list).filter(filters_list_excluded_current).group_by(models.ContentWeb.contragent_list)
        else:
            response_of_contragent = select(models.ContentWeb.contragent_list).filter(filters_list).group_by(models.ContentWeb.contragent_list)

        result = db.execute(response_of_contragent)
        for item in result:
            if item.contragent_list is not None:
                for contragent in item.contragent_list:
                    return_dict["contragent_list"].append(contragent) if not return_dict["contragent_list"].__contains__(contragent) and not contragent in filterData['contragent_list'] else True

        if filterData["current_filter"] == "kl":
            response_of_kl = select(models.ContentWeb.kl).filter(filters_list_excluded_current).group_by(models.ContentWeb.kl)
        else:
            response_of_kl = select(models.ContentWeb.kl).filter(filters_list).group_by(models.ContentWeb.kl)

        result = db.execute(response_of_kl)
        for item in result:
            return_dict["kl"].append(item.kl) if not item.kl in filterData['kl'] else True

        subq = select(models.ContentWeb.tekuschiy).filter(filters_list).group_by(models.ContentWeb.tekuschiy).subquery()
        subq_only_false = select(models.ContentWeb.tekuschiy).filter(filters_list & (models.ContentWeb.tekuschiy == False)).group_by(models.ContentWeb.tekuschiy).subquery()
        only_false = False
        response_of_current = select(func.count(subq.c.tekuschiy))
        result = db.execute(response_of_current)
        for item in result:
            if item.count == 1:
                response_of_current_only_false = select(func.count(subq_only_false.c.tekuschiy))
                result_only_false = db.execute(response_of_current_only_false)
                for item_only_false in result_only_false:
                    only_false = item_only_false.count == 1
                    break
            return_dict["showCurrent"] = not (item.count == 1 and only_false) 
            break
        
        subq = select(models.ContentWeb.buduschiy).filter(filters_list).group_by(models.ContentWeb.buduschiy).subquery()
        subq_only_false = select(models.ContentWeb.buduschiy).filter(filters_list & (models.ContentWeb.buduschiy == False)).group_by(models.ContentWeb.buduschiy).subquery()
        only_false = False
        response_of_current = select(func.count(subq.c.buduschiy))
        result = db.execute(response_of_current)
        for item in result:
            if item.count == 1:
                response_of_current_only_false = select(func.count(subq_only_false.c.buduschiy))
                result_only_false = db.execute(response_of_current_only_false)
                for item_only_false in result_only_false:
                    only_false = item_only_false.count == 1
                    break
            return_dict["showFuture"] = not (item.count == 1 and only_false) 
            break

        subq = select(models.ContentWeb.proshedshiy).filter(filters_list).group_by(models.ContentWeb.proshedshiy).subquery()
        subq_only_false = select(models.ContentWeb.proshedshiy).filter(filters_list & (models.ContentWeb.proshedshiy == False)).group_by(models.ContentWeb.proshedshiy).subquery()
        only_false = False
        response_of_current = select(func.count(subq.c.proshedshiy))
        result = db.execute(response_of_current)
        for item in result:
            if item.count == 1:
                response_of_current_only_false = select(func.count(subq_only_false.c.proshedshiy))
                result_only_false = db.execute(response_of_current_only_false)
                for item_only_false in result_only_false:
                    only_false = item_only_false.count == 1
                    break
            return_dict["showPast"] = not (item.count == 1 and only_false) 
            break

        subq = select(models.ContentWeb.bezmp).filter(filters_list).group_by(models.ContentWeb.bezmp).subquery()
        subq_only_false = select(models.ContentWeb.bezmp).filter(filters_list & (models.ContentWeb.bezmp == False)).group_by(models.ContentWeb.bezmp).subquery()
        only_false = False
        response_of_current = select(func.count(subq.c.bezmp))
        result = db.execute(response_of_current)
        for item in result:
            if item.count == 1:
                response_of_current_only_false = select(func.count(subq_only_false.c.bezmp))
                result_only_false = db.execute(response_of_current_only_false)
                for item_only_false in result_only_false:
                    only_false = item_only_false.count == 1
                    break
            return_dict["showWithoutMP"] = not (item.count == 1 and only_false) 
            break

        subq = select(models.ContentWeb.nevypolnennyezadachi).filter(filters_list).group_by(models.ContentWeb.nevypolnennyezadachi).subquery()
        subq_only_false = select(models.ContentWeb.nevypolnennyezadachi).filter(filters_list & (models.ContentWeb.nevypolnennyezadachi == False)).group_by(models.ContentWeb.nevypolnennyezadachi).subquery()
        only_false = False
        response_of_current = select(func.count(subq.c.nevypolnennyezadachi))
        result = db.execute(response_of_current)
        for item in result:
            if item.count == 1:
                response_of_current_only_false = select(func.count(subq_only_false.c.nevypolnennyezadachi))
                result_only_false = db.execute(response_of_current_only_false)
                for item_only_false in result_only_false:
                    only_false = item_only_false.count == 1
                    break
            return_dict["showUndoneTaskFilter"] = not (item.count == 1 and only_false) 
            break

        subq = select(models.ContentWeb.fonoviy).filter(filters_list).group_by(models.ContentWeb.fonoviy).subquery()
        subq_only_false = select(models.ContentWeb.fonoviy).filter(filters_list & (models.ContentWeb.fonoviy == True)).group_by(models.ContentWeb.fonoviy).subquery()
        only_false = False
        response_of_current = select(func.count(subq.c.fonoviy))
        result = db.execute(response_of_current)
        for item in result:
            if item.count == 1:
                response_of_current_only_false = select(func.count(subq_only_false.c.fonoviy))
                result_only_false = db.execute(response_of_current_only_false)
                for item_only_false in result_only_false:
                    only_false = item_only_false.count == 1
                    break
            return_dict["showAdFilter"] = not (item.count == 1 and only_false) 
            break

        subq = select(models.ContentWeb.scenariy).filter(filters_list).group_by(models.ContentWeb.scenariy).subquery()
        subq_only_false = select(models.ContentWeb.scenariy).filter(filters_list & (models.ContentWeb.scenariy == "")).group_by(models.ContentWeb.scenariy).subquery()
        only_false = False
        response_of_current = select(func.count(subq.c.scenariy))
        result = db.execute(response_of_current)
        for item in result:
            if item.count == 1:
                response_of_current_only_false = select(func.count(subq_only_false.c.scenariy))
                result_only_false = db.execute(response_of_current_only_false)
                for item_only_false in result_only_false:
                    only_false = item_only_false.count == 1
                    break
            return_dict["showHaveScriptFilter"] = not (item.count == 1 and only_false) 
            break

        subq = select(models.ContentWeb.naservere).filter(filters_list).group_by(models.ContentWeb.naservere).subquery()
        subq_only_false = select(models.ContentWeb.naservere).filter(filters_list & (models.ContentWeb.naservere == False)).group_by(models.ContentWeb.naservere).subquery()
        only_false = False
        response_of_current = select(func.count(subq.c.naservere))
        result = db.execute(response_of_current)
        for item in result:
            if item.count == 1:
                response_of_current_only_false = select(func.count(subq_only_false.c.naservere))
                result_only_false = db.execute(response_of_current_only_false)
                for item_only_false in result_only_false:
                    only_false = item_only_false.count == 1
                    break
            return_dict["showOnServerFilter"] = not (item.count == 1 and only_false) 
            break

        type_count = {"Аудио": 0,
                    "Видео": 0,
                    "Текст": 0,
                    "Картинка": 0,
                    "Неопределено": 0,
                    "Без файла": 0}
        
        response_of_current = select(models.ContentWeb.filetypes).filter(filters_list).group_by(models.ContentWeb.filetypes)
        result = db.execute(response_of_current)

        for item in result:
            if item.filetypes is None:
                continue

            if len(item.filetypes) == 0:
                type_count["Без файла"] += 1
            
            for content_type in item.filetypes:
                if content_type in type_count.keys():
                    type_count[content_type] += 1

        return_dict["showAudioFilter"] = (type_count["Аудио"] > 0)
        return_dict["showImageFilter"] = (type_count["Картинка"] > 0)
        return_dict["showVideoFilter"] = (type_count["Видео"] > 0)
        return_dict["showTextFilter"] = (type_count["Текст"] > 0)
        return_dict["showUnknownFileTypeFilter"] = (type_count["Неопределено"] > 0)
        return_dict["showNoFileFilter"] = (type_count["Без файла"] > 0)

        return_dict["isExample"] = True
        count = response.count()

        max_page = count//size + 1

        response = response.order_by(models.ContentWeb.primer.desc(), models.ContentWeb.datasozdaniya.desc())

        unic_list = response.limit(size).offset(page * size).all()

        return max_page, unic_list, count, return_dict 
    
    else:
    # Получаем всех контрагентов по пользователю.
        contragents = get_contragent_by_user(db = db, user = user)
        try:
            additional_filter = []

            for contragent_found in contragents:
                additional_filter.append(contragent_found == any_(models.ContentWeb.contragent_list)) 

            combined_filter = [True]
            if data["search"] != "":

                # Разбиваем поиск на отдельные проверки для каждого поля
                brand_filter = func.array_to_string(models.ContentWeb.brand_list, ';').ilike(f'%{data["search"]}%')
                contragent_filter =  func.array_to_string(models.ContentWeb.contragent_list, ';').ilike(f'%{data["search"]}%')

                contentkod_filter = models.ContentWeb.contentkod.ilike(f'%{data["search"]}%')
                contactperson_filter = models.ContentWeb.kl.ilike(f'%{data["search"]}%')
                naimenovanie_filter = models.ContentWeb.naimenovanie.ilike(f'%{data["search"]}%')

                # Объединяем все фильтры с оператором ИЛИ (|)
                combined_filter = brand_filter | contentkod_filter | contragent_filter | contactperson_filter | naimenovanie_filter

            or_filters = []
            filters_list_brand = []
            filters_list_contragent = []
            filters_list_otvetstvenniy = []
            filters_list_kl = []

            if filterData["showCurrent"] == True:
                or_filters.append(models.ContentWeb.tekuschiy == True)

            if filterData["showFuture"] == True:
                or_filters.append(models.ContentWeb.buduschiy == True)

            if filterData["showPast"] == True:
                or_filters.append(models.ContentWeb.proshedshiy == True)

            if filterData["showWithoutMP"] == True:
                or_filters.append(models.ContentWeb.bezmp == True)

            if filterData["showAdFilter"] == True:
                or_filters.append(models.ContentWeb.fonoviy == False)

            if filterData["showUndoneTaskFilter"] == True:
                or_filters.append(models.ContentWeb.nevypolnennyezadachi == True)

            if filterData["showOnServerFilter"] == True:
                or_filters.append(models.ContentWeb.naservere == True)

            if filterData["showAudioFilter"] == True:
                or_filters.append('Аудио' == any_(models.ContentWeb.filetypes))

            if filterData["showVideoFilter"] == True:
                or_filters.append('Видео' == any_(models.ContentWeb.filetypes))

            if filterData["showImageFilter"] == True:
                or_filters.append('Картинка' == any_(models.ContentWeb.filetypes))

            if filterData["showTextFilter"] == True:
                or_filters.append('Текст' == any_(models.ContentWeb.filetypes))

            if filterData["showHaveScriptFilter"] == True:
                or_filters.append(models.ContentWeb.scenariy != '')

            if filterData["showUnknownFileTypeFilter"] == True:
                or_filters.append('Неопределено' == any_(models.ContentWeb.filetypes))

            if filterData["showNoFileFilter"] == True:
                or_filters.append(models.ContentWeb.rasshireniefailacontenta == '')

            if filterData["isExample"] == True:
                or_filters.append(models.ContentWeb.primer == True)

            for item in filterData["brand_list"]:
                filters_list_brand.append(item == any_(models.ContentWeb.brand_list))

            for item in filterData["contragent_list"]:
                filters_list_contragent.append(item == any_(models.ContentWeb.contragent_list))

            for item in filterData["kl"]:
                filters_list_kl.append(item == models.ContentWeb.kl)

            for item in filterData["otvetstvenniy"]:
                filters_list_otvetstvenniy.append(item == models.ContentWeb.otvetstvenniy)

            if len(or_filters) == 0:
                or_filters.append(True)

            if len(filters_list_brand) == 0:
                filters_list_brand.append(True)

            if len(filters_list_contragent) == 0:
                filters_list_contragent.append(True)

            if len(filters_list_kl) == 0:
                filters_list_kl.append(True)

            if len(filters_list_otvetstvenniy) == 0:
                filters_list_otvetstvenniy.append(True)

            if len(additional_filter) == 0:
                additional_filter.append(True)

            filters_list = or_(*filters_list_kl) & or_(*filters_list_brand) & or_(*filters_list_contragent) & or_(*filters_list_otvetstvenniy) & and_(*or_filters) & or_(*additional_filter)
        
            if filterData["current_filter"] == "brand_list":
                
                filters_list_excluded_current = or_(*filters_list_kl) & or_(*filters_list_contragent) & or_(*filters_list_otvetstvenniy) & and_(*or_filters) & or_(*additional_filter)

            elif filterData["current_filter"] == "contragent_list":
                
                filters_list_excluded_current = or_(*filters_list_kl) & or_(*filters_list_brand) & or_(*filters_list_otvetstvenniy) & and_(*or_filters) & or_(*additional_filter)

            elif filterData["current_filter"] == "otvetstvenniy":
                
                filters_list_excluded_current = or_(*filters_list_kl) & or_(*filters_list_brand) & or_(*filters_list_contragent) & and_(*or_filters) & or_(*additional_filter)

            elif filterData["current_filter"] == "kl":
                
                filters_list_excluded_current = or_(*filters_list_brand) & or_(*filters_list_contragent) & or_(*filters_list_otvetstvenniy) & and_(*or_filters) & or_(*additional_filter)

            if filterData["current_filter"] == "otvetstvenniy":
                response_of_responsibles = select(models.ContentWeb.otvetstvenniy).filter(filters_list_excluded_current).group_by(models.ContentWeb.otvetstvenniy)
            else:
                response_of_responsibles = select(models.ContentWeb.otvetstvenniy).filter(filters_list).group_by(models.ContentWeb.otvetstvenniy)

            result = db.execute(response_of_responsibles)
            for item in result:
                return_dict["otvetstvenniy"].append(item.otvetstvenniy) if not item.otvetstvenniy in filterData['otvetstvenniy'] else True

            if filterData["current_filter"] == "brand_list":
                response_of_brand = select(models.ContentWeb.brand_list).filter(filters_list_excluded_current).group_by(models.ContentWeb.brand_list)
            else:
                response_of_brand = select(models.ContentWeb.brand_list).filter(filters_list).group_by(models.ContentWeb.brand_list)

            result = db.execute(response_of_brand)
            for item in result:
                if item.brand_list is not None:
                    for brand in item.brand_list:
                        return_dict["brand_list"].append(brand) if not return_dict["brand_list"].__contains__(brand) and not brand in filterData['brand_list'] else True

            if filterData["current_filter"] == "contragent_list":
                response_of_contragent = select(models.ContentWeb.contragent_list).filter(filters_list_excluded_current).group_by(models.ContentWeb.contragent_list)
            else:
                response_of_contragent = select(models.ContentWeb.contragent_list).filter(filters_list).group_by(models.ContentWeb.contragent_list)

            result = db.execute(response_of_contragent)
            for item in result:
                if item.contragent_list is not None:
                    for contragent in item.contragent_list:
                        return_dict["contragent_list"].append(contragent) if not return_dict["contragent_list"].__contains__(contragent) and not contragent in filterData['contragent_list'] else True

            if filterData["current_filter"] == "kl":
                response_of_kl = select(models.ContentWeb.kl).filter(filters_list_excluded_current).group_by(models.ContentWeb.kl)
            else:
                response_of_kl = select(models.ContentWeb.kl).filter(filters_list).group_by(models.ContentWeb.kl)

            result = db.execute(response_of_kl)
            for item in result:
                return_dict["kl"].append(item.kl) if not item.kl in filterData['kl'] else True

            subq = select(models.ContentWeb.tekuschiy).filter(filters_list).group_by(models.ContentWeb.tekuschiy).subquery()
            subq_only_false = select(models.ContentWeb.tekuschiy).filter(filters_list & (models.ContentWeb.tekuschiy == False)).group_by(models.ContentWeb.tekuschiy).subquery()
            only_false = False
            response_of_current = select(func.count(subq.c.tekuschiy))
            result = db.execute(response_of_current)
            for item in result:
                if item.count == 1:
                    response_of_current_only_false = select(func.count(subq_only_false.c.tekuschiy))
                    result_only_false = db.execute(response_of_current_only_false)
                    for item_only_false in result_only_false:
                        only_false = item_only_false.count == 1
                        break
                return_dict["showCurrent"] = not (item.count == 1 and only_false) 
                break
            
            subq = select(models.ContentWeb.buduschiy).filter(filters_list).group_by(models.ContentWeb.buduschiy).subquery()
            subq_only_false = select(models.ContentWeb.buduschiy).filter(filters_list & (models.ContentWeb.buduschiy == False)).group_by(models.ContentWeb.buduschiy).subquery()
            only_false = False
            response_of_current = select(func.count(subq.c.buduschiy))
            result = db.execute(response_of_current)
            for item in result:
                if item.count == 1:
                    response_of_current_only_false = select(func.count(subq_only_false.c.buduschiy))
                    result_only_false = db.execute(response_of_current_only_false)
                    for item_only_false in result_only_false:
                        only_false = item_only_false.count == 1
                        break
                return_dict["showFuture"] = not (item.count == 1 and only_false) 
                break

            subq = select(models.ContentWeb.proshedshiy).filter(filters_list).group_by(models.ContentWeb.proshedshiy).subquery()
            subq_only_false = select(models.ContentWeb.proshedshiy).filter(filters_list & (models.ContentWeb.proshedshiy == False)).group_by(models.ContentWeb.proshedshiy).subquery()
            only_false = False
            response_of_current = select(func.count(subq.c.proshedshiy))
            result = db.execute(response_of_current)
            for item in result:
                if item.count == 1:
                    response_of_current_only_false = select(func.count(subq_only_false.c.proshedshiy))
                    result_only_false = db.execute(response_of_current_only_false)
                    for item_only_false in result_only_false:
                        only_false = item_only_false.count == 1
                        break
                return_dict["showPast"] = not (item.count == 1 and only_false) 
                break

            subq = select(models.ContentWeb.bezmp).filter(filters_list).group_by(models.ContentWeb.bezmp).subquery()
            subq_only_false = select(models.ContentWeb.bezmp).filter(filters_list & (models.ContentWeb.bezmp == False)).group_by(models.ContentWeb.bezmp).subquery()
            only_false = False
            response_of_current = select(func.count(subq.c.bezmp))
            result = db.execute(response_of_current)
            for item in result:
                if item.count == 1:
                    response_of_current_only_false = select(func.count(subq_only_false.c.bezmp))
                    result_only_false = db.execute(response_of_current_only_false)
                    for item_only_false in result_only_false:
                        only_false = item_only_false.count == 1
                        break
                return_dict["showWithoutMP"] = not (item.count == 1 and only_false) 
                break

            subq = select(models.ContentWeb.nevypolnennyezadachi).filter(filters_list).group_by(models.ContentWeb.nevypolnennyezadachi).subquery()
            subq_only_false = select(models.ContentWeb.nevypolnennyezadachi).filter(filters_list & (models.ContentWeb.nevypolnennyezadachi == False)).group_by(models.ContentWeb.nevypolnennyezadachi).subquery()
            only_false = False
            response_of_current = select(func.count(subq.c.nevypolnennyezadachi))
            result = db.execute(response_of_current)
            for item in result:
                if item.count == 1:
                    response_of_current_only_false = select(func.count(subq_only_false.c.nevypolnennyezadachi))
                    result_only_false = db.execute(response_of_current_only_false)
                    for item_only_false in result_only_false:
                        only_false = item_only_false.count == 1
                        break
                return_dict["showUndoneTaskFilter"] = not (item.count == 1 and only_false) 
                break

            subq = select(models.ContentWeb.fonoviy).filter(filters_list).group_by(models.ContentWeb.fonoviy).subquery()
            subq_only_false = select(models.ContentWeb.fonoviy).filter(filters_list & (models.ContentWeb.fonoviy == True)).group_by(models.ContentWeb.fonoviy).subquery()
            only_false = False
            response_of_current = select(func.count(subq.c.fonoviy))
            result = db.execute(response_of_current)
            for item in result:
                if item.count == 1:
                    response_of_current_only_false = select(func.count(subq_only_false.c.fonoviy))
                    result_only_false = db.execute(response_of_current_only_false)
                    for item_only_false in result_only_false:
                        only_false = item_only_false.count == 1
                        break
                return_dict["showAdFilter"] = not (item.count == 1 and only_false) 
                break

            subq = select(models.ContentWeb.scenariy).filter(filters_list).group_by(models.ContentWeb.scenariy).subquery()
            subq_only_false = select(models.ContentWeb.scenariy).filter(filters_list & (models.ContentWeb.scenariy == "")).group_by(models.ContentWeb.scenariy).subquery()
            only_false = False
            response_of_current = select(func.count(subq.c.scenariy))
            result = db.execute(response_of_current)
            for item in result:
                if item.count == 1:
                    response_of_current_only_false = select(func.count(subq_only_false.c.scenariy))
                    result_only_false = db.execute(response_of_current_only_false)
                    for item_only_false in result_only_false:
                        only_false = item_only_false.count == 1
                        break
                return_dict["showHaveScriptFilter"] = not (item.count == 1 and only_false) 
                break

            subq = select(models.ContentWeb.naservere).filter(filters_list).group_by(models.ContentWeb.naservere).subquery()
            subq_only_false = select(models.ContentWeb.naservere).filter(filters_list & (models.ContentWeb.naservere == False)).group_by(models.ContentWeb.naservere).subquery()
            only_false = False
            response_of_current = select(func.count(subq.c.naservere))
            result = db.execute(response_of_current)
            for item in result:
                if item.count == 1:
                    response_of_current_only_false = select(func.count(subq_only_false.c.naservere))
                    result_only_false = db.execute(response_of_current_only_false)
                    for item_only_false in result_only_false:
                        only_false = item_only_false.count == 1
                        break
                return_dict["showOnServerFilter"] = not (item.count == 1 and only_false) 
                break

            type_count = {"Аудио": 0,
                        "Видео": 0,
                        "Текст": 0,
                        "Картинка": 0,
                        "Неопределено": 0,
                        "Без файла": 0}
            
            response_of_current = select(models.ContentWeb.filetypes).filter(filters_list).group_by(models.ContentWeb.filetypes)
            response_of_total_type_count = select(func.count(models.ContentWeb.filetypes)).filter(filters_list)
            result = db.execute(response_of_current)
            result_total_number = db.execute(response_of_total_type_count)
            for item in result_total_number:
                total_type_count = item.count
                break

            for item in result:
                if item.filetypes is None:
                    continue

                if len(item.filetypes) == 0:
                    type_count["Без файла"] += 1
                
                for content_type in item.filetypes:
                    if content_type in type_count.keys():
                        type_count[content_type] += 1

            return_dict["showAudioFilter"] = (type_count["Аудио"] > 0)
            return_dict["showImageFilter"] = (type_count["Картинка"] > 0)
            return_dict["showVideoFilter"] = (type_count["Видео"] > 0)
            return_dict["showTextFilter"] = (type_count["Текст"] > 0)
            return_dict["showUnknownFileTypeFilter"] = (type_count["Неопределено"] > 0)
            return_dict["showNoFileFilter"] = (type_count["Без файла"] > 0)

            return_dict["isExample"] = True
            
            response = response.filter(or_(*combined_filter) & and_(*or_filters) & or_(*filters_list_brand) & or_(*filters_list_contragent) & or_(*filters_list_kl) & or_(*filters_list_otvetstvenniy) & or_(*additional_filter) | (models.ContentWeb.primer == True))

            count = response.count()

            max_page = count//size + 1

            response = response.order_by(models.ContentWeb.primer.desc(), models.ContentWeb.datasozdaniya.desc())

            unic_list = response.limit(size).offset(page * size).all()
            
            return max_page, unic_list, count, return_dict
        
        except Exception as e:
            print(f"Error occurred: in get_content {e}")
            return None

def save_data(
        data: dict, 
        db: Session,
        token: str
    ):

    save_status = True
    
    save_data_set = {}
    save_data_set["token"] = token
    
    for key in data:
        save_data_set[key.lower()] = data[key]  

    try:
        delete_request = delete(models.SaveData).where(models.SaveData.token == token)
        db.execute(delete_request)
        insert_request = insert(models.SaveData).values(save_data_set)
        print(insert_request)
        print(insert_request.params)
        db.execute(insert_request)
        db.commit()
    except:
        save_status = False

    return save_status

def get_filters_by_saved_data(
        db: Session,
        token: str
    ):
    return_dict = get_base_dict()
    response = select(models.SaveData).where(models.SaveData.token == token)
    filters_count = db.execute(response).scalar()
    
    if filters_count is not None:
        filters = db.execute(response).scalars().unique().all()
        for item in filters:
            return_dict = {
                            "showVideoFilter": item.showvideofilter,
                            "showCurrent": item.showcurrent,
                            "showFuture": item.showfuture,
                            "showPast": item.showpast,
                            "showWithoutMP": item.showwithoutmp,
                            "showUndoneTaskFilter": item.showundonetaskfilter,
                            "showHaveScriptFilter": item.showhavescriptfilter,
                            "showAdFilter": item.showadfilter,
                            "showOnServerFilter": item.showonserverfilter,
                            "showAudioFilter": item.showaudiofilter,
                            "showImageFilter": item.showimagefilter,
                            "showTextFilter": item.showtextfilter,
                            "showUnknownFileTypeFilter": item.showunknownfiletypefilter,
                            "showNoFileFilter": item.shownofilefilter,
                            "current_filter": item.current_filter,
                            "brand_list": item.brand_list,
                            "contragent_list": item.contragent_list,
                            "kl": item.kl,
                            "otvetstvenniy": item.otvetstvenniy,
                            "isExample": item.isexample
                        }

    return return_dict


def get_base_dict():

    return {
            "showVideoFilter": False,
            "showCurrent": False,
            "showFuture": False,
            "showPast": False,
            "showWithoutMP": False,
            "showUndoneTaskFilter": False,
            "showHaveScriptFilter": False,
            "showAdFilter": True,
            "showOnServerFilter": False,
            "showAudioFilter": False,
            "showImageFilter": False,
            "showTextFilter": False,
            "showUnknownFileTypeFilter": False,
            "showNoFileFilter": False,
            "current_filter": "",
            "brand_list": [],
            "contragent_list": [],
            "kl": [],
            "otvetstvenniy": [],
            "isExample": True,
            "search": ""
        }
