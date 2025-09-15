1. Crear el entorno virtual

python -m venv env

2. Activar el entorno virtual

En Windows: env\Scripts\activate

En macOS/Linux: source env/bin/activate

3. Instalar las dependencias

pip install -r requirements.txt

4. Levantar el servidor
5. 
cd api uvicorn main:app --reload
