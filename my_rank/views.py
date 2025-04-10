from django.shortcuts import render, get_object_or_404
from my_rank.models import Rank
from django.contrib.auth.decorators import login_required


@login_required
def rank_view(request):
    user = request.user
    rank = user.rank  # El rango actual del usuario
    total_points = user.points

    # Obtener todos los rangos para el menú desplegable
    ranks = Rank.objects.all().order_by('min_points')

    # Calcular el rango actual y el siguiente rango
    current_rank = rank
    next_rank = Rank.objects.filter(
        min_points__gt=current_rank.min_points).order_by('min_points').first()

    # Calcular el progreso dentro del rango actual
    if next_rank:
        progress = (total_points - current_rank.min_points) / \
            (next_rank.min_points - current_rank.min_points) * 100
    else:
        progress = 100  # Caso en que el usuario ha alcanzado el rango más alto

    context = {
        'rank': current_rank,
        'next_rank': next_rank,
        'progress': progress,
        'total_points': total_points,
        'ranks': ranks,
    }
    return render(request, 'my_rank/rank.html', context)
