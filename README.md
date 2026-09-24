# College Lost & Found API

A FastAPI-based REST API for managing lost and found items in a college campus.

## Technologies Used

- Python
- FastAPI
- SQLModel
- SQLite
- Uvicorn

## Features

- Add a lost or found item
- View all items
- View item by ID
- Update an item
- Delete an item
- Filter items by status
- Filter items by category
- Input validation
- Proper error handling

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/items` | Create a new item |
| GET | `/items` | Get all items |
| GET | `/items/{item_id}` | Get item by ID |
| PUT | `/items/{item_id}` | Update an item |
| DELETE | `/items/{item_id}` | Delete an item |
| GET | `/items/status/{status}` | Filter by status |
| GET | `/items/category/{category}` | Filter by category |

## Status Values

- Lost
- Found
- Returned

## Database

The project uses SQLite with SQLModel.

Database table is created automatically when the application starts.

## How to Run

```bash
pip install -r requirements.txt