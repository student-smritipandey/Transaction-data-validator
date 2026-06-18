import json

with open("config/country_rules.json", "r") as f:
    country_rules = json.load(f)

def validate_phone(phone, country):

    country = str(country).strip()

    if country not in country_rules:
        return False

    expected_length = country_rules[country]["phone_length"]

    phone = str(phone)

    if not phone.isdigit():
        return False

    return len(phone) == expected_length