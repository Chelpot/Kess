from datetime import *

from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect

from .forms import SignUpForm
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
    if datetime.now(timezone.utc) > kess.published_at + timedelta(days=3):
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
            answer_state = True
        else:
            answer_state = False

    return render(request, 'kess/detail.html', {'kess': kess,
                                                'is_answer_valide': answer_state,
                                                'kess_hint': kess_hint
                                                })


def add_kess(request):
    context = {'': ''}
    return render(request, 'kess/add_kess.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user, backend='kess.auth.CheckPasswordBackend')
            user.is_staff = False
            user.is_superuser = False
            user.points = 0
            user.save()
            return redirect('/kess')
    else:
        form = SignUpForm()
    return render(request, 'kess/signup.html', {'form': form})
