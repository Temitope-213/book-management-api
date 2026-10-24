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

@app.get("/books", status_code = 200)
def get_books(genre: str = None):
    if genre is None:
        return list(books.values())

    filtered_books = []
    for book in books.values():
        if book["genre"].lower() == genre.lower():
            filtered_books.append(book)
    return filtered_books

@app.get("/books/{book_id}", status_code = 200)
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]

@app.put("/books/{book_id}", status_code = 200)
def update_book(book_id: int, book: Book):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    
    books[book_id] = {
        "id": book_id,
        "title": book.title,
        "author": book.author,
        "publication_year": book.publication_year,
        "genre": book.genre
    }
    return books[book_id]

@app.delete("/books/{book_id}", status_code = 204)
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    deleted_book = books.pop(book_id)

    return {
        "message": "Book deleted successfully",
        "book": deleted_book
    }