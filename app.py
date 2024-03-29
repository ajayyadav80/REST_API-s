from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

#init
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init db
db = SQLAlchemy(app)

#init ma
ma = Marshmallow(app)
#############################    PRODUCT ###########################
# Product Class/Model
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  

  def __init__(self, name, description, price):
    self.name = name
    self.description = description
    self.price = price

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'price')

# Init schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)
    
#create prod
@app.route('/product', methods=['POST'])
def add_prod():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']

    new_product = Product(name,description,price)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

#GET All Product
@app.route('/product', methods=['GET'])
def get_products():
    all_product = Product.query.all()
    result = products_schema.dump(all_product)
    return jsonify(result.data)

#GET one Product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  

  product.name = name
  product.description = description
  product.price = price

  db.session.commit()

  return product_schema.jsonify(product)

# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()

  return product_schema.jsonify(product)

#############################   END OF PRODUCT ###########################

#execute server
if __name__ == '__main__':
    app.run(debug=True)
