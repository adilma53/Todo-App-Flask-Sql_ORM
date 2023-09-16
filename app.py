from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the React frontend

# Get the PostgreSQL URI from environment variables
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://adil_db_name_user:ACUhYDGYHM6OEBcEkyOHk7MjfPV5RbMI@dpg-ck329vmru70s73av7kt0-a/adil_db_name'

db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/', methods=['GET'])
def get_hello():
    return 'hello adil'

# Get all todos
@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    todo_list = [{'id': todo.id, 'text': todo.text, 'completed': todo.completed} for todo in todos]
    return jsonify(todo_list)

# Add a new todo
@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_todo = Todo(text=data['text'])

    try:
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({'message': 'Todo added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Add a new todo with custom text
@app.route('/api/addtodo/<text>', methods=['POST'])
def add_custom_todo(text):
    new_todo = Todo(text=text)

    try:
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({'message': 'Todo added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update a todo's completed status
@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get(id)

    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404

    # Toggle the completed status
    todo.completed = not todo.completed

    try:
        db.session.commit()
        return jsonify({'message': 'Todo updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a todo
@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)

    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404

    try:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'message': 'Todo deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
