from sqlalchemy import select, orm, or_, func, text, any_
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
    

def get_content_web(db: Session) -> models.ContentWeb:
    """
    Метод получения примеров контента
    db - Сессия базы данных,
    token - Токен авторизации пользователя
    Вызывается если пользователь не авторизован
    """
    response = db.query(models.ContentWeb).filter(models.ContentWeb.primer == True)
    count = db.query(func.count(models.ContentWeb.link)).scalar()
    return response, count


def get_content_web_for_user(db: Session, token: str, filterData: str, page: int, size: int) -> models.ContentWeb: 
                           
    """
    Метод получения контента по пользователю.
    db - Сессия базы данных,
    token - Токен авторизации пользователя
    filterData - Данные фильтрации в запросе
    page - отдаваемая страница массива данных
    size - размерность страницы массива данных
    """
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
            return None
    


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
    return [contragent.link for contragent in contragents]

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

def get_content_web_test_non_auth(db: Session) -> models.ContentWeb:
    """
    Метод получения примеров контента
    db - Сессия базы данных,
    token - Токен авторизации пользователя
    Вызывается если пользователь не авторизован
    """
    response = db.query(models.ContentWebTest).filter(models.ContentWebTest.primer == True)
    count = db.query(func.count(models.ContentWebTest.link)).scalar()
    return response, count


def get_content_web_test(db: Session, token: str, filterData: str, page: int, size: int) -> models.ContentWebTest: 
                           
    """
    Метод получения контента по пользователю.
    db - Сессия базы данных,
    token - Токен авторизации пользователя
    filterData - Данные фильтрации в запросе
    page - отдаваемая страница массива данных
    size - размерность страницы массива данных
    """
    user = get_user_by_token(db = db, token = token) # Получаем пользователя

    response = db.query(models.ContentWebTest)

    if user.is_employee:

        if filterData["search"] == "":

            or_filters = []

            if filterData["tekuschiy"] == True:
                or_filters.append(models.ContentWebTest.tekuschiy == True)

            if filterData["buduschiy"] == True:
                or_filters.append(models.ContentWebTest.buduschiy == True)

            if filterData["proshedshiy"] == True:
                or_filters.append(models.ContentWebTest.proshedshiy == True)

            if filterData["bezmp"] == True:
                or_filters.append(models.ContentWebTest.bezmp == True)

            if filterData["is_ad"] == True:
                or_filters.append(models.ContentWebTest.fonoviy == False)

            if or_filters:
                response = response.filter(or_(*or_filters))

        else:
 
            # Разбиваем поиск на отдельные проверки для каждого поля
            brand_filter = func.array_to_string(models.ContentWebTest.brand_list, ';').ilike(f'%{filterData["search"]}%')
            contragent_filter =  func.array_to_string(models.ContentWebTest.contragent_list, ';').ilike(f'%{filterData["search"]}%')

            contentkod_filter = models.ContentWebTest.contentkod.ilike(f'%{filterData["search"]}%')
            contactperson_filter = models.ContentWebTest.kl.ilike(f'%{filterData["search"]}%')
            naimenovanie_filter = models.ContentWebTest.naimenovanie.ilike(f'%{filterData["search"]}%')

            # Объединяем все фильтры с оператором ИЛИ (|)
            combined_filter = brand_filter | contentkod_filter | contragent_filter | contactperson_filter | naimenovanie_filter

            response = response.filter(combined_filter)


        count = response.count()

        response = response.order_by(models.ContentWebTest.datasozdaniya.desc())

        unic_list = response.limit(size).offset(page * size).all()
        
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
        
            count = db.execute(select(func.count()).select_from(subresponse.alias())).scalar()

            response = db.execute(response.limit(size).offset(page * size)).scalars().unique().all()

            return response, count
        except Exception as e:
            print(f"Error occurred: in get_content {e}")
            return None

