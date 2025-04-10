from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required
def flow(request):
    return render(request, 'flow/flow.html')


@csrf_exempt
@login_required
def assign_point(request):
    if request.method == 'POST':
        try:
            user = request.user
            # Asignar un punto al usuario
            user.add_points(1)
            user.save()
            return JsonResponse({'status': 'success', 'points': user.points})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        return JsonResponse({'status': 'error'}, status=400)
