import json


def load_data(file_path):
    """ Loads a JSON file """
    with open(file_path, "r") as handle:
        return json.load(handle)


def serialize_animal(animal_obj):
    """
    Erzeugt den strukturierten HTML-String für ein einzelnes Tierobjekt
    unter Verwendung von verschachtelten <ul>/<li>-Elementen.
    """
    output = '<li class="cards__item">\n'

    # --- 1. Titel (Name) ---
    if 'name' in animal_obj:
        output += f'  <div class="card__title">{animal_obj["name"]}</div>\n'

    # --- 2. Textblock-Container ---
    card_list_items = ""
    characteristics = animal_obj.get('characteristics')

    # Diet
    if characteristics and 'diet' in characteristics:
        card_list_items += f'      <li><strong>Diet:</strong> {characteristics["diet"]}</li>\n'

    # Location (Erster Ort)
    if 'locations' in animal_obj and isinstance(animal_obj['locations'], list) and len(animal_obj['locations']) > 0:
        card_list_items += f'      <li><strong>Location:</strong> {animal_obj["locations"][0]}</li>\n'

    # Type
    if characteristics and 'type' in characteristics:
        card_list_items += f'      <li><strong>Type:</strong> {characteristics["type"]}</li>\n'

    # Fügt die Liste in den div.card__text-Container ein, falls Inhalte gesammelt wurden
    if card_list_items:
        output += '  <div class="card__text">\n'
        output += '    <ul>\n'
        output += card_list_items
        output += '    </ul>\n'
        output += '  </div>\n'  # Schließt div.card__text ab

    # Ende des Listenelements/der Karte
    output += '</li>\n'

    return output.strip()


if __name__ == "__main__":
    # Daten laden
    try:
        animals_data = load_data('animals_data.json')
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        print(f"Fehler beim Laden der Datei: {e}")
        exit()

    # Den gesamten HTML-String erzeugen (vereinfachter Code)
    animals_info_string = ""

    if isinstance(animals_data, list):
        for animal_obj in animals_data:
            animals_info_string += serialize_animal(animal_obj)

        animals_info_string = animals_info_string.strip()

    # HTML-Vorlage lesen
    try:
        with open('animals_template.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print("Fehler: Die Datei 'animals_template.html' wurde nicht gefunden.")
        exit()

    # Platzhalter ersetzen
    final_html_content = template_content.replace('__REPLACE_ANIMALS_INFO__', animals_info_string)

    # Neuen Inhalt in animals.html schreiben
    try:
        with open('animals.html', 'w', encoding='utf-8') as f:
            f.write(final_html_content)

        print("Check")

    except Exception as e:
        print(f"Fehler beim Schreiben der Datei 'animals.html': {e}")