from flask import Flask 
from database import mysql 
from rutas.login import login 
from rutas.administrador import administrador 
from rutas.cliente import cliente 
app = Flask(__name__) 

app.config["MYSQL_HOST"] = "localhost" 
app.config["MYSQL_USER"] = "root" 
app.config["MYSQL_PASSWORD"] = "" 
app.config["MYSQL_DB"] = "renta_vehiculos" 

app.secret_key = "123456" 

mysql.init_app(app) 

app.register_blueprint(login) 
app.register_blueprint(administrador) 
app.register_blueprint(cliente) 
 
if __name__ == "__main__": 
    app.run(debug=True) 