from flask import Flask, render_template, request
import hashlib
import mysql.connector

programa = Flask(__name__)
mi_db = mysql.connector.connect(host="localhost",
                                port=3306,
                                user="root",
                                password="",
                                database="db-adso08")
mi_cursor = mi_db.cursor()

@programa.route("/")
def raiz():
    return render_template("index.html")

@programa.route("/login", methods=['POST'])
def login():
    id = request.form['id']
    contra = request.form['contra']
    cifrada = hashlib.sha512(contra.encode("UTF-8")).hexdigest()
    sql = f"SELECT nombre,contraseña,estado FROM usuarios WHERE id='{id}'"
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

if __name__ == "__main__":
    programa.run(host="0.0.0.0",port="5080",debug=True)