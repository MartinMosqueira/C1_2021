from celery import Celery
from config import config

app = Celery('tasks', broker=config['broker'], backend=config['backend'])

# pasar la configuracion como json
app.conf.CELERY_ACCEPT_CONTENT = ['json']
app.conf.CELERY_TASK_SERIALIZER = 'json'

@app.task
def suma(n, m):
    return n+m

@app.task
def resta(n, m):
    return n-m

@app.task
def mult(n, m):
    return n*m

@app.task
def div(n, m):
    return n/m

@app.task
def pot(n, m):
    return n**m
