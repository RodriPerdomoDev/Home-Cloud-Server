from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

carpeta = os.environ.get("RUTA_CARPETA")


# Endpoint que lista los archivos que hay en el directorio marcado en la variable carpeta

@router.get("/")
def get_directorios_archivos():
    archivos_en_carpeta = os.listdir(carpeta)
    archivo_lista = []
    carpeta_lista = []
    for archivo_nombre in archivos_en_carpeta:
        ruta_completa = os.path.join(carpeta, archivo_nombre)
        if os.path.isfile(ruta_completa):
            archivo_lista.append(archivo_nombre)
        else:
            carpeta_lista.append(archivo_nombre)
    return {"archivos": archivo_lista, "carpetas": carpeta_lista}


# Enpoint para descargar un archivo que recibo por el body, mediante post

@router.post("/descargar")
def descargar_archivos(archivo_nombre: str):
    ruta_completa = os.path.join(carpeta, archivo_nombre)
    return FileResponse(ruta_completa, media_type="aplication/octet-stream", filename=archivo_nombre)


# Endpoint para subir archivos


@router.post("/subir")
def subir_archivo(archivo: UploadFile = File(...)):
    ruta_completa = f"{carpeta}/{archivo.filename}"
    with open(ruta_completa, "wb") as f:
        f.write(archivo.file.read())
    return {"mensaje": "Archivo guardado con exito"}


# Endpoint para eliminar archivos


@router.delete("/eliminar")
def eliminar_archivo(archivo_nombre: str):
    ruta_completa = f"{carpeta}/{archivo_nombre}"
    if os.path.exists(ruta_completa):
        os.remove(ruta_completa)
        return {"mensaje": f"El archivo {archivo_nombre} fue eliminado exitosamente"}
    else:
        return JSONResponse(content={"mensaje": f"El archivo {archivo_nombre} no existe"}, status_code=404)


# Endpoint para crear una carpeta

@router.post("/crear")
def crear_carpeta(nombre_carpeta):
    ruta_carpeta = f"{carpeta}/{nombre_carpeta}"
    if os.path.exists(ruta_carpeta):
        raise HTTPException(
            status_code=500, detail=f"La carpeta {nombre_carpeta} ya existe")
    try:
        os.makedirs(ruta_carpeta)
        return {"mensaje": f"La carpeta {nombre_carpeta} fue creada con exito!"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al crear la carpeta: {e}")
