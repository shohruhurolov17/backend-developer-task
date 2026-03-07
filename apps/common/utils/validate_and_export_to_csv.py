from rest_framework.exceptions import ValidationError
from django.conf import settings
import csv
import os


data = [
    {
        "id": 1,
        "name": "Shohruh",
        "address": {
            "city": "Tashkent",
            "zip": 100000
        },
        "orders": [
            {"product": "iPhone 14 Pro", "price": 1000, "currency": "USD"},
            {"product": "Mouse", "price": 100000, "currency": "UZS"}
        ]
    }
]

schema = {
    "id": {"type": int},
    "name": {"type": str},
    "address": {
        "type": dict,
        "schema": {
            "city": {"type": str},
            "zip": {"type": int}
        }
    },
    "orders": {
        "type": list,
        "items": {
            "product": {"type": str},
            "price": {"type": int},
            "currency": {"type": str}
        }
    }
}


def validate_json(data, schema, path="root"):

    if not isinstance(data, dict):
        raise ValidationError("Expected object", path)

    for key, rule in schema.items():

        if key not in data:
            raise ValidationError(f"Missing key '{key}'", path)

        value = data[key]
        expected_type = rule.get("type")

        if expected_type and not isinstance(value, expected_type):
            raise ValidationError(
                f"Expected type {expected_type.__name__} but got {type(value).__name__}",
                f"{path}.{key}"
            )

        if expected_type == dict and "schema" in rule:
            validate_json(value, rule["schema"], f"{path}.{key}")

        if expected_type == list and "items" in rule:
            for i, item in enumerate(value):
                validate_json(item, rule["items"], f"{path}.{key}[{i}]")


def flatten_json(data, parent_key="", sep="."):
    items = {}

    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k

        if isinstance(v, dict):
            items.update(flatten_json(v, new_key, sep))

        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.update(flatten_json(item, f"{new_key}[{i}]", sep))
                else:
                    items[f"{new_key}[{i}]"] = item
        else:
            items[new_key] = v

    return items


def json_to_csv(data_list, filename="output.csv"):

    flattened = [flatten_json(item) for item in data_list]

    # CSV header
    headers = set()
    for row in flattened:
        headers.update(row.keys())

    headers = list(headers)

    file = os.path.join(settings.BASE_DIR, f'media/csv/{filename}')

    with open(file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for row in flattened:
            writer.writerow(row)


def validate_and_export_to_csv():

    try:
        
        for item in data:
            validate_json(item, schema)

        json_to_csv(data)

        print("CSV successfully created")

    except ValidationError as err:
        print("Error:", err)