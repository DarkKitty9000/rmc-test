from sqlalchemy import select, orm, or_, func
from sqlalchemy.orm import Session
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

    response = db.query(models.ContentWeb)

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
                response = response.filter(or_(*or_filters))
            
            response = response.order_by(models.ContentWeb.datasozdaniya.desc())

        else:

            response = response.join(models.ContentWeb.brands, isouter = True).join(models.ContentWeb.contragents, isouter = True).\
                join(models.ContentWeb.contact_persons, isouter=True).filter((models.Brand.full_name.like(f'%{filterData["search"]}%'))|
                                                                (models.ContentWeb.contentkod.like(f'%{filterData["search"]}%'))|
                                                                (models.Contragent.full_name.like(f'%{filterData["search"]}%'))|
                                                                (models.ContactPerson.full_name.like(f'%{filterData["search"]}%'))|
                                                                (models.ContentWeb.naimenovanie.like(f'%{filterData["search"]}%'))).order_by(models.ContentWeb.datasozdaniya.desc())
        
        count = response.count()

        response = response.limit(size).offset((page) * size).all()
        
        return response, count 
    
    else:
    # Получаем всех контрагентов по пользователю.
        contragents = get_contragent_by_user(db = db, user = user)
        try:
            response = response.join(models.ContentWeb.brands,isouter = True).join(models.ContentWeb.contragents,isouter = True).\
                join(models.ContentWeb.contact_persons,isouter=True).filter(
                    models.Contragent.link.in_(contragents)    
                )
                
            if filterData["search"] != '':

                response = response.filter((models.Brand.full_name.like(f'%{filterData["search"]}%'))|
                                            (models.ContentWeb.contentkod.like(f'%{filterData["search"]}%'))|
                                            (models.Contragent.full_name.like(f'%{filterData["search"]}%'))|
                                            (models.ContactPerson.full_name.like(f'%{filterData["search"]}%'))|
                                            (models.ContentWeb.naimenovanie.like(f'%{filterData["search"]}%'))).order_by(models.ContentWeb.datasozdaniya.desc())
                
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
                    response = response.filter(or_(*or_filters))

                response = response.order_by(models.ContentWeb.datasozdaniya.desc())

            count = response(func.count(models.ContentWeb.link))
            
            response = response.limit(size).offset((page) * size).all()

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
