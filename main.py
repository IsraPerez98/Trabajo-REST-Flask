from flask import Flask, request
from flask_cors import CORS, cross_origin

import re

app = Flask(__name__)
#api = Api(app)
api = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

def verificarRut(rut):
    #True si el digito verificador es valido, False en otro caso
    #se utiliza el algoritmo de modulo 11
    #https://validarutchile.cl/calcular-digito-verificador.php

    rut_separado = rut.split('-')

    #invertimos la cifra antes del digito verificador
    rut_reversa = rut_separado[0][::-1]

    print(rut_reversa)

    #multiplicaremos por esta serie
    serie = (2, 3, 4, 5, 6, 7)
    indice_serie = 0 # el indice del arreglo anterior

    #almacenamos la suma total de las multiplicaciones
    suma_total = 0

    for digito in rut_reversa:
        digito_int = int(digito)

        multiplicacion = digito_int * serie[indice_serie]

        suma_total += multiplicacion

        indice_serie += 1

        if (indice_serie >= 6):
            indice_serie = 0

    #el digito verificador correspondiente al rut
    digito_calculado = str(11 - (suma_total % 11))

    # si el valor es 11, convertimos a 0
    if(digito_calculado == "11"):
        digito_calculado = "0"
    # si es 10, entonces convertimos a k
    elif(digito_calculado == "10"):
        digito_calculado = "k"
    
    #el digito que ingreso el usuario
    digito_usuario = rut_separado[1].lower()

    print("Digito calculado es: ", digito_calculado)
    print("Digito ingresado es: ", digito_usuario)

    if(digito_calculado == digito_usuario):
        return True
    
    return False

@app.route("/digitoverificador/", methods=['POST', 'OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def digitoVerificador():
        try:
            data = request.get_json(force=True)
        except:
            return "JSON con mal formato", 400
        print(data)

        if 'rut' not in data:
            return "RUT no ingresado", 400

        rut = data['rut']

        x = re.search("^[0-9-]*$", rut)

        if not x:
            return "Escriba el rut sin puntos y con guion ej: 12345678-9", 400
        
        if(len(rut) > 10):
            return "El rut no puede tener mas de 10 caracteres", 400
        


        es_valido = verificarRut(rut)
        
        if(es_valido):
            return "El Rut Ingresado es Valido", 200
        else:
            return "El Rut Ingresado NO es Valido", 400

@app.route("/nombrepropio/", methods=['POST', 'OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def nombrePropio():
    data = request.get_json(force=True)
    print(data)

    apellido_paterno = data["apellido paterno"].title()
    apellido_materno = data["apellido materno"].title()
    nombres = data["nombres"].title()
    genero = data["genero"].lower()

    if(genero == "m"):
        return "Sr. %s %s %s" % (nombres, apellido_paterno, apellido_materno), 200
    elif (genero == "f"):
        return "Sra. %s %s %s" % (nombres, apellido_paterno, apellido_materno), 200
    else:
        return "El genero debe ser M o F", 400



if __name__ == "__main__":
    app.run(debug=True)