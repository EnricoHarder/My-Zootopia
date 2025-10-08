import json
import os

import requests
import sys
from dotenv import load_dotenv

API_URL = "https://api.api-ninjas.com/v1/animals"
load_dotenv()
API_KEY = os.getenv('API_KEY')



def fetch_animals_from_api(animal_name):
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        print("FEHLER: API-Schlüssel ist nicht konfiguriert. Bitte ersetze 'YOUR_API_KEY_HERE'.")
        return []

    headers = {'X-Api-Key': API_KEY}
    params = {'name': animal_name}

    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Fehler beim API-Aufruf: {e}")
        return []


def serialize_animal(animal_obj):
    output = '<li class="cards__item">\n'

    name = animal_obj.get('name', 'Unbekanntes Tier')
    output += f'  <div class="card__title">{name}</div>\n'

    card_list_items = ""
    characteristics = animal_obj.get('characteristics', {})

    diet = characteristics.get('diet')
    if diet:
        card_list_items += f'      <li><strong>Diet:</strong> {diet}</li>\n'

    locations = animal_obj.get('locations')
    if isinstance(locations, list) and len(locations) > 0:
        card_list_items += f'      <li><strong>Location:</strong> {locations[0]}</li>\n'

    animal_type = characteristics.get('type')
    if animal_type:
        card_list_items += f'      <li><strong>Type:</strong> {animal_type}</li>\n'

    if card_list_items:
        output += '  <div class="card__text">\n'
        output += '    <ul>\n'
        output += card_list_items
        output += '    </ul>\n'
        output += '  </div>\n'

    output += '</li>\n'

    return output.strip()


if __name__ == "__main__":

    animal_query = input("Enter a name of an animal: ")

    animals_data = fetch_animals_from_api(animal_query)

    animals_info_string = ""

    if isinstance(animals_data, list) and len(animals_data) > 0:
        for animal_obj in animals_data:
            animals_info_string += serialize_animal(animal_obj)

        animals_info_string = animals_info_string.strip()
    else:
        error_message = f'<li class="cards__item">\n<h2>The animal "{animal_query}" doesn\'t exist. 😢</h2>\n</li>'
        animals_info_string = error_message

    try:
        with open('animals_template.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print("Fehler: Die Datei 'animals_template.html' wurde nicht gefunden.")
        sys.exit(1)

    final_html_content = template_content.replace('__REPLACE_ANIMALS_INFO__', animals_info_string)

    try:
        with open('animals.html', 'w', encoding='utf-8') as f:
            f.write(final_html_content)

        print("Website was successfully generated to the file animals.html.")

    except Exception as e:
        print(f"Fehler beim Schreiben der Datei 'animals.html': {e}")
        sys.exit(1)