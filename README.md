# Docker Network with FastAPI and PostgreSQL

This project demonstrates the setup of a network with two Docker containers:
- A PostgreSQL database container
- A FastAPI web application container that connects to the database

## Running the Project

1. Clone the repository
2. Start the containers:

```bash
docker-compose up --build
```

3. Open in your browser: http://localhost:8000

## API Endpoints

- `GET /`: Health check
- `POST /items/`: Create a new item
- `GET /items/`: Get all items
- `GET /items/{item_id}`: Get item by ID

## Usage Examples

Creating an item:
```bash
curl -X POST "http://localhost:8000/items/" -H "Content-Type: application/json" -d '{"name": "Test item", "description": "Item description"}'
```

Getting all items:
```bash
curl "http://localhost:8000/items/"
```

## Important

The data in the database is preserved between container restarts thanks to the use of the named volume `postgres_data`.