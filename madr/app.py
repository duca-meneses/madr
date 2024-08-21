from fastapi import FastAPI

from madr.routers import account, auth

app = FastAPI(title='MADR', summary='Meu Acervo Digital de Romances')

app.include_router(account.router)
app.include_router(auth.router)


@app.get('/')
async def read_root():
    return {'server': 'up'}
