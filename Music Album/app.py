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

#############################    Music ALBUM  ###########################
# Employee Class/Model
class MusicAlbum(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique = True)
  singer = db.Column(db.String(100))
  Rdate = db.Column(db.String(200))
  
  

  def __init__(self, name, singer , Rdate):
    self.name = name
    self.singer = singer
    self.Rdate = Rdate

# Product Schema
class MusicAlbumSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'singer' , 'Rdate')

# Init schema
MA_schema = MusicAlbumSchema(strict=True)
MAs_schema = MusicAlbumSchema(many=True, strict=True)
    
#create prod
@app.route('/MusicAlbum', methods=['POST'])
def add_alb():
    name = request.json['name']
    singer = request.json['singer']
    Rdate = request.json['Rdate']

    new_album = MusicAlbum(name,singer,Rdate)

    db.session.add(new_album)
    db.session.commit()

    return MA_schema.jsonify(new_album)

#GET All Product
@app.route('/MusicAlbum', methods=['GET'])
def get_albs():
    all_alb =MusicAlbum.query.all()
    result = MAs_schema.dump(all_alb)
    return jsonify(result.data)

#GET one Product
@app.route('/MusicAlbum/<id>', methods=['GET'])
def get_alb(id):
    alb = MusicAlbum.query.get(id)
    return MA_schema.jsonify(alb)

@app.route('/MusicAlbum/<id>', methods=['PUT'])
def update_alb(id):
  alb = MusicAlbum.query.get(id)

  name = request.json['name']
  singer = request.json['singer']
  Rdate = request.json['Rdate']
  

  alb.name = name
  alb.singer = singer
  alb.Rdate = Rdate

  db.session.commit()

  return MA_schema.jsonify(alb)

# Delete Product
@app.route('/MusicAlbum/<id>', methods=['DELETE'])
def delete_alb(id):
  alb = MusicAlbum.query.get(id)
  db.session.delete(alb)
  db.session.commit()

  return MA_schema.jsonify(alb)

#############################   END OF Music ALBUM ###########################

#execute server
if __name__ == '__main__':
    app.run(debug=True)
