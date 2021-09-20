from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Kess


def index(request):
    latest_kess_list = Kess.objects.order_by('-date')[:5]
    context = {'latest_kess_list': latest_kess_list}
    return render(request, 'kess/index.html', context)


def detail(request, kess_id):
    kess = get_object_or_404(Kess, pk=kess_id)
    kess_hint = ''
    for letter in kess.reponse:
        if ' ' in letter:
            kess_hint += ' '
        else:
            kess_hint += '-'

    #TODO: Make it with POST instead, build a form and try to customise it's css
    if request.method == 'GET':
        if request.GET.get('answer') == kess.reponse:
            answer_state=True
        else:
            answer_state=False




    return render(request, 'kess/detail.html', {'kess': kess,
                                                'is_answer_valide': answer_state,
                                                'kess_hint': kess_hint
                                                })

