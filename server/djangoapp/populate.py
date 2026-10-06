from django.db import transaction
from .models import CarMake, CarModel


@transaction.atomic
def initiate():
    cars = [
        ("NISSAN", "Japanese", [
            ("Pathfinder", "SUV"),
            ("Qashqai", "SUV"),
            ("XTRAIL", "SUV"),
        ]),
        ("Mercedes", "German", [
            ("A-Class", "SUV"),
            ("C-Class", "SUV"),
            ("E-Class", "SUV"),
        ]),
        ("Audi", "German", [
            ("A4", "SUV"),
            ("A5", "SUV"),
            ("A6", "SUV"),
        ]),
        ("Kia", "Korean", [
            ("Sorrento", "SUV"),
            ("Carnival", "SUV"),
            ("Cerato", "SEDAN"),
        ]),
        ("Toyota", "Japanese", [
            ("Corolla", "SEDAN"),
            ("Camry", "SEDAN"),
            ("Kluger", "SUV"),
        ]),
    ]

    for name, country, models in cars:
        make, _ = CarMake.objects.get_or_create(
            name=name,
            defaults={"description": f"Great cars. {country} technology"},
        )
        for model_name, car_type in models:
            CarModel.objects.get_or_create(
                car_make=make,
                name=model_name,
                defaults={
                    "type": car_type,
                    "year": 2023,
                    "dealer_id": 1,
                },
            )
