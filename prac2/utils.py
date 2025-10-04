import json

def save_to_json(data, filename="jsonparse.json"): # Записываем в json файл все данные
    with open(filename, "w") as file:
        json.dump(data, file)

