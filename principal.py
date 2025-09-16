from flask import Flask, render_template, request

programa = Flask(__name__)

@programa.route("/")
def raiz():
    return render_template("index.html")

@programa.route("/login", methods=['POST'])
def login():
    id = request.form['id']
    contra = request.form['contra']
    if id=="afvelasco" and contra=="1234":
        return render_template("bienvenido.html")
    else:
        return render_template("index.html", msg="Credenciales inválidas")

if __name__ == "__main__":
    programa.run(host="0.0.0.0",port="5080",debug=True)