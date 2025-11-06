from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    author: str
    publication_year: int

book_list = [Book(id = 1, title = "Война и мир", author = "Л. Н. Толстой", publication_year = 1867),
             Book(id = 2, title = "Мастер и Маргарита", author = "М. А. Булгаков", publication_year = 1967),
             Book(id = 3, title = "Маленький принц", author = "Антуана де Сент-Экзюпери", publication_year = 1943),
             Book(id = 4, title = "Анна Каренина", author = "Л. Н. Толстой", publication_year = 1878)
             ]

app = FastAPI()

@app.get("/books")
async def get_books(author: str | None = Query(default=None, min_length=1)):
    if author:
        return [book for book in book_list if book.author == author]
    return book_list

@app.post("/books", response_model=Book, status_code=201)
async def create_book_api(book: Book):
    new_id = max([b.id for b in book_list]) + 1 if book_list else 1

    new_book = Book(
        id=new_id,
        title=book.title,
        author=book.author,
        publication_year=book.publication_year
    )

    book_list.append(new_book)
    return new_book

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int):
    for book in book_list:
        if book.id == book_id:
            return Book(id = book.id, title = book.title, author = book.author, publication_year = book.publication_year)

    raise HTTPException(status_code=404, detail="404 Not Found")

@app.delete("/books/{book_id}")
async def delete_book_by_id(book_id: int):
    for book in book_list:
        if book.id == book_id:
            book_list.remove(book)
            return book_list

    raise HTTPException(status_code=404, detail="404 Not Found")

@app.put("/books/{book_id}")
async def put_book_by_id(book_id: int, book_data: Book):
    for book in book_list:
        if book.id == book_id:
            book.title = book_data.title
            book.author = book_data.author
            book.publication_year = book_data.publication_year
            return book

    raise HTTPException(status_code=404, detail="404 Not Found")
