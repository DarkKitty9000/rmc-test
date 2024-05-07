from fastapi import FastAPI

app = FastAPI()


@app.get("/nomenclatureplacing")
async def get_nomenclature_placing():

    result = {
        ''
    }


@app.get("/test")
def get_something():
    print('got_something')
