import os
from typing import List

import asyncpg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres"
)


class Item(BaseModel):
    id: int = None
    name: str
    description: str = None


async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT
        )
    """)
    await conn.close()


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
async def root():
    return {"message": "Приложение работает! Соединение с базой данных установлено."}


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    conn = await asyncpg.connect(DATABASE_URL)
    result = await conn.fetchrow(
        "INSERT INTO items (name, description) VALUES ($1, $2) RETURNING id, name, description",
        item.name,
        item.description,
    )
    await conn.close()
    return dict(result)


@app.get("/items/", response_model=List[Item])
async def read_items():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("SELECT id, name, description FROM items")
    await conn.close()
    return [dict(row) for row in rows]


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    conn = await asyncpg.connect(DATABASE_URL)
    row = await conn.fetchrow(
        "SELECT id, name, description FROM items WHERE id = $1", item_id
    )
    await conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    return dict(row)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