def get_content_filters(
        db: Session,
        token: str,
        data: dict
):
    user_data = get_user_by_token(db = db, token = token)

    additional_filter = []
    if not user_data.is_employee:
        contrangents = get_contragent_by_user(db = db, user = user_data)
        response_of_additional_sort = select(models.Contragent.full_name).filter(models.Contragent.link.in_(contrangents)).group_by(models.Contragent.full_name)
        result = db.execute(response_of_additional_sort)
        for item in result:
            additional_filter.append(item.full_name == any_(models.ContentWebTest.contragent_list))

    filters_list = []
    filters_list_excluded_current = []
    filters_list_brand = []
    filters_list_contragent = []
    filters_list_otvetstvenniy = []
    filters_list_kl = []
    
    for filter in data["filters_list"]:

        for list_filter in data["filters_list"][filter]:
                
            if filter == "brand_list":
                filters_list_brand.append(list_filter == any_(models.ContentWebTest.brand_list))    
            elif filter == "contragent_list":
                filters_list_contragent.append(list_filter == any_(models.ContentWebTest.contragent_list))
            if filter == "otvetstvenniy":
                filters_list_otvetstvenniy.append(models.ContentWebTest.otvetstvenniy == list_filter)
            elif filter == "kl":
                filters_list_kl.append(models.ContentWebTest.kl == list_filter)

    if len(filters_list_brand) == 0:
        filters_list_brand.append(True)
    if len(filters_list_contragent) == 0:
        filters_list_contragent.append(True)
    if len(filters_list_otvetstvenniy) == 0:
        filters_list_otvetstvenniy.append(True)
    if len(filters_list_kl) == 0:
        filters_list_kl.append(True)
        
    filters_list = or_(*filters_list_kl) & or_(*filters_list_brand) & or_(*filters_list_contragent) & or_(*filters_list_otvetstvenniy)
            
    if data["current_filter"] == "brand_list":
        
        filters_list_excluded_current = or_(*filters_list_kl) & or_(*filters_list_contragent) & or_(*filters_list_otvetstvenniy)

    elif data["current_filter"] == "contragent_list":
        
        filters_list_excluded_current = or_(*filters_list_kl) & or_(*filters_list_brand) & or_(*filters_list_otvetstvenniy)

    elif data["current_filter"] == "otvetstvenniy":
        
        filters_list_excluded_current = or_(*filters_list_kl) & or_(*filters_list_brand) & or_(*filters_list_contragent)

    else:
        
        filters_list_excluded_current = or_(*filters_list_brand) & or_(*filters_list_contragent) & or_(*filters_list_otvetstvenniy)

    if len(additional_filter) > 0:

        filters_list = filters_list & or_(*additional_filter)
        filters_list_excluded_current = filters_list_excluded_current & or_(*additional_filter)

    return_dict = {"brand_list":[], "contragent_list":[], "otvetstvenniy":[], "kl":[]}

    if data["current_filter"] == "otvetstvenniy":
        response_of_responsibles = select(models.ContentWebTest.otvetstvenniy).filter(filters_list_excluded_current).group_by(models.ContentWebTest.otvetstvenniy)
    else:
        response_of_responsibles = select(models.ContentWebTest.otvetstvenniy).filter(filters_list).group_by(models.ContentWebTest.otvetstvenniy)

    print(response_of_responsibles)

    result = db.execute(response_of_responsibles)
    for item in result:
        return_dict["otvetstvenniy"].append(item.otvetstvenniy) if not item.otvetstvenniy in data["filters_list"]['otvetstvenniy'] else True

    if data["current_filter"] == "brand_list":
        response_of_brand = select(models.ContentWebTest.brand_list).filter(filters_list_excluded_current).group_by(models.ContentWebTest.brand_list)
    else:
        response_of_brand = select(models.ContentWebTest.brand_list).filter(filters_list).group_by(models.ContentWebTest.brand_list)

    result = db.execute(response_of_brand)
    for item in result:
        for brand in item.brand_list:
            return_dict["brand_list"].append(brand) if not return_dict["brand_list"].__contains__(brand) and not brand in data["filters_list"]['brand_list'] else True

    if data["current_filter"] == "contragent_list":
        response_of_contragent = select(models.ContentWebTest.contragent_list).filter(filters_list_excluded_current).group_by(models.ContentWebTest.contragent_list)
    else:
        response_of_contragent = select(models.ContentWebTest.contragent_list).filter(filters_list).group_by(models.ContentWebTest.contragent_list)

    print(response_of_contragent)

    result = db.execute(response_of_contragent)
    for item in result:
        for contragent in item.contragent_list:
            return_dict["contragent_list"].append(contragent) if not return_dict["contragent_list"].__contains__(contragent) and not contragent in data["filters_list"]['contragent_list'] else True

    if data["current_filter"] == "kl":
        response_of_kl = select(models.ContentWebTest.kl).filter(filters_list_excluded_current).group_by(models.ContentWebTest.kl)
    else:
        response_of_kl = select(models.ContentWebTest.kl).filter(filters_list).group_by(models.ContentWebTest.kl)

    result = db.execute(response_of_kl)
    for item in result:
        return_dict["kl"].append(item.kl) if not item.kl in data["filters_list"]['kl'] else True

    return return_dict