import json


def load_data(file_path):
    """ Loads a JSON file """
    with open(file_path, "r") as handle:
        return json.load(handle)


if __name__ == "__main__":
    # Daten laden
    try:
        animals_data = load_data('animals_data.json')
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        print(f"Fehler beim Laden der Datei: {e}")
        exit()

    # String mit Tierdaten erzeugen (nutzt <br> anstelle von \n)
    animals_info_string = ""

    if isinstance(animals_data, list):
        for animal in animals_data:

            # --- Beginn eines Tierblocks ---

            if 'name' in animal:
                animals_info_string += f"Name: {animal['name']}<br>"

            characteristics = animal.get('characteristics')

            if characteristics:
                if 'diet' in characteristics:
                    animals_info_string += f"Diet: {characteristics['diet']}<br>"

                if 'type' in characteristics:
                    animals_info_string += f"Type: {characteristics['type']}<br>"

            if 'locations' in animal and isinstance(animal['locations'], list) and len(animal['locations']) > 0:
                animals_info_string += f"Location: {animal['locations'][0]}<br>"

        # Entfernt den letzten <br> am Ende des gesamten Strings
        animals_info_string = animals_info_string.removesuffix('<br>')

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