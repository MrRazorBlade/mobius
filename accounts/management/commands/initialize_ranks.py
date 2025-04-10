from django.core.management.base import BaseCommand
from my_rank.models import Rank


class Command(BaseCommand):
    help = 'Initializes the ranks in the database'

    def handle(self, *args, **kwargs):
        ranks = [
            {"name": "Variant", "min_points": 0, "max_points": 99},
            {"name": "Minuteman", "min_points": 100, "max_points": 499},
            {"name": "Analyst", "min_points": 500, "max_points": 1499},
            {"name": "Judge", "min_points": 1500, "max_points": 2999},
            {"name": "Time-Keeper", "min_points": 3000, "max_points": 5999},
            # max_points=None para indicar sin límite
            {"name": "Time-Keeper", "min_points": 6000, "max_points": None},
        ]

        for rank_data in ranks:
            rank, created = Rank.objects.get_or_create(
                name=rank_data["name"],
                min_points=rank_data["min_points"],
                max_points=rank_data.get("max_points")
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Rank "{rank.name}" created.'))
            else:
                self.stdout.write(f'Rank "{rank.name}" already exists.')

        self.stdout.write(self.style.SUCCESS(
            'All ranks have been initialized.'))
