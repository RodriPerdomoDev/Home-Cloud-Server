from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

carpeta = os.environ.get("RUTA_CARPETA")

# Enpoint para listar archivos o directorios dependiendo el nombre de la carpeta que me pasen por parametro de la url


@router.get("/{nombre_carpeta}")
def obtener_datos_from_carpeta(nombre_carpeta: str):
    ruta_carpeta = f"{carpeta}/{nombre_carpeta}"
    if os.path.exists(ruta_carpeta) and os.path.isdir(ruta_carpeta):
        archivos_en_carpeta = os.listdir(f"{carpeta}/{nombre_carpeta}")
        archivo_lista = []
        carpeta_lista = []
        for archivo_nombre in archivos_en_carpeta:
            ruta_completa = os.path.join(
                f"{carpeta}/{nombre_carpeta}", archivo_nombre)
            if os.path.isfile(ruta_completa):
                archivo_lista.append(archivo_nombre)
            else:
                carpeta_lista.append(archivo_nombre)
        return {"archivos": archivo_lista, "carpetas": carpeta_lista}
    else:
        return JSONResponse(content={"mensaje": f"La carpeta {ruta_carpeta} no existe"}, status_code=404)

# Endpoint para descargar archivos desde una ruta especifica es decir carpeta + nombre carpeta de donde se quiere descargar


@router.post("/{nombre_carpeta}/descargar")
def descargar_archivo_desde_carpeta(nombre_carpeta: str, nombre_archivo: str):
    ruta_archivo_desde_carpeta = f"{carpeta}/{nombre_carpeta}/{nombre_archivo}"
    ruta_carpeta = f"{carpeta}/{nombre_carpeta}"
    if os.path.exists(ruta_carpeta) and os.path.isdir(ruta_carpeta):
        if os.path.exists(ruta_archivo_desde_carpeta):
            archivo_descargar = os.path.join(ruta_archivo_desde_carpeta)
            return FileResponse(archivo_descargar, media_type="aplication/octet-stream", filename=nombre_archivo)
        else:
            return JSONResponse(content={"mensaje": f"El archivo {nombre_archivo} no existe"}, status_code=404)
    else:
        return JSONResponse(content={"mensaje": f"La carpeta {nombre_carpeta} no existe"}, status_code=404)

# Endpoint para subir archivos a una determinada carpeta


@router.post("/{nombre_carpeta}/subir")
def subir_archivo_a_determinada_carpeta(nombre_carpeta: str, archivo: UploadFile = File(...)):
    ruta_completa = f"{carpeta}/{nombre_carpeta}/{archivo.filename}"
    with open(ruta_completa, "wb") as f:
        f.write(archivo.file.read())
    return {"mensaje": "Archivo guardado con exito"}

# Endpoint para eliminar archivos desde una determinada carpeta


@router.delete("/{nombre_carpeta}/eliminar")
def eliminar_archivo_desde_determinada_carpeta(nombre_carpeta: str, archivo_nombre: str):
    ruta_completa = f"{carpeta}/{nombre_carpeta}/{archivo_nombre}"
    if os.path.exists(ruta_completa):
        os.remove(ruta_completa)
        return {"mensaje": f"El archivo {archivo_nombre} se elimino con exito"}
    else:
        return JSONResponse(content={"mensaje": f"El archivo {archivo_nombre} no existe"}, status_code=404)
