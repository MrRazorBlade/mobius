from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from my_rank.models import Rank


class Command(BaseCommand):
    help = 'Assigns initial rank to users who do not have a rank assigned'

    def handle(self, *args, **kwargs):
        # El rango de "Novato" ha sido renombrado a "Variante" desde initialize_ranks.py
        novice_rank = Rank.objects.get(min_points=0, max_points=99)

        # Filtrar usuarios sin un rango asignado
        users_without_rank = CustomUser.objects.filter(rank__isnull=True)

        for user in users_without_rank:
            user.rank = novice_rank
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f'Assigned new rank to {user.username}'))

        self.stdout.write(self.style.SUCCESS(
            'Successfully assigned initial rank to all users without a rank'))
