# FastAPI Todo List App

A simple Todo List API built with FastAPI and SQLite.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

Start the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Create Todo
- **POST** `/todos/`
- Body: `{"title": "Buy groceries", "description": "Milk, eggs, bread"}`

### Get All Todos
- **GET** `/todos/`

### Get Single Todo
- **GET** `/todos/{todo_id}`

### Update Todo
- **PUT** `/todos/{todo_id}`
- Body: `{"title": "Updated title", "completed": true}`

### Delete Todo
- **DELETE** `/todos/{todo_id}`

## Database

SQLite database is automatically created at `./todos.db`
