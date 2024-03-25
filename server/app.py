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

@app.route('/messages', methods=['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

@app.post('/messages')
def post_message():
    data = request.json
    try:
        message = Message(
            body=data.get('body'),
            username=data.get('username'),
        )
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict())
    except Exception as e:
        print(e)
        return {'error': f"could not post message {e}"}, 405
    
@app.patch('/messages/<int:id>')
def patch_message(id):
    message = db.session.get(Message, id)
    if not message:
        return {"error": "message not found"}
    try:
        data = request.json
        for key in data:
            setattr(message, key, data[key])
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict())
    except Exception as e:
        return {"error": f"{e}"}
    
@app.delete('/messages/<int:id>')
def delete_message(id):
    message = db.session.get(Message, id)
    if not message:
        return {"error": "message not found"}, 404
    db.session.delete(message)
    db.session.commit()
    return {}, 202

if __name__ == '__main__':
    app.run(port=5555)