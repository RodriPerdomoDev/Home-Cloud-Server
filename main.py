from fastapi import FastAPI
from controllers import main_controller, carpeta_controller

app = FastAPI()

app.include_router(main_controller.router)
app.include_router(carpeta_controller.router)
