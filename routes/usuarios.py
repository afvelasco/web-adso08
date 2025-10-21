from conexion import *
from models.usuarios import mi_usuarios

@programa.route("/usuarios")
def usuarios():
    if session.get("login")==True:
        resultado = mi_usuarios.consultar()
        return render_template("usuarios.html", usu=resultado)
    else:
        return redirect("/")

@programa.route("/agregausuario")
def agregausuario():
    if session.get("login")==True:
        return render_template("agregausuario.html")
    else:
        return redirect("/") 

@programa.route("/guardausuario", methods=["POST"])
def guardausuario():
    if session.get("login")==True:
        id = request.form['id']
        nombre = request.form['nom']
        contra = request.form['contra']
        confir = request.form['confir']
        foto = request.files['foto']
        if contra!=confir:
            return render_template("agregausuario.html",msg="Contraseñas no coinciden")
        else:
            resultado = mi_usuarios.consulta_id(id)
            if len(resultado)>0:
                return render_template("agregausuario.html",msg="Id de usuario ya existe")
            else:
                cifrada = hashlib.sha512(contra.encode("UTF-8")).hexdigest()
                nom,ext = os.path.splitext(foto.filename)
                nombre_foto = id + ext
                foto.save("uploads/"+nombre_foto)
                mi_usuarios.agregar(id,nombre,cifrada,nombre_foto)
                return redirect("/usuarios")
    else:
        return redirect("/") 

@programa.route("/editausuario/<id>")
def editausuario(id):
    if session.get("login")==True:
        resultado = mi_usuarios.consulta_id(id)[0]
        return render_template("editausuario.html",usu=resultado)
    else:
        return redirect("/") 

@programa.route("/actualizausuario", methods=["POST"])
def actualizausuario():
    if session.get("login")==True:
        id = request.form['id']
        nombre = request.form['nom']
        foto = request.files['foto']
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
        return redirect("/usuarios")
    else:
        return redirect("/") 
