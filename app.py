from flask import Flask, jsonify, request
import phonenumbers
from phonenumbers import geocoder
import csv

import codecs

app = Flask(__name__)

#curl --request GET \
#  --url 'http://127.0.0.1:4000/phones/(213)%20416-0509'
@app.route('/phones/<string:number>', methods = ['GET'])
def addProductPost(number):
    text = number
    for match in phonenumbers.PhoneNumberMatcher(text, "US"):
        numberFormated = (phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))    
    z = phonenumbers.parse(numberFormated, None)
    validNumber = phonenumbers.is_valid_number(z)
    ch_number = phonenumbers.parse(numberFormated, "CH")
    geo = geocoder.description_for_number(ch_number, "es")
    #numbers, valid, location
    return jsonify({"number":numberFormated,"valid":validNumber, "location":geo})

#curl --request POST \
#  --url http://127.0.0.1:4000/phones/csv \
#  --header 'content-type: multipart/form-data; boundary=---011000010111000001101001' \
#  --form numbers=
@app.route('/phones/csv', methods=['POST'])
def handle_form():
    print("Posted file: {}".format(request.files['numbers']))
           
    file = request.files['numbers']
    read = csv.reader(codecs.iterdecode(file, 'utf-8'))

    my_list = []
    for row in read:
        #print(row[0])
        for match in phonenumbers.PhoneNumberMatcher(row[0], "US"):
            numberFormated = (phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))    
            z = phonenumbers.parse(numberFormated, None)
            validNumber = phonenumbers.is_valid_number(z)
            ch_number = phonenumbers.parse(numberFormated, "CH")
            geo = geocoder.description_for_number(ch_number, "es")
            #numbers, valid, location
            my_list.append(str(row[0]+", "+str(validNumber)+", "+ifnull(geo,"n/a")))
            print(row[0], validNumber, geo)

    return jsonify(results = my_list)

def ifnull(var, val):
  if var is "":
    return val
  return var

if __name__ == '__main__':
    app.run(debug=True, port=4000)