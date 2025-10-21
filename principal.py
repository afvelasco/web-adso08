from conexion import *
import routes.usuarios

@programa.route("/uploads/<nombre>")
def uploads(nombre):
    return send_from_directory(programa.config['CARPETA_UP'],nombre)

@programa.route("/")
def raiz():
    return render_template("index.html")

@programa.route("/login", methods=['POST'])
def login():
    id = request.form['id']
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
        session["login"] = True
        session["id"] = id
        session["nombre"] = resultado[0][0]
        return render_template("bienvenido.html")

@programa.route("/borrausuario/<id>")
def borrausuario(id):
    if session.get("login")==True:
        sql = f"UPDATE usuarios SET estado=1 WHERE id='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
        return redirect("/usuarios")
    else:
        return redirect("/") 

if __name__ == "__main__":
    programa.run(host="0.0.0.0",port="5080",debug=True)