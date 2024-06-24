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
    """
    response = db.query(models.ContentWeb).filter(models.ContentWeb.primer == True)
    count = db.query(func.count(models.ContentWeb.link)).scalar()
    return response, count


def get_content_web_for_user(db: Session, token: str, search: str, page: int, size: int) -> models.ContentWeb: 
                             
    """
    Метод получения контента по пользователю.
    """
    user = get_user_by_token(db = db, token = token) # Получаем пользователя

    if user.is_employee:

        if search == "":

            response = db.query(models.ContentWeb).order_by(models.ContentWeb.datasozdaniya.desc()).limit(size).offset((page) * size).all()

        else:

            response = db.query(models.ContentWeb).join(models.ContentWeb.brands, isouter = True).join(models.ContentWeb.contragents, isouter = True).\
                join(models.ContentWeb.contact_persons, isouter=True).filter((models.Brand.full_name.like(f'%{search}%'))|
                                                                (models.ContentWeb.contentkod.like(f'%{search}%'))|
                                                                (models.Contragent.full_name.like(f'%{search}%'))|
                                                                (models.ContactPerson.full_name.like(f'%{search}%'))|
                                                                (models.ContentWeb.naimenovanie.like(f'%{search}%'))).order_by(models.ContentWeb.datasozdaniya.desc()).limit(size).offset((page) * size).all()
        
        count = db.query(func.count(models.ContentWeb.link)).scalar()
        
        return response, count 
    
    else:
    # Получаем всех контрагентов по пользователю.
        contragents = get_contragent_by_user(db = db, user = user)
        try:
            response = db.query(models.ContentWeb).join(models.ContentWeb.brands,isouter = True).join(models.ContentWeb.contragents,isouter = True).\
                join(models.ContentWeb.contact_persons,isouter=True).filter(
                    models.Contragent.link.in_(contragents)    
                )
                
            if search != "":

                 response = response.filter((models.Brand.full_name.like(f'%{search}%'))|
                                            (models.ContentWeb.contentkod.like(f'%{search}%'))|
                                            (models.Contragent.full_name.like(f'%{search}%'))|
                                            (models.ContactPerson.full_name.like(f'%{search}%'))|
                                            (models.ContentWeb.naimenovanie.like(f'%{search}%'))).order_by(models.ContentWeb.datasozdaniya.desc()).limit(size).offset((page) * size).all()
                
            else:

                response = response.order_by(models.ContentWeb.datasozdaniya.desc()).limit(size).offset((page) * size).all()

            count = db.query(func.count(models.ContentWeb.link)).scalar()

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
