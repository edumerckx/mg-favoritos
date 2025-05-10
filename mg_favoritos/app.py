from fastapi import FastAPI

from mg_favoritos.routes.auth import router as auth_router
from mg_favoritos.routes.clients import router as clients_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(clients_router)


@app.get('/')
def main():
    return {'message': 'mg-favoritos'}
