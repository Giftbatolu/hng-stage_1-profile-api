import os
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from profiles_api.models import Profile

    
class Command(BaseCommand):
    help = "Seed database from JSON file"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "profiles_api", "seed_data", "seed_profiles.json")

        with open(file_path, "r") as file:
            data = json.load(file)

        for item in data["profiles"]:
            Profile.objects.get_or_create(
                name=item["name"],
                gender=item["gender"],
                gender_probability=item["gender_probability"],
                age=item["age"],
                age_group=item["age_group"],
                country_id=item["country_id"],
                country_name=item["country_name"],
                country_probability=item["country_probability"],
            )

        self.stdout.write(self.style.SUCCESS("Data seeded successfully"))