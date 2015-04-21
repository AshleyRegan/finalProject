#! /usr/bin/env python

from flask import *
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/action/messages.db'
db = SQLAlchemy(app)

class Message(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(50))
  message = db.Column(db.String(255))
  
  def __init__(self, name, message):
    self.name = name
    self.message = message

  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
      'message': self.message
    }
    
db.create_all()

def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

@app.route('/')
def index():
  names = ['Alice', 'Bob', 'Carol', 'David', 'Ed']
  return render_template('index.html', names=names)

@app.route('/msg', methods=['GET'])
def messageIndex():
  messages = Message.query.all()
  
  if request_wants_json():
    data = {'messages': [message.serialize() for message in messages]}
    return jsonify(data)
  else:
    return render_template('messageIndex.html', messages=messages)

@app.route('/msg', methods=['POST'])
def messageCreate():
  name = request.form.get('from')
  messageText = request.form.get('message')

  message = Message(name, messageText)
  db.session.add(message)
  db.session.commit()  
  return redirect(url_for('messageIndex'))

@app.route('/msg/new')
def messageNewHtml():
  return render_template('messageNewHtml.html')

@app.route('/msg/<int:msgId>')
def messageShow(msgId):
  message = Message.query.get(msgId)

  if request_wants_json():
    return jsonify(message.serialize())

  return render_template('messageShow.html', message=message)




if __name__ == '__main__':
  app.debug = True
  app.run(host='0', port=3000)
  
