from flask import Flask, redirect, render_template, request, send_from_directory
import hashlib
import mysql.connector
import os

programa = Flask(__name__)
programa.config['CARPETA_UP'] = os.path.join('uploads')
mi_db = mysql.connector.connect(host="localhost",
                                port=3306,
                                user="root",
                                password="",
                                database="db-adso08")
mi_cursor = mi_db.cursor()

@programa.route("/uploads/<nombre>")
def uploads(nombre):
    return send_from_directory(programa.config['CARPETA_UP'],nombre)

@programa.route("/")
def raiz():
    return render_template("index.html")

@programa.route("/login", methods=['POST'])
def login():
    id = request.form['id']
    contra = request.form['contra']
    cifrada = hashlib.sha512(contra.encode("UTF-8")).hexdigest()
    sql = f"SELECT nombre,contrasena,estado FROM usuarios WHERE id='{id}'"
    mi_cursor.execute(sql)
    resultado = mi_cursor.fetchall()
    if len(resultado)==0:
        return render_template("index.html", msg="Credenciales incorrectas")
    elif resultado[0][1]!=cifrada:
        return render_template("index.html", msg="Credenciales incorrectas")
    elif resultado[0][2]!=0:
        return render_template("index.html", msg="Usuario bloqueado")
    else:
        return render_template("bienvenido.html")

@programa.route("/usuarios")
def usuarios():
    sql = "SELECT * FROM usuarios WHERE estado=0"
    mi_cursor.execute(sql)
    resultado = mi_cursor.fetchall()
    return render_template("usuarios.html", usu=resultado)

@programa.route("/agregausuario")
def agregausuario():
    return render_template("agregausuario.html")

@programa.route("/guardausuario", methods=["POST"])
def guardausuario():
    id = request.form['id']
    nombre = request.form['nom']
    contra = request.form['contra']
    confir = request.form['confir']
    foto = request.files['foto']
    if contra!=confir:
        return render_template("agregausuario.html",msg="Contraseñas no coinciden")
    else:
        sql = f"SELECT nombre FROM usuarios WHERE id='{id}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        if len(resultado)>0:
            return render_template("agregausuario.html",msg="Id de usuario ya existe")
        else:
            cifrada = hashlib.sha512(contra.encode("UTF-8")).hexdigest()
            nom,ext = os.path.splitext(foto.filename)
            nombre_foto = id + ext
            foto.save("uploads/"+nombre_foto)
            sql = f"INSERT INTO usuarios (id,nombre,contrasena,foto) VALUES ('{id}','{nombre}','{cifrada}','{nombre_foto}')"
            mi_cursor.execute(sql)
            mi_db.commit()
            return redirect("/usuarios")

@programa.route("/borrausuario/<id>")
def borrausuario(id):
    sql = f"UPDATE usuarios SET estado=1 WHERE id='{id}'"
    mi_cursor.execute(sql)
    mi_db.commit()
    return redirect("/usuarios")

if __name__ == "__main__":
    programa.run(host="0.0.0.0",port="5080",debug=True)