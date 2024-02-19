# string_processor/views.py
from django.shortcuts import render
from .forms import StringForm
import re


def process_string(request):
    if request.method == 'POST':
        form = StringForm(request.POST)
        if form.is_valid():
            input_string = form.cleaned_data['input_string']
            processed_string_0, processed_string_1 = sanitize_and_process(input_string)  # Unpack the two returned strings

            # Pass both results to the template
            context = {
                'processed_string_0': processed_string_0,
                'processed_string_1': processed_string_1,
                'form': form  # Include the form in context for re-rendering
            }
            return render(request, 'translated_and_sorted_list_output.html', context)
        else:
            return render(request, 'list_to_translate_and_sort_form.html', {'form': form})
    else:
        form = StringForm()

    return render(request, 'list_to_translate_and_sort_form.html', {'form': form})



import json
import os
from django.conf import settings

def sanitize_and_process(input_string):
    # Build the path to country_translations.json
    file_path = os.path.join(settings.BASE_DIR, 'list_translate_and_sort', 'country_translations.json')

    # Load country translations from JSON file
    with open(file_path, 'r') as file:
        country_translations = json.load(file)

    # Sanitize the string
    sanitized_string = custom_strip(input_string)

    # Remove the last "." "," or ";" if any
    last_character = ''
    if sanitized_string[-1] in {'.', ',', ';'}:
        last_character = sanitized_string[-1]
        sanitized_string = sanitized_string[:-1]


    # Replace 'and' with ',' in country names and replace territories with ','
    replacements = {
        "Antigua and Barbuda": "Antigua_and_Barbuda",
        "Bosnia and Herzegovina": "Bosnia_and_Herzegovina",
        "Saint Kitts and Nevis": "Saint Kitts_and_Nevis",
        "Saint Vincent and the Grenadines": "Saint Vincent_and_the Grenadines",
        "Sao Tome and Principe": "Sao Tome_and_Principe",
        "Trinidad and Tobago": "Trinidad_and_Tobago",
        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom of Great Britain_and_Northern Ireland",
        "Hong Kong, China": "Hong Kong_China",
        "Macao, China": "Macao_China"
    }

    # Apply the replacements
    for old, new in replacements.items():
        sanitized_string = sanitized_string.replace(old, new)

    # Replace the last "and" with ","
    sanitized_string = sanitized_string.rsplit(' and', 1)
    sanitized_string = ','.join(sanitized_string)

    # Split the countries
    countries = re.split(r'[;,]\s*', sanitized_string)

    translated_countries_0 = []
    translated_countries_1 = []

    for country in countries:
        country = country.strip()

        # Check for and remove 'The ' or 'the ' prefix
        if country.lower().startswith('the '):
            country = country[4:]

        # Get the translations
        translation = country_translations.get(country, [country, country])
        translated_countries_0.append(translation[0])
        translated_countries_1.append(translation[1])

    # Sort the lists
    translated_countries_0.sort()
    translated_countries_1.sort()

    # Join the lists into strings
    if len(translated_countries_0) > 1:
        to_return_0 = ', '.join(translated_countries_0[:-1]) + " и " + translated_countries_0[-1] + last_character
        to_return_1 = ', '.join(translated_countries_1[:-1]) + " и " + translated_countries_1[-1] + last_character
    else:
        to_return_0 = "".join(translated_countries_0) + last_character
        to_return_1 = "".join(translated_countries_1) + last_character

    return to_return_0, to_return_1


def custom_strip(input_string):
    # Pattern to match undesired characters at the start of the string
    # ^ matches the start of the string, [^a-zA-Z.,;:] matches any char not a letter or .,;:
    input_string = re.sub(r'^[^a-zA-Z.,;:]+', '', input_string)

    # This pattern looks for undesired characters at the end of the string,
    # ensuring to keep the final punctuation marks if present.
    # It does so by capturing a group of allowed punctuation marks right before the end of the string
    # and only removing characters that do not belong to the set [a-zA-Z.,;:] before this group.
    input_string = re.sub(r'[^a-zA-Zа-яА-Я.,;:]+([.,;:]?)$', r'\1', input_string)

    return input_string

