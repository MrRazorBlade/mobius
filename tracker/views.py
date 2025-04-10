import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import Habit, HabitRecord
import calendar
from .forms import HabitForm
from django.contrib.auth.decorators import login_required


@login_required
def index(request, year=2024, month=8):
    # Limites de mes y año
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    # Obtener el nombre del mes
    month_name = calendar.month_name[month]

    # Obtener el mes y año actual
    days_in_month = calendar.monthrange(year, month)[1]
    days = list(range(1, days_in_month + 1))

    # Obtener solo los hábitos del usuario actual
    habits = Habit.objects.filter(user=request.user)

    # Crear una estructura de datos para los hábitos y sus registros
    habits_data = []
    total_days = days_in_month * len(habits)
    completed_days = 0
    for habit in habits:
        records = {
            record.date.day: record.completed
            for record in HabitRecord.objects.filter(habit=habit, date__year=year, date__month=month)
        }
        habits_data.append(
            {'id': habit.id, 'name': habit.name, 'records': records})
        completed_days += sum(records.values())

    if total_days > 0:
        completion_rate = (completed_days / total_days) * 100
    else:
        completion_rate = 0

    context = {
        'days': days,
        'habits': habits_data,
        'current_month': month,
        'current_month_name': month_name,
        'current_year': year,
        'completion_rate': completion_rate,
    }

    return render(request, 'tracker/index.html', context)


@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user  # Asocia el hábito al usuario
            habit.save()
            return redirect('tracker:index')
    else:
        form = HabitForm()

    return render(request, 'tracker/add_habit.html', {'form': form})


@login_required
def edit_habit(request, habit_id):
    # Asegura que el hábito pertenece al usuario
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('tracker:index')
    else:
        form = HabitForm(instance=habit)

    return render(request, 'tracker/edit_habit.html', {'form': form, 'habit': habit})


@login_required
def toggle_habit_record(request, habit_id, day, month, year):
    date = datetime.date(year, month, day)
    # Asegura que el hábito pertenece al usuario
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    record, created = HabitRecord.objects.get_or_create(habit=habit, date=date)

    if not record.completed:
        record.completed = True  # Si el hábito no está completado, se marca como completado
        if not record.reward_claimed:
            # Si la recompensa no está reclamada, se marca como reclamada y se asigna un punto
            record.reward_claimed = True
            habit.user.add_points(1)
            habit.user.save()
    else:
        # Si el hábito ya está completado, se desmarca
        record.completed = False
        # Se mantiene reward_claimed como True, para que no se otorguen puntos adicionales

    record.save()

    return redirect('tracker:index', year=year, month=month)


@login_required
def delete_habit(request, habit_id):
    # Asegura que el hábito pertenece al usuario
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == "POST":
        habit.delete()
        return redirect('tracker:index')
    return render(request, 'tracker/delete_habit.html', {'habit': habit})
