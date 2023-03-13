from typing import Optional   
from fastapi import FastAPI, APIRouter, UploadFile, File
from pydantic import BaseModel  
from datetime import datetime
from time import sleep
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from BBDD import Basededatos

api = FastAPI()
basededatos = Basededatos()
ahora = datetime.now()
fecha = ahora.strftime("%Y-%m-%d_%H-%M-%S")

@api.get("/videos")
def get_videos():
    
    return basededatos.mostrar_video()

@api.delete("/borrar")
def get_borrar():
    basededatos.eliminar_video()
    return 'BBDD Eliminada OK'

if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=5000)