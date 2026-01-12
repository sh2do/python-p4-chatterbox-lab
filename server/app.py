from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([{
            'id': message.id,
            'body': message.body,
            'username': message.username,
            'created_at': message.created_at.isoformat(),
            'updated_at': message.updated_at.isoformat()
        } for message in messages])
    
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify({
            'id': new_message.id,
            'body': new_message.body,
            'username': new_message.username,
            'created_at': new_message.created_at.isoformat(),
            'updated_at': new_message.updated_at.isoformat()
        }), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get_or_404(id)
    
    if request.method == 'PATCH':
        data = request.get_json()
        message.body = data['body']
        db.session.commit()
        
        return jsonify({
            'id': message.id,
            'body': message.body,
            'username': message.username,
            'created_at': message.created_at.isoformat(),
            'updated_at': message.updated_at.isoformat()
        })
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    app.run(port=4000, debug=True)
