from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from datetime import date

# Vista para listar las tareas y agruparlas


@login_required
def task_list(request):
    tasks = Task.objects.filter(
        user=request.user).order_by('group_order', 'group')
    groups = {}
    for task in tasks:
        if task.group in groups:
            groups[task.group].append(task)
        else:
            groups[task.group] = [task]
    return render(request, 'tasks/task_list.html', {'groups': groups})

# Vista para añadir una nueva tarea


@login_required
def add_task(request):
    groups = Task.objects.filter(user=request.user).values_list(
        # Obtener grupos distintos del usuario actual
        'group', flat=True).distinct()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Asocia la tarea al usuario actual
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form, 'groups': groups})

# Vista para mostrar el calendario


@login_required
def view_calendar(request):
    tasks = Task.objects.filter(user=request.user)
    events = []
    for task in tasks:
        if task.due_date:
            events.append({
                'title': task.title,
                'start': task.due_date.strftime('%Y-%m-%d'),
                'completed': task.completed,
            })
    return render(request, 'task_calendar/calendar.html', {'events': events})

# Vista para editar una tarea existente


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    groups = Task.objects.filter(user=request.user).values_list(
        # Obtener grupos distintos del usuario actual
        'group', flat=True).distinct()
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task, 'groups': groups})

# Vista para alternar el estado de completado de una tarea


@login_required
def toggle_task_completion(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
        return JsonResponse({'success': True})
    return redirect('task_list')


# Vista para eliminar una tarea


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/delete_task.html', {'task': task})

# Vista para eliminar todas las tareas completadas


@login_required
def delete_completed_tasks(request):
    if request.method == 'POST':
        Task.objects.filter(user=request.user, completed=True).delete()
        return redirect('task_list')
    return render(request, 'tasks/task_list.html')

# Vista para reordenar los grupos usando drag and drop


@csrf_exempt
@login_required
def reorder_groups(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        for item in data:
            tasks = Task.objects.filter(user=request.user, group=item['group'])
            for task in tasks:
                task.group_order = item['position']
                task.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'bad request'}, status=400)
