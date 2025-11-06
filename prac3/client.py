import requests

rest_api_url = "http://127.0.0.1:8000"

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

def send_post(json):
    response = requests.post(f"{rest_api_url}/books", json=json)
    response.raise_for_status()

    if response.status_code == 201:
        print("\nStatus code 201 Created")
    else:
        print(f"\nStatus code {response.status_code}")
        return

    data = response.json()
    for i, j in data.items():
        print(f"{i}: {j}")

def del_book(id):
    response = requests.delete(f"{rest_api_url}/books/{id}")
    response.raise_for_status()

    if response.status_code == 200:
        print("\nStatus code 200 OK")
    else:
        print(f"\nStatus code {response.status_code}")
        return

    data = response.json()
    for i in range(len(data)):
        print(f"{data[i]['id']}: {data[i]['title']}, {data[i]['author']}, {data[i]['publication_year']}")

def update_book(id, data):
    response = requests.put(f"{rest_api_url}/books/{id}", json = data)

    if response.status_code == 200:
        print("\nStatus code 200 OK")
    else:
        print(f"\nStatus code {response.status_code}")
        return

    data = response.json()
    for i, j in data.items():
        print(f"{i}: {j}")

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
            update_book(book_id, {"id": book_id_int, "title": title, "author": author, "publication_year": publication_year})
        case 6:
            print("Enter info about book to add it to list:")
            book_id = int(input("ID: "))
            title = input("Title: ")
            author = input("Author: ")
            publication_year = int(input("Publication year: "))
            send_post({"id": book_id, "title": title, "author": author, "publication_year": publication_year})
        case _:
            print("Invalid choice. Please select a valid option.")



def main():
    while True:
        print("\nChoose action:")
        print("1. Get list of books.")
        print("2. Get list of books by author.")
        print("3. Get book from list by id.")
        print("4. Delete book from list by id.")
        print("5. Update book info.")
        print("6. Add new book to list.")
        print("7. Exit.")

        choice = input("Enter your choice (1-7): ")

        if choice == '7':
            print("Stop program!")
            break

        switch_action(choice)


if __name__ == "__main__":
    main()
