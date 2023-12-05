## Instrucciones para usar el entorno virtual desde 0

1. Clona este repositorio en tu sistema.
2. Crea y activa un entorno virtual dentro de myapi:

   @/myapi:

   python -m venv venv
   (uno de estos funciona)
   python3 -m venv venv

   source venv/bin/activate  # En sistemas Unix/Linux
   venv\Scripts\activate  # En sistemas Windows

3. Ejecutar: pip install -r requirements.txt


## Instrucciones para usar el venv ya creado

1. Modificar ruta SQL en app>config.py
2. Utilizar port deseado en app>run.py

## si los imports no te cargan

1. Veremos el import en amarillo
2. Usamos el foco para definir el intérprete de ese import
3. En nuestro caso Python 3.10 de nuestro venv.
4. Nuestro venv se habrá creado donde estemos trabajando en la terminal
5. Debería ser /tu-ruta/venv/bin/python3.10
6. Listo