from pydantic import BaseModel, Field

class Book(BaseModel):
    id: int = Field(description="Уникальный идентификатор книги", example=1)
    title: str = Field(description="Название книги", example="Преступление и наказание")
    author: str = Field(description="Автор книги", example="Ф. М. Достоевский")
    publication_year: int = Field(description="Год публикации книги", example=1866)

class BookCreate(BaseModel):
    title: str
    author: str
    publication_year: int

class User(BaseModel):
    username: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None