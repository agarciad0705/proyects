from flask import Flask, jsonify, request
import phonenumbers
from phonenumbers import geocoder

app = Flask(__name__)

@app.route('/ping')
def ping():
    return jsonify({"Pong!":""})

from products import products
@app.route('/products', methods = ['GET'])
def getProducts():
    return jsonify({"Products:":products})

    
@app.route('/products/<string:name>', methods = ['GET'])
def getProduct(name):
    print(name)
    product = [product for product in products if product['nombre']==name]
    if(len(product)>0):
        return jsonify(product[0])
    return jsonify({"Products:":"producto no encontrado"})


@app.route('/products', methods = ['POST'])
def addProductPost():
    num = request.json['data']
    x = phonenumbers.parse("2134160509", None)
    geo = geocoder.description_for_number(x, "es")
    print(geo)
    return jsonify(geo)

if __name__ == '__main__':
    app.run(debug=True, port=4000)