from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def flow(request):
    return render(request, 'flow/flow.html')
