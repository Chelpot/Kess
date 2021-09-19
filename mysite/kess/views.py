from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Kess


def index(request):
    latest_kess_list = Kess.objects.order_by('-date')[:5]
    context = {'latest_kess_list': latest_kess_list}
    return render(request, 'kess/index.html', context)


def detail(request, kess_id):
    kess = get_object_or_404(Kess, pk=kess_id)
    return render(request, 'kess/detail.html', {'kess': kess})

