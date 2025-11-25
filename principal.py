from conexion import *
import routes.usuarios
import routes.productos

@programa.route("/uploads/<nombre>")
def uploads(nombre):
    return send_from_directory(programa.config['CARPETA_UP'],nombre)

@programa.route("/")
def raiz():
    return render_template("index.html")

if __name__ == "__main__":
    programa.run(host="0.0.0.0",port="5080",debug=True)