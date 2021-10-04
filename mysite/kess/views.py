from django.http import Http404
from django.shortcuts import get_object_or_404, render
from datetime import *

from .models import Kess


def index(request):
    # Look for Kess ready to be published only
    latest_kess_list = Kess.objects.filter(
        is_ready_to_publish=True,
    ).order_by('-published_at')[:10]
    context = {'latest_kess_list': latest_kess_list}
    return render(request, 'kess/index.html', context)


def detail(request, kess_id):
    kess = get_object_or_404(Kess, pk=kess_id)
    kess_hint = ''

    # Only display hint for current kess when it's been 3 days since publication date
    if datetime.now(timezone.utc) > kess.published_at + timedelta(days = 3):
        for letter in kess.reponse:
            if ' ' in letter:
                kess_hint += ' '
            else:
                kess_hint += '-'
    else:
        kess_hint = "Vous aurez l'indice quand le Kess sera publié depuis 3 jours."
    # TODO: Make it with POST instead, build a form and try to customise it's css
    if request.method == 'GET':
        if request.GET.get('answer') == kess.reponse:
            answer_state=True
        else:
            answer_state=False

    return render(request, 'kess/detail.html', {'kess': kess,
                                                'is_answer_valide': answer_state,
                                                'kess_hint': kess_hint
                                                })


def add_kess(request):
    context = {'': ''}
    return render(request, 'kess/add_kess.html', context)
