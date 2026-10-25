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

# Create a new book
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

# Get all books or you can filter by genre
@app.get("/books", status_code = 200)
def get_books(genre: str = None):
    if genre is None:
        return list(books.values())

    filtered_books = []
    for book in books.values():
        if book["genre"].lower() == genre.lower():
            filtered_books.append(book)
    return filtered_books

# Get one book by its ID
@app.get("/books/{book_id}", status_code = 200)
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]

# Replace an existing book (replaces all its fields)
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

# Delete a book by its ID
@app.delete("/books/{book_id}", status_code = 204)
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    deleted_book = books.pop(book_id)

    return {
        "message": "Book deleted successfully",
        "book": deleted_book
    }

# Get all books, with optional genre filtering and a limit
@app.get("/books", status_code = 200)
def get_books(genre: str = None, limit: int = None):
    result = []
    for book in books.values():
        if genre is None or book["genre"].lower() == genre.lower():
            result.append(book)
    if limit is not None:
        result = result[:limit]

    return result