from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List

tags_metadata = [{
        "name": "Books",
        "description": "Операции с книгами: получение списка, создание, обновление и удаление книг",
}]

class Book(BaseModel):
    id: int = Field(description="Уникальный идентификатор книги", example=1)
    title: str = Field(description="Название книги", example="Преступление и наказание")
    author: str = Field(description="Автор книги", example="Ф. М. Достоевский")
    publication_year: int = Field(description="Год публикации книги", example=1866)

book_list = [Book(id = 1, title = "Война и мир", author = "Л. Н. Толстой", publication_year = 1867),
             Book(id = 2, title = "Мастер и Маргарита", author = "М. А. Булгаков", publication_year = 1967),
             Book(id = 3, title = "Маленький принц", author = "Антуана де Сент-Экзюпери", publication_year = 1943),
             Book(id = 4, title = "Анна Каренина", author = "Л. Н. Толстой", publication_year = 1878)
             ]

app = FastAPI(
    title="API обработки данных книг",
    description="Сервис для работы со списком данных о кнгиах.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

@app.get("/books", tags=["Books"], summary="Получить список всех книг",
    description="Возвращает массив всех книг. Позволяет фильтровать по автору через query.",
    response_model=List[Book])
async def get_books(author: str | None = Query(default=None, min_length=1, description="Фильтр по автору", example="Л. Н. Толстой")):
    """
    Получает список всех книг.
    - **Если параметр не указан то возвращает полный список книг**,
    - **Если параметр указан то фильтрует по автору**
    """
    if author:
        return [book for book in book_list if book.author == author]
    return book_list

@app.post("/books", response_model=Book, status_code=201, tags=["Books"], summary="Добавить новую книгу",
    description="Создает новую запись о книге.",
    responses={201: {"description": "Книга успешно создана", "content": {
                "application/json": {
                    "example": {
                        "id": 5,
                        "title": "Новая книга",
                        "author": "Новый автор",
                        "publication_year": 2025
                    }
                }
            }
        }
    }
)
async def create_book_api(book: Book):
    """
    Создает новую книгу.
    - **ID генерируется на основе максимального существующего ID + 1**,
    - **Возвращает созданную книгу с присвоенным ID**
    """

    new_id = max([b.id for b in book_list]) + 1 if book_list else 1

    new_book = Book(
        id=new_id,
        title=book.title,
        author=book.author,
        publication_year=book.publication_year
    )

    book_list.append(new_book)
    return new_book

@app.get(
    "/books/{book_id}", tags=["Books"], summary="Получить книгу по ID",
    description="Возвращает информацию о книге по ID.",
    responses={200: {"description": "Успешный ответ с данными книги", "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Война и мир",
                        "author": "Л. Н. Толстой", 
                        "publication_year": 1867
                    }
                }
            }
        },
        404: {"description": "Книга не найдена"}
    }
)
async def get_book_by_id(book_id: int = Path(description="ID книги для получения", example=1)):
    """
    Получает информацию о книге по её ID.
    
    - **Возвращает объект книги, если она найдена**,
    - **Возвращает ошибку 404, если книга с таким ID отсутствует**
    """

    for book in book_list:
        if book.id == book_id:
            return Book(id = book.id, title = book.title, author = book.author, publication_year = book.publication_year)

    raise HTTPException(status_code=404, detail="404 Not Found")

@app.delete("/books/{book_id}", tags=["Books"], summary="Удалить книгу по ID",
    description="Удаляет книгу из библиотеки по её уникальному идентификатору.",
    responses={200: {"description": "Книга успешно удалена, возвращает обновленный список книг", "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 2,
                            "title": "Мастер и Маргарита",
                            "author": "М. А. Булгаков",
                            "publication_year": 1967
                        },
                        {
                            "id": 3, 
                            "title": "Маленький принц",
                            "author": "Антуана де Сент-Экзюпери",
                            "publication_year": 1943
                        }
                    ]
                }
            }
        },
        404: {"description": "Книга не найдена"}
    }
)
async def delete_book_by_id(book_id: int = Path(description="ID книги для удаления", example=1)):
    """
    Удаляет книгу из списка по её ID.
    - **Удаляет книгу с указанным ID из списка**,
    - **Возвращает обновленный список книг после удаления**,
    - **Возвращает ошибку 404, если книга с указанным ID не найдена**
    """

    for book in book_list:
        if book.id == book_id:
            book_list.remove(book)
            return book_list

    raise HTTPException(status_code=404, detail="404 Not Found")

@app.put("/books/{book_id}", tags=["Books"], summary="Обновить книгу по ID",
    description="Полностью обновляет информацию о книге по её уникальному идентификатору.",
    responses={200: {"description": "Книга успешно обновлена", "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Обновленное название",
                        "author": "Обновленный автор",
                        "publication_year": 2024
                    }
                }
            }
        },
        404: {"description": "Книга не найдена"}
    }
)
async def put_book_by_id(book_id: int = Path(description="ID книги для обновления", example=1), book_data: Book = Path(description="Данные о книги для обновления")):
    """
    Полностью обновляет информацию о существующей книге.
    
    - **Обновляет все поля книги с указанным ID**,
    - **Требует полного объекта книги в запросе**,
    - **Возвращает обновленную книгу**,
    - **Возвращает ошибку 404, если книга с указанным ID не найдена**
    """
    
    for book in book_list:
        if book.id == book_id:
            book.title = book_data.title
            book.author = book_data.author
            book.publication_year = book_data.publication_year
            return book

    raise HTTPException(status_code=404, detail="404 Not Found")