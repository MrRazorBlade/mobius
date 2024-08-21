from django.shortcuts import render


def habit_list(request):
    # Lógica para listar los hábitos
    return render(request, 'habits/habit_list.html')
