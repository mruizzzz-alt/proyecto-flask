from flask import Blueprint 
from flask import render_template 
from flask import request
from database import mysql 
from flask import session, redirect, url_for  
from werkzeug.security import check_password_hash, generate_password_hash

 
login = Blueprint("login",__name__) 
 
@login.route("/") 
def inicio(): 
    cursor = mysql.connection.cursor() 
    cursor.execute("SELECT COUNT(*) FROM usuarios") 
    total = cursor.fetchone() 
    cursor.close() 
    return render_template("acceso/inicio.html",total_usuarios=total[0]) 

@login.route("/registro", methods=["GET", "POST"]) 
def registro(): 
    mensaje = "" 
    tipo_mensaje = "" 
 
    if request.method == "POST": 
        cedula = request.form["cedula"] 
        nombres = request.form["nombres"] 
        apellidos = request.form["apellidos"] 
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        password = request.form["password"]
        

        cursor = mysql.connection.cursor() 
        cursor.execute("""SELECT id FROM usuarios WHERE cedula = %s""",(cedula,)) 
        usuario = cursor.fetchone() 
 
        if usuario: 
            mensaje = "La cédula ya está registrada." 
            tipo_mensaje = "danger" 
        else: 
            password_encriptado = generate_password_hash(password) 
 
            sql = """INSERT INTO usuarios(cedula,nombres,apellidos,telefono,correo,password,rol) 
            VALUES 
            (%s,%s,%s,%s,%s,%s,'Cliente')""" 
 
            cursor.execute(sql,(cedula,nombres,apellidos,telefono,correo,password_encriptado)) 
            mysql.connection.commit() 
 
 
            mensaje = "Usuario registrado correctamente." 
            tipo_mensaje = "success" 
 
        cursor.close() 
 
    return render_template("acceso/registro.html", mensaje=mensaje, tipo_mensaje=tipo_mensaje)

@login.route("/sesion", methods=["GET","POST"]) 
def iniciar_sesion(): 
    mensaje = "" 
 
    if request.method == "POST": 
        cedula = request.form["cedula"] 
        password = request.form["password"] 
        cursor = mysql.connection.cursor() 
 
        cursor.execute("""SELECT id,nombres,apellidos,password,rol FROM usuarios WHERE cedula=%s""",(cedula,)) 
        usuario = cursor.fetchone() 

        if usuario: 
            password_bd = usuario[3] 
            if check_password_hash(password_bd,password): 
                session["id"] = usuario[0] 
                session["nombre"] = usuario[1] 
                session["rol"] = usuario[4] 
 
                cursor.close() 
 
                if usuario[4] == "Administrador": 
                    return redirect(url_for("administrador.dashboard")) 
 
                else: 
                    return redirect(url_for("cliente.dashboard")) 
 
            else: 
 
                mensaje = "Contraseña incorrecta." 
        else: 
            mensaje = "La cédula no está registrada." 
 
        cursor.close() 
 
    return render_template("acceso/login.html",mensaje=mensaje) 
@login.route("/cerrar_sesion") 
def cerrar_sesion(): 
    session.clear() 
    return redirect(url_for("login.inicio")) 