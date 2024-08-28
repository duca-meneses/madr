from fastapi import FastAPI

from madr.routers import account, auth, book, novelist

app = FastAPI(title='MADR', summary='Meu Acervo Digital de Romances')

app.include_router(account.router)
app.include_router(auth.router)
app.include_router(book.router)
app.include_router(novelist.router)


@app.get('/', tags=['heath_check'])
async def read_root():
    return {'server': 'up'}
