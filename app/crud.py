from sqlalchemy.orm import Session

from . import models, schemas


def get_nomenclature_placing_from_db(db: Session, ):
    return db.query(models.NomenclaturePlacing).all()
