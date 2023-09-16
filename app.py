from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the React frontend

# Load environment variables from .env file
load_dotenv()
db_uri = os.getenv("SQLALCHEMY_DATABASE_URI")
# Replace the SQLite URI with your MariaDB URI
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Get all todos
@app.get('/api/todos')
def get_todos():
    todos = Todo.query.all()
    todo_list = [{'id': todo.id, 'text': todo.text, 'completed': todo.completed} for todo in todos]
    return jsonify(todo_list)

# Add a new todo
@app.post('/api/todos')
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

# Update a todo's completed status
@app.put('/api/todos/<int:id>')
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
@app.delete('/api/todos/<int:id>')
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
    app.run(debug=True)
