from conexion import *

class Usuarios:
    def consultar(self):
        sql = "SELECT * FROM usuarios WHERE estado=0"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado
    
    def consulta_id(self, id):
        sql = f"SELECT id,nombre,foto FROM usuarios WHERE id='{id}' and estado=0"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def agregar(self, id,nombre,cifrada,nombre_foto):
        sql = f"INSERT INTO usuarios (id,nombre,contrasena,foto) VALUES ('{id}','{nombre}','{cifrada}','{nombre_foto}')"
        mi_cursor.execute(sql)
        mi_db.commit()


mi_usuarios = Usuarios()