from flask import Flask, request
from flask_restful import Api, Resource, abort

app = Flask(__name__)
api = Api(app)

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

class digitoVerificador(Resource):
    def post(self):
        data = request.get_json(force=True)
        rut = data['rut']

        if('.' in rut):
            return "Escriba el rut sin puntos y con guion ej: 12345678-9", 400

        es_valido = verificarRut(rut)
        
        if(es_valido):
            return "El Rut Ingresado es Valido", 200
        else:
            return "El Rut Ingresado NO es Valido", 400

api.add_resource(digitoVerificador, "/digitoverificador/")

if __name__ == "__main__":
    app.run(debug=True)