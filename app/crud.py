from sqlalchemy import select, orm
from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models, schemas


# Метод для получения мест размещения номенклатуры
def get_nomenclature_placing_from_db(
        db: Session
        # page: int,
        # size: int,
    ):
    """
    Метод для получения мест размещения номенклатуры
    db - Сессия базы данных,
    page - Индекс страницы для пагинации,
    size - Размер страницы для пагинации.
    """
    # offset_min = page * size
    # offset_max = (page + 1) * size
    response = db.query(models.NomenclaturePlacing).all()
    return response #[offset_min: offset_max]


def get_nomenclature_placing_from_db_for_user(
        db: Session,
        token: str,
        # page: int,
        # size: int,
    ):
    """
    Метод для получения мест размещения номенклатуры по пользователю
    db - Сессия базы данных,
    token - Токен авторизации пользователя,
    page - Индекс страницы для пагинации,
    size - Размер страницы для пагинации.
    """
    # offset_min = page * size
    # offset_max = (page + 1) * size

    user = get_user_by_token(db=db, token=token) # Получаем пользователя

    if user.is_employee:
        response = db.query(models.NomenclaturePlacing).all()
        return response #[offset_min: offset_max]

    else:
    # Получаем всех контрагентов по пользователю.
        contragents = get_contragent_by_user(db=db, user=user)
        try:
            response = db.query(models.NomenclaturePlacing).filter(
                models.NomenclaturePlacing.contragents.any(
                    link=contragents[0].link
                )   
            )
            return response#[offset_min: offset_max]
        except:
            return None
    

def get_content_web(db: Session) -> models.ContentWeb:
    """
    Метод получения контента
    *** в разработке
    """
    response = db.query(models.ContentWeb).filter(models.ContentWeb.primer == True)
    return response


def get_content_web_for_user(db: Session, token: str,) -> models.ContentWeb: 
                             #page: int, size: int,) -> models.ContentWeb:
    """
    Метод получения контента по пользователю.
    *** в разработке
    """
    # offset_min = page * size
    # offset_max = (page + 1) * size

    user = get_user_by_token(db=db, token=token) # Получаем пользователя

    if user.is_employee:

        response = db.query(models.ContentWeb).all()

        return response#[offset_min: offset_max]
    
    else:
    # Получаем всех контрагентов по пользователю.
        contragents = get_contragent_by_user(db=db, user=user)
        try:
            response = db.query(models.ContentWeb).filter(
                models.ContentWeb.contragents.any(
                    link=contragents[0].link
             )
         )
            return response#[offset_min: offset_max]
        except:
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
        raise HTTPException(status_code=404, detail="Пользователь не найден.")


def get_contragent_by_user(db: Session, user: models.User):
    """
    Метод получения контрагента по пользователю
    db - Сессия базы данных,
    user - Объект пользователя.
    """
    contragents = db.query(models.Contragent).filter(
        models.Contragent.contact_persons.any(link=user.link)
    ).all()
    return contragents
