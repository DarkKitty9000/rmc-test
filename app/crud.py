from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models, schemas


def get_nomenclature_placing_from_db(db: Session):
    return db.query(models.NomenclaturePlacing).all()


def get_nomenclature_placing_from_db_for_user(db: Session, token: str):
    try:
        user = db.query(models.Token).filter(models.Token.token == token).first()
    except:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")
    try:
        return db.query(models.NomenclaturePlacing).filter(models.NomenclaturePlacing.owner_id == user.user_id)
    except:
        return None
