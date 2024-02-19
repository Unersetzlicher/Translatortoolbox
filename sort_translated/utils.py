import re
from langdetect import detect


def detect_language(input_string):
    try:
        return detect(input_string)
    except:
        return 'en'  # Default to English if detection fails


def get_conjunction(language):
    conjunctions = {
        'en': ' and ',
        'fr': ' et ',
        'ru': ' и ',
        'es': ' y ',
    }
    return conjunctions.get(language, ' and ')  # Default to 'and'


def replace_last_conjunction(sanitized_string, conjunction):
    if conjunction in sanitized_string:
        parts = sanitized_string.rsplit(conjunction, 1)
        if len(parts) == 2:
            sanitized_string = ','.join(parts)  # Replace the last occurrence only
    return sanitized_string


# Update other functions as necessary...

def sanitize_and_process(input_string):
    sanitized_string = input_string.strip()
    last_character = ''
    if sanitized_string and sanitized_string[-1] in {'.', ',', ';'}:
        last_character = sanitized_string[-1]
        sanitized_string = sanitized_string[:-1]

    language = detect_language(sanitized_string)
    conjunction = get_conjunction(language)

    # Apply language-specific replacements here...

    # Replace the last conjunction with a comma before splitting
    sanitized_string = replace_last_conjunction(sanitized_string, conjunction)

    # Split the countries, considering both commas and semicolons as delimiters
    countries = re.split(r'[;,]\s*', sanitized_string)

    # Sort the list and rejoin with the appropriate conjunction and last character
    sorted_string = sort_countries(countries, last_character, conjunction)

    return sorted_string


def sort_countries(countries, last_character, conjunction):
    # Ensure countries list is sorted
    sorted_countries = sorted(countries)

    # Join all but the last with a comma, and add the last one with the conjunction
    if len(sorted_countries) > 1:
        sorted_string = ', '.join(sorted_countries[:-1]) + f"{conjunction}" + sorted_countries[-1]
    else:
        # Handle the case with only one country in the list
        sorted_string = ''.join(sorted_countries)

    # Append the last character if it's a punctuation
    if last_character:
        sorted_string += last_character

    return sorted_string

replacements_en = {
        "Antigua and Barbuda": "Antigua_and_Barbuda",
        "Bosnia and Herzegovina": "Bosnia_and_Herzegovina",
        "Saint Kitts and Nevis": "Saint_Kitts_and_Nevis",
        "Saint Vincent and the Grenadines": "Saint_Vincent_and_the_Grenadines",
        "Sao Tome and Principe": "Sao_Tome_and_Principe",
        "Trinidad and Tobago": "Trinidad_and_Tobago",
        "United Kingdom of Great Britain and Northern Ireland": "United_Kingdom_of_Great_Britain_and_Northern_Ireland",
        "Hong Kong, China": "Hong_Kong_China",
        "Macao, China": "Macao_China"
    }
replacements_ru = {
        "Антигуа и Барбуда": "Антигуа_и_Барбуда",
        "Босния и Герцеговина": "Босния_и_Герцеговина",
        "Сент-Китс и Невис": "Сент_Китс_и_Невис",
        "Сент-Винсент и Гренадины": "Сент_Винсент_и_Гренадины",
        "Сан-Томе и Принсипи": "Сан_Томе_и_Принсипи",
        "Тринидад и Тобаго": "Тринидад_и_Тобаго",
        "Соединенное Королевство Великобритании и Северной Ирландии": "Соединенное_Королевство_Великобритании_и_Северной_Ирландии",
        "Гонконг, Китай": "Гонконг_Китай",
        "Макао, Китай": "Макао_Китай"
    }
replacements_es = {
        "Antigua y Barbuda": "Antigua_y_Barbuda",
        "Bosnia y Herzegovina": "Bosnia_y_Herzegovina",
        "San Cristóbal y Nieves": "San_Cristobal_y_Nieves",
        "San Vicente y las Granadinas": "San_Vicente_y_las_Granadinas",
        "Santo Tomé y Príncipe": "Santo_Tome_y_Principe",
        "Trinidad y Tobago": "Trinidad_y_Tobago",
        "Reino Unido de Gran Bretaña e Irlanda del Norte": "Reino_Unido_de_Gran_Bretaña_e_Irlanda_del_Norte",
        "Hong Kong, China": "Hong_Kong_China",
        "Macao, China": "Macao_China"
    }