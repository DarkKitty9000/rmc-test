from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models, schemas


def get_nomenclature_placing_from_db(
        db: Session,
        page: int,
        size: int,
    ):
    offset_min = page * size
    offset_max = (page + 1) * size
    response = db.query(models.NomenclaturePlacing).all()
    return response[offset_min: offset_max]


def get_nomenclature_placing_from_db_for_user(
        db: Session,
        token: str,
        page: int,
        size: int,
    ):
    offset_min = page * size
    offset_max = (page + 1) * size
    user = get_user_by_token(db=db, token=token)
    try:
        response = db.query(models.NomenclaturePlacing).filter(
            models.NomenclaturePlacing.owner_link == user.user_link
        )
        return response[offset_min: offset_max]
    except:
        return None
    

def get_user_by_token(db: Session, token: str):
    try:
        return db.query(models.Token).filter(models.Token.token == token).first()
    except:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")
