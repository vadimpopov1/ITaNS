import requests
import json

rest_api_url = "http://127.0.0.1:8000"
AUTH_TOKEN = None

def get_posts(author: str | None = None):
    params = {}
    if author and author.strip():
        params["author"] = author

    response = requests.get(f"{rest_api_url}/books", params=params)
    response.raise_for_status()

    if response.status_code == 200:
        print("\nStatus code 200 OK")
    else:
        print(f"\nStatus code {response.status_code}")
        return

    data = response.json()
    for i in range(len(data)):
        print(f"{data[i]['id']}: {data[i]['title']}, {data[i]['author']}, {data[i]['publication_year']}")

def get_posts_with_id(id):
    response = requests.get(f"{rest_api_url}/books/{id}")
    response.raise_for_status()

    if response.status_code == 200:
        print("\nStatus code 200 OK")
    else:
        print(f"\nStatus code {response.status_code}")
        return

    data = response.json()
    for i, j in data.items():
        print(f"{i}: {j}")

def send_post(json_data):
    headers = {}
    if AUTH_TOKEN:
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    
    response = requests.post(f"{rest_api_url}/books", json=json_data, headers=headers)
    response.raise_for_status()

    if response.status_code == 201:
        print("\nStatus code 201 Created")
    elif response.status_code == 401:
        print("Authentication error. Please log in again.")
    else:
        print(f"\nStatus code {response.status_code}")
        return

    data = response.json()
    for i, j in data.items():
        print(f"{i}: {j}")

def del_book(id):
    headers = {}
    if AUTH_TOKEN:
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    
    try:
        response = requests.delete(f"{rest_api_url}/books/{id}", headers=headers)
        
        if response.status_code == 200:
            print("\nStatus code 200 OK")
            data = response.json()
            for i in range(len(data)):
                print(f"{data[i]['id']}: {data[i]['title']}, {data[i]['author']}, {data[i]['publication_year']}")
        elif response.status_code == 401:
            print("\nError 401: Unauthorized. Please log in first.")
            return
        elif response.status_code == 404:
            print("\nError 404: Book not found.")
            return
        else:
            print(f"\nError: Status code {response.status_code}")
            return
            
    except requests.exceptions.RequestException as e:
        print(f"\nRequest error: {e}")
        return

def update_book(id, data):
    headers = {}
    if AUTH_TOKEN:
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    
    response = requests.put(f"{rest_api_url}/books/{id}", json=data, headers=headers)

    if response.status_code == 200:
        print("\nStatus code 200 OK")
    elif response.status_code == 401:
        print("Authentication error. Please log in again.")
    else:
        print(f"\nStatus code {response.status_code}")
        return

    data = response.json()
    for i, j in data.items():
        print(f"{i}: {j}")


def register_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    response = requests.post(f"{rest_api_url}/register", json={"username": username, "password": password})
    if response.status_code == 200:
        print("Registration successful!")
        print(response.json())
    else:
        print(f"Error: {response.status_code} - {response.text}")

def login_user():
    global AUTH_TOKEN
    username = input("Enter username: ")
    password = input("Enter password: ")
    response = requests.post(f"{rest_api_url}/token", data={"username": username, "password": password})
    if response.status_code == 200:
        AUTH_TOKEN = response.json().get("access_token")
        print("Login successful. Token stored.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def add_book():
    if not AUTH_TOKEN:
        print("Error: You must be logged in to add a book. Use the 'login' command.")
        return
        
    title = input("Enter title: ")
    author = input("Enter author: ")
    year = int(input("Enter publication year: "))
    book_data = {"title": title, "author": author, "publication_year": year}
    
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    
    response = requests.post(f"{rest_api_url}/books", json=book_data, headers=headers)
    
    if response.status_code == 201:
        print("Book added successfully:")
        print(response.json())
    elif response.status_code == 401:
        print("Authentication error. Your session may have expired. Please log in again.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def switch_action(choice):
    try:
        choice = int(choice)
    except ValueError:
        print("Please enter a valid number")
        return

    match choice:
        case 1:
            print("List of books:")
            get_posts()
        case 2:
            author = input("Enter author (e.g., Л. Н. Толстой): ")
            get_posts(author)
        case 3:
            book_id = input("Enter id of book: ")
            get_posts_with_id(book_id)
        case 4:
            book_id = input("Enter id to delete a book: ")
            del_book(book_id)
        case 5:
            book_id = input("Enter id to update book: ")
            print("Enter new book data:")
            book_id_int = int(book_id)
            title = input("Title: ")
            author = input("Author: ")
            publication_year = int(input("Publication year: "))
            update_book(book_id, {"title": title, "author": author, "publication_year": publication_year})
        case 6:
            add_book()
        case 7:
            register_user()
        case 8:
            login_user()
        case 9:
            print("Stop program!")
            return "exit"
        case _:
            print("Invalid choice. Please select a valid option.")
    
    return None

while True:
    print("\nChoose action:")
    print("1. Get list of books.")
    print("2. Get list of books by author.")
    print("3. Get book from list by id.")
    print("4. Delete book from list by id.")
    print("5. Update book info.")
    print("6. Add new book to list.")
    print("7. Register new user.")
    print("8. Login.")
    print("9. Exit.")

    choice = input("Enter your choice (1-9): ")

    if choice == '9':
        print("Stop program!")
        break

    result = switch_action(choice)
    if result == "exit":
        break