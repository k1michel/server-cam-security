from typing import Optional   
from fastapi import FastAPI, APIRouter, UploadFile, File
from pydantic import BaseModel  
from datetime import datetime
from time import sleep
import uvicorn
from os import getcwd
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from BBDD import Basededatos

servidor = APIRouter()
api = FastAPI()
basededatos = Basededatos()
ahora = datetime.now()
fecha = ahora.strftime("%Y-%m-%d_%H-%M-%S")

class Envios(BaseModel):
    video = str
    ano = int
    mes = int
    dia = int
    hora = int
    minuto = int


@servidor.post("/upload")
async def post_upload(file: UploadFile = File(...)):
    with open(getcwd() + '/' + file.filename, "wb") as myfile:
        print(file.filename)
        data = await file.read()
        myfile.write(data)
        envio = Envios()
        dict_file = dict(
            video = envio.video,
            ano = envio.ano,
            mes = envio.mes,
            dia = envio.dia,
            hora = envio.hora,
            minuto = envio.minuto,
        )
        dict_file['video']= file.filename
        dict_file['ano'] = int(ahora.strftime("%Y"))
        dict_file['mes'] = int(ahora.strftime("%m"))
        dict_file['dia'] = int(ahora.strftime("%d"))
        dict_file['hora'] = int(ahora.strftime("%H"))
        dict_file['minuto'] = int(ahora.strftime("%M"))
        basededatos.insertar_video(dict_file)
        myfile.close()
    return 'VIDEO RECIBIDO OK'

@servidor.get("/streaming/{name_file}")
async def get_file(name_file:str):
    def iterfile():
        with open(getcwd() + "/" + name_file, mode="rb") as file_like:  # 
            yield from file_like
            
    return StreamingResponse(iterfile(), media_type="video/mp4")

@servidor.get("/download/{name_file}")
async def get_download(name_file: str):
    return FileResponse(getcwd() + "/" + name_file, media_type ="aplication/octet-stream",filename= name_file)



if __name__ == "__main__":
    uvicorn.run(servidor, host="0.0.0.0", port=8000)

