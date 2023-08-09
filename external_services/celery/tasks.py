from celery import Celery
from services import SonnikTypeResponse, Sonnik

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def run_sonnik_interpretation(text_image: str) -> SonnikTypeResponse:
    sonnik = Sonnik()
    return sonnik.interpret(text_image.strip())
