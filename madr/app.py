from fastapi import FastAPI

app = FastAPI(title='MADR', summary='Meu Acervo Digital de Romances')


@app.get('/')
def read_root():
    return {'server': 'up'}
