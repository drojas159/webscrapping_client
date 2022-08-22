import psycopg2
from psycopg2 import Error
conexion = psycopg2.connect(
    user = 'postgres',
    password = 'admin',
    host = '127.0.0.1',
    port = '5432',
    database = 'test_db'
)
try:
    with conexion:
        with conexion.cursor() as cursor:
            print('registro')
            sentencia ='SELECT nombre FROM persona'
            cursor.execute(sentencia)
            registros= cursor.fetchall()
            arre=[]
            for registro in registros:
                arre.append(registro)
            print(arre)
except Exception as e:
    print(f'Ocurrio un error  {e}')
finally:
    
    conexion.close()