from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.get("/nomenclatureplacing")
async def get_nomenclature_placing(db: Session = Depends(get_db)):
    nomenclature = crud.get_nomenclature_placing_from_db(db=db)
    return nomenclature


@app.get("/test")
def get_something():
    print('got_something')
