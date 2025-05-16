# FastAPI Demo Application

A simple REST API demo built with FastAPI that demonstrates CRUD operations for items.

## Features

- RESTful API endpoints for managing items
- Automatic API documentation with Swagger UI
- Input validation using Pydantic models
- CORS middleware enabled
- In-memory database for demonstration

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

- Windows:

```bash
.\venv\Scripts\activate
```

- Unix/MacOS:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the server with:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## API Endpoints

- `GET /`: Welcome message
- `GET /items`: List all items
- `GET /items/{item_id}`: Get a specific item
- `POST /items`: Create a new item
- `PUT /items/{item_id}`: Update an existing item
- `DELETE /items/{item_id}`: Delete an item

## Example Item Structure

```json
{
  "name": "Example Item",
  "description": "This is an example item",
  "price": 29.99,
  "is_available": true
}
```