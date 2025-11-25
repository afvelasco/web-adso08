from conexion import *

class Productos:
    def consultar(self):
        sql = "SELECT * FROM productos WHERE estado=0"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado
    
    def consulta_codigo(self, codigo):
        sql = f"SELECT codigo,nombre,precio,stock,foto FROM productos WHERE codigo='{codigo}' and estado=0"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def agregar(self, codigo,nombre,precio,stock,nombre_foto):
        sql = f"INSERT INTO productos (codigo,nombre,precio,stock,foto) VALUES ('{codigo}','{nombre}','{precio}','{stock}','{nombre_foto}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def modificar(self, codigo,nombre,precio,stock,foto):
        sql = f"UPDATE productos SET nombre='{nombre}' precio={precio} stock={stock} WHERE codigo='{codigo}'"
        mi_cursor.execute(sql)
        mi_db.commit()
        if foto.filename != "":
            nom,ext = os.path.splitext(foto.filename)
            nombre_foto = codigo + ext
            foto.save("uploads/"+nombre_foto)
            sql = f"UPDATE productos SET foto='{nombre_foto}' WHERE codigo='{codigo}'"
            mi_cursor.execute(sql)
            mi_db.commit()
    
    def borrar(self, codigo):
        sql = f"UPDATE productos SET estado=1 WHERE codigo='{codigo}'"
        mi_cursor.execute(sql)
        mi_db.commit()

mi_productos = Productos()