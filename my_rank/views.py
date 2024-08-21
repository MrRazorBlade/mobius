from django.shortcuts import render


def rank_view(request):
    return render(request, 'my_rank/rank.html')
