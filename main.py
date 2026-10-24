from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

books = {}
next_id = 1

class Book(BaseModel):
    title: str
    author: str
    publication_year: int
    genre: str

@app.post("/books", status_code = 201)
def create_book(book: Book):
    global next_id

    new_book = {
        "id": next_id,
        "title": book.title,
        "author": book.author,
        "publication_year": book.publication_year,
        "genre": book.genre 
    }

    books[next_id] = new_book
    next_id += 1
    return new_book