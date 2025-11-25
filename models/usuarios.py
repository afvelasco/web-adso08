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

    def modificar(self, id, nombre, foto):
        sql = f"UPDATE usuarios SET nombre='{nombre}' WHERE id='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
        if foto.filename != "":
            nom,ext = os.path.splitext(foto.filename)
            nombre_foto = id + ext
            foto.save("uploads/"+nombre_foto)
            sql = f"UPDATE usuarios SET foto='{nombre_foto}' WHERE id='{id}'"
            mi_cursor.execute(sql)
            mi_db.commit()
    
    def borrar(self, id):
        sql = f"UPDATE usuarios SET estado=1 WHERE id='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()

    def loguear(self, id, contra):
        cifrada = hashlib.sha512(contra.encode("UTF-8")).hexdigest()
        sql = f"SELECT nombre FROM usuarios WHERE id='{id}' AND contrasena='{cifrada}' AND estado=0"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        if len(resultado)>0:
            return [True,resultado[0][0]]
        else:
            return [False,""]



mi_usuarios = Usuarios()