# FastAPI Todo List

A simple todo list API built with FastAPI and SQLite.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API documentation: `http://localhost:8000/docs`
Alternative docs: `http://localhost:8000/redoc`

## Endpoints

- `GET /` - List all todos
- `GET /todos/{todo_id}` - Get a specific todo
- `POST /todos` - Create a new todo
- `PUT /todos/{todo_id}` - Update a todo
- `DELETE /todos/{todo_id}` - Delete a todo
- `GET /health` - Health check

## Example Usage

Create a todo:
```bash
curl -X POST "http://localhost:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "description": "Build my first API"}'
```

Get all todos:
```bash
curl "http://localhost:8000/"
```

Update a todo:
```bash
curl -X PUT "http://localhost:8000/todos/1" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

Delete a todo:
```bash
curl -X DELETE "http://localhost:8000/todos/1"
```