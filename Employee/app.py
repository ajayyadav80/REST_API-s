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

#############################    Employee ###########################
# Employee Class/Model
class Employee(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  designation = db.Column(db.String(200))
  salary = db.Column(db.Integer)
  

  def __init__(self, name, designation , salary):
    self.name = name
    self.designation = designation
    self.salary = salary

# Product Schema
class EmployeeSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'designation' , 'salary')

# Init schema
employee_schema = EmployeeSchema(strict=True)
employees_schema = EmployeeSchema(many=True, strict=True)
    
#create prod
@app.route('/employee', methods=['POST'])
def add_emp():
    name = request.json['name']
    designation = request.json['designation']
    salary = request.json['salary']

    new_employee = Employee(name,designation,salary)

    db.session.add(new_employee)
    db.session.commit()

    return employee_schema.jsonify(new_employee)

#GET All Product
@app.route('/employee', methods=['GET'])
def get_employees():
    all_emp =Employee.query.all()
    result = employees_schema.dump(all_emp)
    return jsonify(result.data)

#GET one Product
@app.route('/employee/<id>', methods=['GET'])
def get_emp(id):
    emp = Employee.query.get(id)
    return employee_schema.jsonify(emp)

@app.route('/employee/<id>', methods=['PUT'])
def update_emp(id):
  emp = Employee.query.get(id)

  name = request.json['name']
  designation = request.json['designation']
  salary = request.json['salary']
  

  emp.name = name
  emp.designation = designation
  emp.salary = salary

  db.session.commit()

  return employee_schema.jsonify(emp)

# Delete Product
@app.route('/employee/<id>', methods=['DELETE'])
def delete_emp(id):
  emp = Employee.query.get(id)
  db.session.delete(emp)
  db.session.commit()

  return employee_schema.jsonify(emp)

#############################   END OF EMPLOYEE ###########################

#execute server
if __name__ == '__main__':
    app.run(debug=True)
