# string_processor/views.py
from django.shortcuts import render
from .forms import StringForm



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
    sanitized_string = input_string.strip()

    # Remove the last "." if any
    last_character = ""
    if sanitized_string.endswith('.') or sanitized_string.endswith(',') or sanitized_string.endswith(';'):
        last_character = sanitized_string[-1]
        sanitized_string = sanitized_string[:-1]


    # Replace 'and' with ',' in country names and replace territories with ','
    replacements = {
        "Antigua and Barbuda": "Antigua_and_Barbuda",
        "Bosnia and Herzegovina": "Bosnia_and_Herzegovina",
        "Saint Kitts and Nevis": "Saint Kitts_and_Nevis",
        "Saint Vincent and the Grenadines": "Saint_Vincent_and_the_Grenadines",
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
    sanitized_string = sanitized_string.rsplit('and', 1)
    sanitized_string = ','.join(sanitized_string)

    countries = sanitized_string.split(',')
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
    to_return_0 = ', '.join(translated_countries_0[:-1]) + " и " + translated_countries_0[-1] + last_character
    to_return_1 = ', '.join(translated_countries_1[:-1]) + " и " + translated_countries_1[-1] + last_character

    return to_return_0, to_return_1
