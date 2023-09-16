import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App()
{
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');

  useEffect(() =>
  {
    fetchTodos();
  }, []);

  const fetchTodos = async () =>
  {
    try
    {
      const response = await axios.get('http://localhost:5000/api/todos');
      console.log('res ->', response);
      setTodos(response.data);
    } catch (error)
    {
      console.error(error);
    }
  };

  const addTodo = async () =>
  {
    if (newTodo.trim() === '') return;
    try
    {
      const response = await axios.post('http://localhost:5000/api/todos', { text: newTodo });
      console.log('res ->', response);
      setNewTodo('');
      fetchTodos();
    } catch (error)
    {
      console.error(error);
    }
  };

  const updateTodo = async (id, text, completed) =>
  {
    try
    {
      await axios.put(`http://localhost:5000/api/todos/${id}`, {
        text,
        completed,
      });
      fetchTodos();
    } catch (error)
    {
      console.error(error);
    }
  };

  const deleteTodo = async (id) =>
  {
    try
    {
      await axios.delete(`http://localhost:5000/api/todos/${id}`);
      fetchTodos();
    } catch (error)
    {
      console.error(error);
    }
  };

  return (
    <div className="bg-gradient-to-b from-slate-900 via-slate-800 to-slate-600  text-white min-h-screen py-8 font-roboto">
      <div className="max-w-md mx-auto p-4 border border-slate-500 rounded-lg shadow-lg">
        <h1 className="text-3xl font-extrabold mb-6 text-center">Todo List</h1>

        <div className="flex mb-7">
          <input
            className=" flex-grow px-4 py-2 bg-white text-black rounded-l focus:outline-none text-base font-semibold"
            type="text"
            placeholder="Add a new todo"
            value={newTodo}
            onChange={(e) => setNewTodo(e.target.value)}
            onKeyPress={e => (e.key === 'Enter') ? addTodo() : ''}
          />
          <button
            className="border-b border-t border-r border-slate-500 px-4 py-2 bg-slate-900 text-red-600 rounded-r hover:bg-red-600 hover:text-white transition duration-300 ease-in-out text-base font-semibold"
            onClick={addTodo}
          >
            Add
          </button>
        </div>

        <ul>
          {todos.map((todo) => (

            <li
              key={todo.id}
              className="rounded-md border border-slate-500 flex items-center mb-4 bg-slate-900 rounded-lg px-4 py-2 transition duration-300 ease-in-out hover:bg-slate-700"
            >
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={(e) =>
                  updateTodo(todo.id, todo.text, e.target.checked)
                }
                className="mr-4 text-red-600 form-checkbox h-6 w-6"
              />
              <span
                className={`text-base font-semibold ${todo.completed ? 'line-through' : ''
                  }`}
              >
                {todo.text}
              </span>
              <button
                onClick={() => deleteTodo(todo.id)}
                className="ml-auto text-red-600 hover:text-red-800 transition duration-300 ease-in-out text-base font-semibold"
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div >
  );
}

export default App;
