## Home Cloud Server
<p>Como indica la descripción, este código es sobre el desarrollo del servidor de Home Cloud Casero, la idea principal del servidor es la administracion de archivos y directorios dentro de una determinada carpeta de nuestro sistema operativo.</p>

## Instalacion del proyecto en sistemas locales
Paso 1: Clonar el repositorio

Paso 2: Generar entorno virtual e instalacion de dependencias

```bash
python -m venv venv  # Si el entorno virtual aún no está creado
source venv/bin/activate  # En Linux/macOS
.\venv\Scripts\activate  # En Windows
pip install -r requirements.txt
```
Paso 3: Generar un archivo .env con una variable de entorno llamada RUTA_CARPETA, haciendo referencia a la ruta de la carpeta donde desea realizar la administracion de los archivos y directorios.

Paso 4: Ejecutar el script uvicorn main:app --reload 
