import re
import requests
import json
from flask import Flask, redirect, url_for, request


# Defining the api-endpoint
url = 'https://www.10bis.co.il/NextApi/GetRestaurantMenu?culture=en&uiCulture=en&restaurantId=19156&deliveryMethod=pickup'

response = requests.request(method='GET', url=url)

# Formatted output
decodedResponse = json.loads(response.text)
# print (json.dumps(decodedResponse, sort_keys=True, indent=4))

print (decodedResponse["Data"]["categoriesList"][3]["dishList"][0]["dishId"])

def GET_food(id,categoryID):
    dishId = decodedResponse["Data"]["categoriesList"][categoryID]["dishList"][id]["dishId"]
    dishName = decodedResponse["Data"]["categoriesList"][categoryID]["dishList"][id]["dishName"]
    dishDescription = decodedResponse["Data"]["categoriesList"][categoryID]["dishList"][id]["dishDescription"]
    dishPrice = decodedResponse["Data"]["categoriesList"][categoryID]["dishList"][id]["dishPrice"]

    pizza = {dishId, dishName, dishDescription, dishPrice}
    return pizza

def GET_pizzas():
    pizzas = []
    for pizza in range(4):
        pizzas.append(GET_food(pizza,3))
    return pizzas

def GET_deserts():
    deserts = []
    for desert in range(3):
        deserts.append(GET_food(desert,4))
    return deserts

def GET_drinks():
    drinks = []
    for drink in range(8):
        drinks.append(GET_food(drink,5))
    return drinks




def POST_order(pizzas, desserts, drinks):
    totalPrice = 0
    for pizza in pizzas:
        totalPrice += decodedResponse["Data"]["categoriesList"][3]["dishList"][pizza]["dishPrice"]
    
    for dessert in desserts:
        totalPrice += decodedResponse["Data"]["categoriesList"][4]["dishList"][dessert]["dishPrice"]
    
    for drink in drinks:
        totalPrice += decodedResponse["Data"]["categoriesList"][5]["dishList"][drink]["dishPrice"]
    print(totalPrice)

    return totalPrice


app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
   return 'pizza %s' % GET_food(int(name),3)

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True) 