from conexion import *
from models.productos import mi_productos

@programa.route("/productos")
def productos():
    if session.get("login")==True:
        resultado = mi_productos.consultar()
        return render_template("productos.html", pro=resultado)
    else:
        return redirect("/")

@programa.route("/agregaproducto")
def agregaproducto():
    if session.get("login")==True:
        return render_template("agregaproducto.html")
    else:
        return redirect("/") 

@programa.route("/guardaproducto", methods=["POST"])
def guardaproducto():
    if session.get("login")==True:
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        foto = request.files['foto']
        resultado = mi_productos.consulta_codigo(codigo)
        if len(resultado)>0:
            return render_template("agregaproducto.html",msg="Código de producto ya existe")
        else:
            nom,ext = os.path.splitext(foto.filename)
            nombre_foto = 'P' + codigo + ext
            foto.save("uploads/"+nombre_foto)
            mi_productos.agregar(codigo,nombre,precio,stock,nombre_foto)
            return redirect("/productos")
    else:
        return redirect("/") 

@programa.route("/editaproducto/<codigo>")
def editaproducto(codigo):
    if session.get("login")==True:
        resultado = mi_productos.consulta_codigo(codigo)[0]
        return render_template("editaproducto.html",pro=resultado)
    else:
        return redirect("/") 

@programa.route("/actualizaproducto", methods=["POST"])
def actualizaproducto():
    if session.get("login")==True:
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        foto = request.files['foto']
        mi_productos.modificar(codigo, nombre, precio, stock, foto)
        return redirect("/productos")
    else:
        return redirect("/")

@programa.route("/borraproducto/<codigo>")
def borraproducto(codigo):
    if session.get("login")==True:
        mi_productos.borrar(id)
        return redirect("/productos")
    else:
        return redirect("/") 
