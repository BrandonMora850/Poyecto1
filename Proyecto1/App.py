from flask import Flask, render_template, request, redirect, url_for, session

from sqlalchemy import create_engine   #crear instancia para base de datos
from sqlalchemy.orm import scoped_session, sessionmaker


import os



app = Flask(__name__)
app.secret_key = "1234"

engine = create_engine("postgres://ouajkbkn:sux35jMh4OOWUHikcOwwqUxCl8WYuJzu@drona.db.elephantsql.com:5432/ouajkbkn") #se conecta a la base de datos
basededatos = scoped_session(sessionmaker(bind=engine))

#index normal
@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/validar", methods=["POST"])
def validar():
    nombrerecibido = request.form.get("Usuario")
    contrarecibida = request.form.get("contra")

    usuarioencontrado = basededatos.execute("SELECT usuario FROM usuarios WHERE usuario=:username",{"username":nombrerecibido}).fetchone()
    contraseñaencontrada = basededatos.execute("SELECT 	contraseña FROM usuarios WHERE usuario=:username",{"username":nombrerecibido}).fetchone()

    if usuarioencontrado is None:
        error = True
        return render_template("index.html", error=error)
    else:
        for passwor_data in contraseñaencontrada:
            if contrarecibida == passwor_data:
                session["user"] = nombrerecibido
                return redirect(url_for('home'))
            else:

                 error = True

            return render_template("index.html", error=error)
    basededatos.commit()

@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    return render_template("index.html")
    #return f"Usuarios : {numerodeusuarios} ! Contraseña : {contrarecibida} !"
@app.route("/home")
def home():
    libreria = basededatos.execute("SELECT * FROM public . libros LIMIT 500")
    filas = libreria.fetchall()
    if "user" in session:
        usuario = session["user"]
        usuarioencontrado = basededatos.execute("SELECT usuario FROM usuarios WHERE usuario=:username",{"username":usuario}).fetchone()
        for row in usuarioencontrado:
            nombre = usuarioencontrado[0]
        return render_template("home.html", filas=filas, nombre=nombre)

@app.route("/busqueda")
def busqueda():
    libreria = basededatos.execute("SELECT * FROM public . libros LIMIT 100")
    filas = libreria.fetchall()
    return render_template("busqueda.html", filas=filas)

@app.route("/buscar", methods=["POST", "GET"])
def buscar():
    busquedarecibida = request.form.get("busqueda")
        #consulta para buscar cualquier resultado entre los campos que coincida con la busqueda
    busquedaencontrada = basededatos.execute("SELECT isbn, titulo, autor, año FROM libros WHERE (LOWER(isbn) LIKE LOWER(:bus)) OR (LOWER(titulo) LIKE LOWER(:bus)) OR (LOWER(autor) LIKE LOWER(:bus)) LIMIT 10", { "bus": '%' + busquedarecibida + '%'} )
    filas = busquedaencontrada.fetchall()
    return render_template("busqueda.html", busquedarecibida = busquedarecibida, busqueda = busqueda, filas=filas)



@app.route("/paginaR")
def paginaR():
    return render_template("Regitrarse.html")

@app.route("/registro", methods=["POST"])
def registro():
    usuarioregistro = request.form.get("Usuario")
    nombreregistro = request.form.get("Nombre")
    RApellidoP = request.form.get("Apellidop")
    RApellidoM = request.form.get("Apellidom")
    contraseñaR = request.form.get("contra")
    correoregistrar = request.form.get("correo")

    registro = False
    Urepetido = basededatos.execute("SELECT usuario FROM usuarios WHERE usuario=:username",{"username":usuarioregistro}).fetchone()

    if usuarioregistro == "" and nombreregistro == "" and RApellidoP == "" and RApellidoM == "" and contraseñaR == "" and correoregistrar == "":
        error = True
        registro = False
        return render_template("Regitrarse.html", error=error)
    if Urepetido is not None:
        duplicado = True
        registro = False
        return render_template("Regitrarse.html", duplicado=duplicado)


    elif usuarioregistro == "" or nombreregistro == "" or RApellidoP == "" or RApellidoM == "" or contraseñaR == "" or correoregistrar == "":
        error = True
        registro = False
        return render_template("Regitrarse.html", error=error)


    else:
        registro = True
        error = False

        basededatos.execute("INSERT INTO usuarios (usuario, nombre, apellidop, apellidom, contraseña, correo) VALUES (:usuario, :nombre, :apellidop, :apellidom, :contraseña, :correo)",{"usuario": usuarioregistro, "nombre": nombreregistro, "apellidop": RApellidoP, "apellidom": RApellidoM, "contraseña": contraseñaR, "correo": correoregistrar})
    basededatos.commit()

    return render_template("index.html", registro=registro)


@app.route("/infolibro", methods=["POST", "GET"])
def infolibro():
    isbnrecibido = request.form.get("isbn")
    datoslibro = basededatos.execute("SELECT isbn, titulo, autor, año  FROM libros WHERE isbn=:isbnrecibido",{"isbnrecibido":isbnrecibido}).fetchall()
    for dato in datoslibro:
        isbn = dato[0]
        titulo  = dato[1]
        autor = dato[2]
        ano = dato[3]
    return render_template("Libro.html", isbn=isbn, titulo=titulo, autor=autor, ano=ano)



if __name__ == '__main__':
    app.run(debug=True)
