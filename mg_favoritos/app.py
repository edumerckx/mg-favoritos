from fastapi import FastAPI

from mg_favoritos.routes.auth import router as auth_router
from mg_favoritos.routes.customer import router as customer_router
from mg_favoritos.routes.favorites import router as favorites_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(favorites_router)


@app.get('/')
def main():
    return {'message': 'mg-favoritos'}
